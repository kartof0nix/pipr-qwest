from colorama import Fore, Back, Style
from item import item

AIM = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class item_square(item):

    def __init__(s, offset_x, offset_y, x, y):
        super().__init__(offset_x, offset_y, x, y)
        s.paths = [0 for i in range(4)]

    def sketch(s):
        grid = [[0 for i in range(3)] for j in range(3)]
        grid[1][1] = 1
        for i in range(4):
            grid[1 + AIM[i][0]][1 + AIM[i][1]] = s.paths[i]

        out = [''.join(['.' if grid[i*3//s.x][j*3//s.y]
                       else '#' for j in range(s.y)]) for i in range(s.x)]

        style = [[s.foreground for i in range(s.y)] for i in range(s.x)]
        return (out, style)


class map:
    def __init__(self, n, m):
        self.n = n
        self.m = m

        self.colour = [[Style.RESET_ALL for j in range(
            self.y)] for i in range(self.x)]
        self.char = [["." for j in range(self.y)] for i in range(self.x)]

        self.fields = [[]]

    def grid(self, x, y):
        for i in range(self.x):
            for j in range(self.y):
                c = (((i*self.n) // self.x) + ((j * self.m) // self.y)) % 3
                self.colour[i][j] = [Fore.CYAN, Fore.MAGENTA, Fore.WHITE][c]


"""
Opis słowny modułów.

Nie piszemy dokumentacji w kodzie.

Testy są wymagane.
"""
