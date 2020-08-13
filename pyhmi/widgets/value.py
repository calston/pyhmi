import pygame
from pygame.locals import * 

from .base import Widget

class SelectablePrecisionValue(Widget):
    def __init__(self, *a, **kw):
        Widget.__init__(self, *a, **kw)

        if not hasattr(self, 'value'):
            self.value = 0

        if not hasattr(self, 'format'):
            self.format = "%d"

        if not hasattr(self, 'max_value'):
            self.max_value = -1

        if not hasattr(self, 'min_value'):
            self.min_value = 0

        self.selected_digit = -1

        self.update_bounds()

    def get_size(self, expand=0):
        return self.font.size(self.format % self.value)

    def update_bounds(self):
        s = self.format % self.value
        
        boxes = []
        offset = 0
        digits = 0
        decimals = False

        for c in s:
            w, h = self.font.size(c)
            if c is '.':
                decimals = 0
            if c.isdigit():
                if decimals is False:
                    digits += 1
                else:
                    decimals += 1
                boxes.append((offset, 0, w, h))
            offset += w
        multiplier = []
        for i in range(digits):
            multiplier.append(10**(digits - i - 1))
        for i in range(decimals):
            multiplier.append(1/(10**(i+1)))

        self.decimals, self.digits = decimals, digits
        self.bounds = boxes
        self.multipliers = multiplier

    def draw(self, surface):
        text = self.font.render(self.format % self.value, self.app.antialias,
                                pygame.Color(*self.font_color))
        surface.blit(text, (0, 0))
        
        if self.selected_digit >= 0:
            x, y, w, h = self.bounds[self.selected_digit]
            pygame.draw.line(surface, pygame.Color(*self.font_color), (x, h-2), (x+w, h-2), 2)

    def inc_digit(self):
        v = self.value + self.multipliers[self.selected_digit]
        if not ((self.max_value >= 0) and (v > self.max_value)):
            self.value = v
            self.app.request_update = True
            self.on_change(self)

    def dec_digit(self):
        v = self.value - self.multipliers[self.selected_digit]
        if v >= self.min_value:
            self.value = v
            self.app.request_update = True
            self.on_change(self)

    def get_digit(self, i):
        if self.decimals:
            v = int(self.value * (10**self.decimals))
        else:
            v = int(self.value)

        f = "%%0%dd" % (self.digits+self.decimals)
        s = (f % v)
        return int(s[i])
    
    def set_digit(self, d):
        digit = self.get_digit(self.selected_digit)
        multiplier = self.multipliers[self.selected_digit]
        self.value = self.value - (digit * multiplier) + (d * multiplier)
        self.on_change(self)

    def on_change(self, caller):
        pass

    def getKeyEvent(self, event):
        if event.type is pygame.KEYDOWN:
            if event.key == 273:
                self.inc_digit()
                self.on_change(self)
            elif event.key == 274:
                self.dec_digit()
                self.on_change(self)
            elif event.key == 275:
                if self.selected_digit < (len(self.bounds)-1):
                    self.selected_digit += 1
                    self.app.request_update = True
            elif event.key == 276:
                if self.selected_digit > 0:
                    self.selected_digit -= 1
                    self.app.request_update = True
            elif event.unicode.isdigit():
                self.set_digit(int(event.unicode))
                if self.selected_digit < (len(self.bounds)-1):
                    self.selected_digit += 1
                self.app.request_update = True
                self.on_change(self)

    def getMouseEvent(self, event):
        if event.type is pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                selected = False
                abs_x, abs_y = self.get_abspos()

                for i, b in enumerate(self.bounds):
                    x1, y1, w, h = b
                    x1 += abs_x
                    y1 += abs_y
                    inx = (x > x1) and (x < (x1 + w))
                    iny = (y > y1) and (y < (y1 + h))
                    if inx and iny:
                        self.selected_digit = i
                        selected = True
                        self.app.request_update = True

                if not selected:
                    self.selected_digit = -1
                    self.app.request_update = True

            elif (event.button == 4) and (self.selected_digit >= 0):
                self.inc_digit()
                self.on_change(self)

            elif (event.button == 5) and (self.selected_digit >= 0):
                self.dec_digit()
                self.on_change(self)
