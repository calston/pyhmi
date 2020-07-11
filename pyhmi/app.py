import os
import importlib
import asyncio

import yaml

import pygame
from pygame.locals import *
from .widgets.base import Widget

_WIDGET_CACHE = {}

DEBUG = False


class View(Widget):
    def __init__(self, parent, bg):
        self.widgets = []
        self.parent = parent
        self.app = parent
        self.bg = bg
        self.x, self.y = 0, 0

    def getModule(self, widget_type):
        if widget_type in _WIDGET_CACHE:
            return _WIDGET_CACHE[widget_type]

        module_path, cls_name = widget_type.rsplit('.', 1)

        cls = getattr(importlib.import_module(module_path), cls_name)

        _WIDGET_CACHE[widget_type] = cls

        return cls

    def get_size(self):
        self.w, self.h = self.app.surface.get_size()
        return self.w, self.h

    def load_widgets(self, parent, widgets):
        for widget in widgets:
            cls = self.getModule(widget['type'])
            instance = cls(self.app, parent, widget.get('attributes', {}), widget.get('actions', {}))

            parent.addWidget(widget['name'], instance)

            if 'widgets' in widget:
                # has children
                self.load_widgets(instance, widget['widgets'])

    def sendEvent(self, event):
        if event.type in [MOUSEBUTTONUP, MOUSEBUTTONDOWN]:
            x, y = event.pos
            for widget in self.widgets:
                if widget.inside(x, y):
                    widget.getEvent(event)


class App(object):
    def __init__(self):
        self.ev_loop = asyncio.get_event_loop()

        self.loaded_views = []
        self.view_objects = []
        self.active_view = None

    def init_pygame(self):
        pygame.display.init()
        pygame.font.init()

        pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.DOUBLEBUF)

        self.fonts = {}

        self.surface = pygame.display.get_surface()

        self.request_update = False

        if DEBUG:
            print("SDL: ", pygame.get_sdl_version())

    def load_font(self, font, size):
        if (font, size) not in self.fonts:
            font_path = pygame.font.match_font(font)
            if font_path is not None:
                if DEBUG:
                    print("Font loaded (%s, %s): %s" % (font, size, font_path))
                self.fonts[(font, size)] = pygame.font.Font(font_path, size)
                return self.fonts[(font, size)]
            elif DEBUG:
                print("Font not found (%s, %s): %s" % (font, size, font_path))

        else:
            return self.fonts[(font, size)]

    def makeColor(self, r, g, b):
        return pygame.Color(r, g, b)

    def load_views(self):
        for view, conf_file in self.views.items():
            config = yaml.load(open(conf_file))

            view = config.get('view')
            if view:
                if view['name'] in self.loaded_views:
                    raise Exception('Duplicate View: %s already loaded' % view['name'])

                view_obj = View(self, self.makeColor(*view.get('background', [0, 0, 0])))
                view_obj.load_widgets(view_obj, view.get('widgets', []))

                setattr(self, view['name'], view_obj)

                self.loaded_views.append(view['name'])
                self.view_objects.append(view_obj)

        self.active_view = self.view_objects[0]

    def draw(self):
        for view in self.view_objects:
            view.draw_widget(self.surface)

    async def main_loop(self):
        self.running = True
        self.draw()
        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                if DEBUG:
                    print(event)
                if event.type is QUIT:
                    self.running = False
                self.active_view.sendEvent(event)

            if self.request_update:
                self.draw()
                self.request_update = False
                pygame.display.flip()

            await asyncio.sleep(0.04)

        self.ev_loop.stop()

    def stop(self):
        self.running = False

    def run(self):
        self.init_pygame()

        self.load_views()

        self.ev_loop.run_until_complete(self.main_loop())
        self.ev_loop.run_forever()

