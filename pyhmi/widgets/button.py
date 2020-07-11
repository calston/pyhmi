import pygame
from pygame.locals import * 

from .base import Widget

class Button(Widget):
    def __init__(self, *a, **kw):
        Widget.__init__(self, *a, **kw)

        if 'fill' not in self.attributes:
            self.fill = pygame.Color(32, 32, 32)

        self.hold = False

    def draw(self, surface):
        print(self.x, self.y, self.w, self.h)
        pygame.draw.rect(surface, pygame.Color(*self.fill),
            (0, 0, self.w, self.h))

        pygame.draw.rect(surface, pygame.Color(255, 255,255),
            (0, 0, self.w, self.h), 2)

        text = self.font.render(self.text, False, pygame.Color(255, 255,255))

        tw, th = self.font.size(self.text)

        surface.blit(text, ((self.w/2) - (tw/2), (self.h/2) - (th/2)))

    def getEvent(self, event):
        if event.type is MOUSEBUTTONDOWN:
            self.hold = True

        if (event.type is MOUSEBUTTONUP) and self.hold:
            self.on_click(self)

    def on_click(self, caller):
        pass
