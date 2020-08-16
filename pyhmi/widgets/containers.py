import pygame

from .base import Widget

class Group(Widget):
    def __init__(self, *a, **kw):
        Widget.__init__(self, *a, **kw)

        if 'fill' not in self.attributes:
            self.fill = (32, 32, 32)

        if 'border' not in self.attributes:
            self.border = (255, 255, 255)

    def draw(self, surface):
        text = self.font.render(self.text, self.app.antialias, pygame.Color(*self.font_color))

        tw, th = self.font.size(self.text)
        w, h = self.get_size()
        
        margin = self.attributes.get('margin', th//2)

        color = pygame.Color(*self.border)
        pygame.draw.rect(surface, pygame.Color(*self.fill), (0, 0, w, h))

        pygame.draw.lines(surface, color, False, (
            (margin, th//2),
            (0, th//2),
            (0, h),
            (w, h),
            (w, th//2),
            (margin+th+tw, th//2)
        ))

        surface.blit(text, (margin + (th//2), 0))
