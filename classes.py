import pygame as pg

pg.init()
WHITE = pg.Color('white')
BLACK = pg.Color('black')


class Menus:
    def __init__(self, surface, rect, color, towers):
        self.surface = surface
        self.rect = rect
        self.color = color
        # Towers needs to be a list of tuples in the form [(name, color, Rect, cost, damage, range), (name, color, Rect, cost, damage, range)]
        # Convert the given list into a dictionary
        self.towers = {}
        for tower in towers:
            self.towers[tower.name] = (tower.color, tower.rect, tower.cost, tower.damage, tower.range)

    def draw(self):
        pg.draw.rect(self.surface, self.color, self.rect)
        for tower in self.towers.items():
            specs = tower[1]
            pg.draw.rect(self.surface, specs[0], specs[1])
            name = Message(self.surface, (specs[1].left + 3, specs[1].centery + 3), (tower[0]), font=pg.font.SysFont('comicsansms', 12), bg_color=specs[0])
            cost = Message(self.surface, (specs[1].left + 5, specs[1].top + 5), str(specs[2]), font=pg.font.SysFont('comicsansms', 18), bg_color=specs[0])
            name.blit()
            cost.blit()


class UserInfo:
    def __init__(self, waves, lives, coins):
        self.waves = waves
        self.lives = lives
        self.coins = coins
        self.wave = 0
        self.start_wave = None

    def next_wave(self):
        if self.wave + 1 <= self.waves:
            return True
        return False


class Levels:
    def __init__(self, grid):
        self.grid = grid
        # Define levels in the form: [spacing, spacing_length, pos, next_tile, (speed, health), (speed, health), ...
        self.wave1 = [3, 2, (self.grid.start[0] - 1, self.grid.start[1]), self.grid.start, (1, 10), (1, 10), (1, 10),
                      (2, 20), (2, 20), (2, 20), (3, 30), (3, 30), (3, 30), (4, 40), (4, 40), (4, 40)]
        self.wave2 = [10, 4, (self.grid.start[0] - 1, self.grid.start[1]), self.grid.start, (2, 20), (2, 20), (2, 20),
                      (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (4, 40), (4, 40), (4, 40), (4, 40),
                      (4, 40), (4, 40)]
        self.wave3 = [3, 1.5, (self.grid.start[0] - 1, self.grid.start[1]), self.grid.start, (4, 40), (4, 40), (4, 40),
                      (4, 40), (4, 40), (4, 40), (4, 40), (4, 40), (4, 40), (4, 40), (4, 40), (4, 40)]
        self.wave4 = [20, 3, (self.grid.start[0] - 1, self.grid.start[1]), self.grid.start, (2, 20), (2, 20), (2, 20),
                      (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20),
                      (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20),
                      (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20),
                      (2, 20), (2, 20), (2, 20), (2, 20)]
        self.wave5 = [5, 3, (self.grid.start[0] - 1, self.grid.start[1]), self.grid.start, (2, 20), (2, 20), (2, 20),
                      (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20),
                      (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (2, 20),
                      (2, 20), (2, 20), (2, 20), (2, 20), (2, 20), (5, 50), (5, 50), (5, 50), (5, 50), (5, 50), (6, 60),
                      (6, 60), (6, 60), (6, 60), (6, 60)]

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
