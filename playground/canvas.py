
from colorama import Fore, Back, Style
from grid import item_square, AIM
import os

from random import randint


class canvas:

    def resize(s, x, y):
        s._x = x
        s._y = y
        s.char =  [[' ' for j in range(y)] for i in range(x)]
        s.style =  [['' for j in range(y)] for i in range(x)]

    def __init__(self, x, y):
        self.resize(x, y)

    def print(self):

        for i in range(self._x):
            for j in range(self._y):
                print(self.style[i][j] + self.char[i][j], end="")
            print()

class canvas_grid(canvas):

    def __init__(s, x, y, n, m):
        super().__init__(x, y)
        s._n = n
        s._m = m
        s.grid = []
        for i in range(n):
            s.grid.append([])
            for j in range(m):
                x0 = s._x * i // n
                y0 = s._y * j // m
                x1 = s._x * (i+1) // n
                y1 = s._y * (j+1) // m
                s.grid[i].append(item_square(x0, y0, x1-x0, y1-y0))
                s.grid[i][j].foreground = [Fore.CYAN, Fore.MAGENTA, Fore.WHITE][(i+j)%3]
   
    def random_maze(s):
        q = randint ( int( (s._n + s._m) * 2.7) , int( (s._n + s._m) * 4.3) )
        for i in range(q):
            i, j = randint(0, s._n-2), randint(0, s._m-2)
            k = randint(0, 1)
            s.grid[i][j].paths[k]=1   
            s.grid [ i + AIM[k][0] ][ j + AIM[k][1] ].paths[k+2]=1   

    def draw(s):
        for i in s.grid:
            for j in i:
                j.draw(s.char, s.style)

global a
a=None
if __name__ == "__main__":
    while(True):
        a, b = input().split(' ')
        a=int(a)
        b=int(b)
        size = os.get_terminal_size()
        a = canvas_grid(size.lines, size.columns, a, b)
        a.random_maze()
        a.draw()
        a.print()
            



