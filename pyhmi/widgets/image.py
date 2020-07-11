import pygame

from .base import Widget


class Image(Widget):
    def __init__(self, *a, **kw):
        Widget.__init__(self, *a, **kw)

        self.image_surf = pygame.image.load(self.filename)
        self.w, self.h = self.image_surf.get_size()

    def draw(self, surface):
        surface.blit(self.image_surf, (0, 0))
