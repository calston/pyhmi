import pygame

from .base import Widget

class SevenSegment(Widget):
    """
    A ridiculous way of displaying numbers on a TFT
    """
    charMap = {
        '0': (True,  True,  True,  True,  True,  True,  False),
        '1': (False, True,  True,  False, False, False, False),
        '2': (True,  True,  False, True,  True,  False, True),
        '3': (True,  True,  True,  True,  False, False, True),
        '4': (False, True,  True,  False, False, True,  True),
        '5': (True,  False, True,  True,  False, True,  True),
        '6': (True,  False, True,  True,  True,  True,  True),
        '7': (True,  True,  True,  False, False, False, False),
        '8': (True,  True,  True,  True,  True,  True,  True),
        '9': (True,  True,  True,  False, False, True,  True)
    }

    def __init__(self, *a, **kw):
        Widget.__init__(self, *a, **kw)

        if 'msd' not in self.attributes:
            self.msd = 1

        if 'value' not in self.attributes:
            self.value = 0

        if 'digits' not in self.attributes:
            self.digits = 1

        if 'padding' not in self.attributes:
            self.padding = 5

        if 'dark_color' not in self.attributes:
            self.dark_color = (32, 32, 32)

        if 'light_color' not in self.attributes:
            self.light_color = (0, 255, 0)

        self.construct_surface()

    def construct_surface(self):
        self.digit = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        
        self.dw = int((self.w / self.digits) - self.padding)

        dh = (self.h / 2) - self.padding

        bt = min(self.dw // 8, dh//5)
        self.bt = bt

        # Horizontal segment
        self.h_dark = pygame.Surface((self.dw - 2*bt, 2*bt), pygame.SRCALPHA)
        self.h_light = pygame.Surface((self.dw - 2*bt, 2*bt), pygame.SRCALPHA)

        h_shape = [
            (0, bt),
            (bt, 0),
            (self.dw - 3*bt, 0),
            (self.dw - 2*bt, bt),
            (self.dw - 3*bt, 2*bt),
            (bt, 2*bt)
        ]
        pygame.draw.polygon(self.h_dark, pygame.Color(*self.dark_color), h_shape)
        pygame.draw.polygon(self.h_light, pygame.Color(*self.light_color), h_shape)

        self.v_dark = pygame.Surface((2*bt, dh), pygame.SRCALPHA)
        self.v_light = pygame.Surface((2*bt, dh), pygame.SRCALPHA)

        v_shape = [
            (bt, 0),
            (2*bt, bt),
            (2*bt, dh - 3*bt),
            (bt, dh - 2*bt),
            (0, dh - 3*bt),
            (0, bt),
        ]
        pygame.draw.polygon(self.v_dark, pygame.Color(*self.dark_color), v_shape)
        pygame.draw.polygon(self.v_light, pygame.Color(*self.light_color), v_shape)

        for i in range(self.digits):
            x = (self.dw + self.padding) * i

            # Horizontal segments
            self.digit.blit(self.h_dark, (x+bt, 0))
            self.digit.blit(self.h_dark, (x+bt, (self.h/2) - bt))
            self.digit.blit(self.h_dark, (x+bt, self.h - 2*bt))

            # Vertical segments
            self.digit.blit(self.v_dark, (x, 2*bt))
            self.digit.blit(self.v_dark, (x+self.dw-2*bt, 2*bt))
            self.digit.blit(self.v_dark, (x, bt+self.h/2))
            self.digit.blit(self.v_dark, (x+self.dw-2*bt, bt+self.h/2))

    def lightSegments(self):
        panel = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        dst = (self.h_dark, self.h_light, self.v_dark, self.v_light)

        v = "%f" % self.value
        nd = len(v.split('.')[0])
        if nd < self.msd:
            v = '0'*(self.msd - nd) + v

        cn = 0
            
        for c in v:
            if cn >= self.digits:
                break

            if (c == '.') and (cn <= self.digits):
                pygame.draw.circle(panel, pygame.Color(*self.light_color), (x + self.dw + 2, self.h-self.bt), self.bt)
                continue

            if c in self.charMap:
                x = (self.dw + self.padding) * cn
                cn += 1
                segments = [
                    (0, (x+self.bt, 0)),
                    (2, (x+self.dw-2*self.bt, 2*self.bt)),
                    (2, (x+self.dw-2*self.bt, self.bt + self.h/2)),
                    (0, (x+self.bt, self.h - 2*self.bt)),
                    (2, (x, self.bt+self.h/2)),
                    (2, (x, 2*self.bt)),
                    (0, (x+self.bt, (self.h/2) - self.bt)),
                ]

                for i, s in enumerate(self.charMap[c]):
                    if s:
                        args = (dst[segments[i][0] + 1], segments[i][1])
                    else:
                        args = (dst[segments[i][0]], segments[i][1])

                    panel.blit(*args)

        return panel

    def draw(self, surface):
        if self.digit:
            surface.blit(self.digit, (0, 0))
            surface.blit(self.lightSegments(), (0, 0))
