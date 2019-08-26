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

