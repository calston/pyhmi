import pygame

class Widget(object):
    def __init__(self, app, parent, attributes, actions):
        self.widgets = []
        self.parent = parent
        self.app = app
        self.attributes = attributes
        self.actions = actions
        for attribute, value in attributes.items():
            setattr(self, attribute, value)

        for action, value in actions.items():
            try:
                if value.startswith('self.'):
                    setattr(self, action, getattr(self.app, value))
                elif hasattr(self.app, value):
                    setattr(self, action, getattr(self.app, value))
                else:
                    module_path, method_name = value.rsplit('.', 1)
                    method  = getattr(importlib.import_module(module_path), method_name)
            except Exception as e:
                raise Exception("Unable to resolve %s=%s" % (action, value))

        if 'font' in attributes:
            self.font = self.app.load_font(self.font['name'], int(self.font['size']))

    def addWidget(self, name, child):
        self.widgets.append(child)
        setattr(self, name, child)

    def get_size(self):
        return self.w, self.h

    def draw_widget(self, surface):
        this_surface = pygame.Surface(self.get_size())

        self.draw(this_surface)

        for widget in self.widgets:
           widget.draw_widget(this_surface)

        surface.blit(this_surface, (self.x, self.y))

    def draw(self, surface):
        pass

    def get_abspos(self):
        x = self.x
        y = self.y
        if hasattr(self.parent, 'x'):
            p_x, p_y = self.parent.get_abspos()
            x += p_x
            y += p_y

        return (x, y)

    def inside(self, x, y):
        x1, y1 = self.get_abspos()
        w, h = self.get_size()

        inx = (x > x1) and (x < (x1 + w))
        iny = (y > y1) and (y < (y1 + h))

        if inx and iny:
            return True
        else:
            return False

    def getEvent(self, event):
        pass
