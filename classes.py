import pygame as pg

pg.init()
WHITE = pg.Color('white')
BLACK = pg.Color('black')


class UserInfo:
    def __init__(self, waves, lives, coins):
        self.waves = waves
        self.lives = lives
        self.coins = coins
        self.wave = 0

    def next_wave(self):
        if self.wave + 1 <= self.waves:
            self.wave += 1
            return True
        return False


class Levels:
    def __init__(self, grid):
        self.grid = grid
        # Define levels in the form: [spacing, spacing_length, pos, next_tile, (speed, health), (speed, health), ...
        self.wave1 = [3, 2, (self.grid.start[0] - 1, self.grid.start[1]), self.grid.start, (1, 100), (1, 100), (1, 100), (2, 200), (2, 200), (2, 200), (3, 300), (3, 300), (3, 300), (4, 400), (4, 400), (4, 400)]
        self.wave2 = [4, 1.8, (self.grid.start[0] - 1, self.grid.start[1]), self.grid.start, (1, 100), (1, 100), (1, 100), (2, 200), (2, 200), (2, 200), (3, 300), (3, 300), (3, 300), (4, 400), (4, 400), (4, 400)]
        self.wave3 = [5, 1.6, (self.grid.start[0] - 1, self.grid.start[1]), self.grid.start, (1, 100), (1, 100), (1, 100), (2, 200), (2, 200), (2, 200), (3, 300), (3, 300), (3, 300), (4, 400), (4, 400), (4, 400)]

        self.levels = [self.wave1, self.wave2, self.wave3]


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


class SquareGrid:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.walls = []
        self.connections = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.path = {}
        self.start = None
        self.end = None

    def in_bounds(self, node):
        return 0 <= node[0] < self.w and 0 <= node[1] < self.h

    def check_walls(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = []
        for connection in self.connections:
            neighbor = (node[0] + connection[0], node[1] + connection[1])
            neighbors.append(neighbor)
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.check_walls, neighbors)
        return list(neighbors)
