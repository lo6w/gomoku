import random


class nb_AI_1:
    board = []
    self_point = []
    player_point = []
    size = 0
    down_chess = []
    self_max_point = []
    player_max_point = []
    point1 = {
        (0, 0, 0, 0, 0): 0,
        (2, 0, 0, 0, 0): 0,
        (1, 2, 0, 0, 0): 4,
        (1, 1, 2, 0, 0): 8,
        (1, 0, 0, 0, 0): 32,
        (1, 1, 1, 2, 0): 48,
        (1, 1, 0, 0, 0): 64,
        (1, 1, 1, 0, 0): 96,
        (1, 1, 1, 1, 2): 128,
        (1, 1, 1, 1, 0): 128
    }
    point2 = {
        (0, 0, 0, 0, 0): 0,
        (1, 0, 0, 0, 0): 0,
        (2, 1, 0, 0, 0): 4,
        (2, 2, 1, 0, 0): 8,
        (2, 0, 0, 0, 0): 32,
        (2, 2, 2, 1, 0): 48,
        (2, 2, 0, 0, 0): 64,
        (2, 2, 2, 0, 0): 96,
        (2, 2, 2, 2, 1): 128,
        (2, 2, 2, 2, 0): 128
    }

    def __init__(self, size=16):
        self.size = size
        self.self_point = []
        self.player_point = []
        for i in range(self.size):
            self.self_point.append([0] * self.size)
            self.player_point.append([0] * self.size)

    def read(self, x, y):
        if x >= 16 or x < 0 or y >= 16 or y < 0:
            return None
        else:
            return self.board[y][x]

    def get_point(self, chess=1):
        max_point = 0
        points = []
        for x in range(self.size):
            for y in range(self.size):
                if chess in [self.read(x - 1, y - 1), self.read(x, y - 1), self.read(x + 1, y - 1),
                             self.read(x - 1, y), self.read(x + 1, y),
                             self.read(x - 1, y + 1), self.read(x, y + 1), self.read(x + 1, y + 1)] and self.board[y][x] == 0:
                    for x_add in range(3):
                        x_add = x_add - 1
                        for y_add in range(3):
                            y_add = y_add - 1
                            if not (x_add == 0 and y_add == 0):
                                line = [0, 0, 0, 0, 0]
                                for long in range(5):
                                    c = self.read(x + (long + 1) * x_add, y + (long + 1) * y_add)
                                    if c is not None:
                                        if c != 0:
                                            line[long] = c
                                        else:
                                            break
                                    else:
                                        break
                                f = (line[0], line[1], line[2], line[3], line[4])
                                if chess == 1 and f in self.point1:
                                    self.player_point[y][x] = self.player_point[y][x] + self.point1[f]
                                elif chess == 2 and f in self.point2:
                                    self.self_point[y][x] = self.self_point[y][x] + self.point2[f]
                    if chess == 1:
                        if max_point < self.player_point[y][x]:
                            max_point = self.player_point[y][x]
                            points = [[x, y]]
                        elif max_point == self.player_point[y][x]:
                            points.append([x, y])
                    elif chess == 2:
                        if max_point < self.self_point[y][x]:
                            max_point = self.self_point[y][x]
                            points = [[x, y]]
                        elif max_point == self.self_point[y][x]:
                            points.append([x, y])
        if len(points) == 1:
            p = points[0]
        elif len(points) > 1:
            p = points[random.randint(0, len(points) - 1)]
        else:
            p = None
        if chess == 1:
            self.player_max_point = [max_point, p]
        if chess == 2:
            self.self_max_point = [max_point, p]

    def get(self, board: list):
        self.board = board
        self.self_point.clear()
        self.player_point.clear()
        for i in range(self.size):
            self.self_point.append([0] * self.size)
            self.player_point.append([0] * self.size)
        self.get_point(1)
        self.get_point(2)
        if self.self_max_point[0]*0.8 > self.player_max_point[0]:
            self.board[self.self_max_point[1][1]][self.self_max_point[1][0]] = 2
        else:
            self.board[self.player_max_point[1][1]][self.player_max_point[1][0]] = 2
        self.get_point(1)
        self.get_point(2)
