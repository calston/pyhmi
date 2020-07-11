
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

    def draw_widget(self, surface):
        self.draw(surface)
        for widget in self.widgets:
           widget.draw_widget(surface)

    def draw(self, surface):
        pass

    def inside(self, x, y):
        if not hasattr(self, 'w'):
            return False

        inx = (x > self.x) and (x < (self.x+self.w))
        iny = (y > self.y) and (y < (self.y+self.h))

        if inx and iny:
            return True
        else:
            return False

    def getEvent(self, event):
        pass
