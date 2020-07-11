import pygame

from .base import Widget

class Text(Widget):
    def __init__(self, *a, **kw):
        Widget.__init__(self, *a, **kw)

        if 'color' not in self.attributes:
            self.color = (255, 255, 255)

    def get_size(self):
        return self.font.size(self.text)

    def draw(self, surface):
        text = self.font.render(self.text, False, pygame.Color(*self.color))
        surface.blit(text, (0, 0))
