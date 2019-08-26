class Levels:
    def __init__(self, grid):
        self.grid = grid
        # Define levels in the form: [spacing, spacing_length, pos, next_tile, (speed, health), (speed, health), ...
        self.wave1 = [3, 2, (self.grid.start[0] - 1, self.grid.start[1]), self.grid.start, (1, 100), (1, 100), (1, 100), (2, 200), (2, 200), (2, 200), (3, 300), (3, 300), (3, 300), (4, 400), (4, 400), (4, 400)]
        self.wave2 = [4, 1.8, (self.grid.start[0] - 1, self.grid.start[1]), self.grid.start, (1, 100), (1, 100), (1, 100), (2, 200), (2, 200), (2, 200), (3, 300), (3, 300), (3, 300), (4, 400), (4, 400), (4, 400)]
        self.wave3 = [5, 1.6, (self.grid.start[0] - 1, self.grid.start[1]), self.grid.start, (1, 100), (1, 100), (1, 100), (2, 200), (2, 200), (2, 200), (3, 300), (3, 300), (3, 300), (4, 400), (4, 400), (4, 400)]

        self.levels = [self.wave1, self.wave2, self.wave3]
