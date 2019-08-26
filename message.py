import pygame as pg
pg.init()
WHITE = pg.Color('white')
BLACK = pg.Color('black')


class Message:
    def __init__(self, surface, pos, text, font=pg.font.SysFont('comicsansms', 20), bg_color=WHITE, txt_color=BLACK):
        self.surface = surface
        self.pos = pos
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.txt_color = txt_color
        self.rect = None
        self.img = None
        self.prep_img()

    def prep_img(self):
        self.img = self.font.render(self.text, True, self.txt_color, self.bg_color)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def blit(self):
        self.surface.blit(self.img, self.rect)
