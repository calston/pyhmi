import pygame

from .base import Widget

class Group(Widget):
    def draw(self, surface):
        text = self.font.render(self.text, False, pygame.Color(*self.font_color))

        tw, th = self.font.size(self.text)
        w, h = self.get_size()
        
        margin = self.attributes.get('margin', th//2)

        color = pygame.Color(*self.attributes.get('color', (255, 255, 255)))

        pygame.draw.lines(surface, color, False, (
            (margin, th//2),
            (0, th//2),
            (0, h),
            (w, h),
            (w, th//2),
            (margin+th+tw, th//2)
        ))

        surface.blit(text, (margin + (th//2), 0))
