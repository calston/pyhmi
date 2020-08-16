import pygame
from pygame.locals import * 

from .base import Widget

class LineChart(Widget):
    def __init__(self, *a, **kw):
        Widget.__init__(self, *a, **kw)

        if not hasattr(self, 'fill'):
            self.fill = (32, 32, 32)

        if not hasattr(self, 'border'):
            self.border = (254, 254, 254)

        if not hasattr(self, 'y_max'):
            self.y_max = None

        if not hasattr(self, 'y_min'):
            self.y_min = None

        if not hasattr(self, 'x_ticks'):
            self.x_ticks = 10

        self.selected_digit = -1

        self.data = []

    def update_data(self, data):
        self.data = data

        if self.y_max is None:
            self.dy_max = max((d[1] for d in self.data))
        else:
            self.dy_max = self.y_max

        if self.y_min is None:
            self.dy_min = min((d[1] for d in self.data))
        else:
            self.dy_min = self.y_min
        
        self.app.request_update = True

    def draw(self, surface):
        w, h = self.get_size()

        pygame.draw.rect(surface, pygame.Color(*self.fill),
                            (0, 0, w, h))

        pygame.draw.rect(surface, pygame.Color(*self.border),
                            (0, 0, w, h), 1)

        sx = 2
        x_width = w - 64
        y_height = h - 64
        border_c = pygame.Color(*self.border)
        pygame.draw.line(surface, border_c, (32, h-32), (w-32, h-32))
        pygame.draw.line(surface, border_c, (32, 32), (32, h-32))

        for i in range(self.x_ticks):
            x = (x_width/self.x_ticks) * (i+1)
            pygame.draw.line(surface, border_c, (32+x, h-32), (32+x, h-16))
            
        if len(self.data) > 1:
            x_min = self.data[0][0]
            x_max = self.data[-1][0]

            x_delta = x_max - x_min
            y_delta = self.dy_max - self.dy_min

            if (x_delta < 1) or (y_delta < 1):
                return

            last_rx = None
            last_ry = None
            for dx, dy in self.data:
                rx = round(((dx - x_min)/x_delta) * x_width)
                ry = round(((dy - self.dy_min)/y_delta) * y_height)
                
                if last_rx is None:
                    last_rx = rx
                    last_ry = ry
                else:
                    pygame.draw.line(surface, border_c, (32+last_rx, h-last_ry), (32+rx, h-ry))
                    last_rx = rx
                    last_ry = ry

    def _getKeyEvent(self, event):
        if event.type is pygame.KEYDOWN:
            pass

    def _getMouseEvent(self, event):
        if event.type is pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                selected = False
                abs_x, abs_y = self.get_abspos()

                if not selected:
                    self.selected_digit = -1
                    self.app.request_update = True

            elif (event.button == 4) and (self.selected_digit >= 0):
                self.inc_digit()

            elif (event.button == 5) and (self.selected_digit >= 0):
                self.dec_digit()
