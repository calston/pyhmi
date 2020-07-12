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
            if 'color' in self.font:
                self.font_color = self.font['color']
            else:
                self.font_color = (255, 255, 255)

            self.font = self.app.load_font(self.font['name'], int(self.font['size']))

    def addWidget(self, name, child):
        self.widgets.append(child)
        setattr(self, name, child)

    def get_size(self, expand=0):
        return self.w+expand, self.h+expand

    def draw_widget(self, surface):
        # surface is 1px bigger to account for 0 base position
        this_surface = pygame.Surface(self.get_size(1), pygame.SRCALPHA)

        self.draw(this_surface)

        for widget in self.widgets:
           widget.draw_widget(this_surface)

        surface.blit(this_surface, self.get_relpos())

    def draw(self, surface):
        pass

    def get_relpos(self):
        x = self.x
        y = self.y

        if x < 0:
            # Snap from right
            pw, _ = self.parent.get_size()
            x += pw
        if y < 0:
            # Snap from bottom
            _, ph = self.parent.get_size()
            y += ph

        return x, y

    def get_abspos(self):
        x, y = self.get_relpos()
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
