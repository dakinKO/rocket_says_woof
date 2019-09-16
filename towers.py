import pygame as pg
BROWN = pg.Color('brown1')
GREEN = pg.Color('green4')
SCREEN_WIDTH = 1440
TILE_SIZE = int(SCREEN_WIDTH / 54)


class Towers(pg.sprite.Sprite):
    def __init__(self, function_str, pos, active):
        super().__init__()
        self.name = function_str
        self.pos = pos
        self.active = active
        self.color = None
        self.rect = pg.Rect(pos, (TILE_SIZE, TILE_SIZE))
        self.cost = None
        self.speed = None
        self.damage = None
        self.range = None
        self.in_range = []
        # Run function to set attributes
        exec('self.' + function_str + '()')
        self.counter = 0
        # noinspection PyTypeChecker
        self.wait_time = (2 - self.speed / 10)

    def draw(self, surface):
        self.rect = pg.Rect(self.pos, (TILE_SIZE, TILE_SIZE))
        pg.draw.rect(surface, self.color, self.rect)

    def dart(self):
        self.color = BROWN
        self.cost = 200
        self.speed = 8
        self.damage = 10
        self.range = 5

    def sniper(self):
        self.color = GREEN
        self.cost = 500
        self.speed = -20
        self.damage = 20
        self.range = 30
