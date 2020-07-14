import pygame

from .base import Widget

class Text(Widget):
    def __init__(self, *a, **kw):
        Widget.__init__(self, *a, **kw)

    def get_size(self, expand=0):
        return self.font.size(self.text)

    def draw(self, surface):
        text = self.font.render(self.text, self.app.antialias, pygame.Color(*self.font_color))
        surface.blit(text, (0, 0))
