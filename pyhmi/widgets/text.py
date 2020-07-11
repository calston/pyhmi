import pygame

from .base import Widget

class Text(Widget):
    def __init__(self, *a, **kw):
        Widget.__init__(self, *a, **kw)

        if 'color' not in self.attributes:
            self.color = (255, 255, 255)

    def draw(self, surface):
        self.w, self.h = self.font.size(self.text)

        text = self.font.render(self.text, False, pygame.Color(*self.color))

        surface.blit(text, (self.x, self.y))

