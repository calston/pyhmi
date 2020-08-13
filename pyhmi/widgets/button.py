import pygame
from pygame.locals import * 

from .base import Widget

class Button(Widget):
    def __init__(self, *a, **kw):
        Widget.__init__(self, *a, **kw)

        if 'fill' not in self.attributes:
            self.fill = (32, 32, 32)

        self.hold = False

    def draw(self, surface):
        w, h = self.get_size()
        pygame.draw.rect(surface, pygame.Color(*self.fill),
            (0, 0, w, h))

        pygame.draw.rect(surface, pygame.Color(255, 255,255),
            (0, 0, w, h), 2)

        text = self.font.render(self.text, self.app.antialias,
                                pygame.Color(*self.font_color))

        tw, th = self.font.size(self.text)

        surface.blit(text, ((w/2) - (tw/2), (h/2) - (th/2)))

    def getMouseEvent(self, event):
        if event.type is MOUSEBUTTONDOWN:
            self.hold = True

        if (event.type is MOUSEBUTTONUP) and self.hold:
            self.on_click(self)

    def on_click(self, caller):
        pass
