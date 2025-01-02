
# from colorama import Fore, Back, Style
from grid import  AIM
from item import TRANSPARENT
import os

from random import randint

class item:
    '''Item to be drawn on canvas'''
    style = ''
    # def resize(s):
    #     s.x = x
    #     s.y = y
    #     s.off_x = offset_x
    #     s.off_y = offset_y
    # def __init__(s, offset_x, offset_y, x, y):
    #     s.resize(offset_x, offset_y, x, y)


    def sketch(s, x, y):
        '''Sketch the item with size (x, y)'''
        grid = [[None for i in range(y)] for j in range(x)]
        clr = [[s.foreground for i in range(y)] for j in range(x)]
        return (grid, clr)
    
    def apply(s, off_x, off_y, x, y, char, style):
        '''Apply the rendered item on canvas (char, style) with offset'''
        (grid, stl) = s.sketch(x, y)
        for i in range (x):
            for j in range (y):

                if(grid[i][j] != TRANSPARENT):
                    char[i + off_x][j + off_y] = grid[i][j]
                if(style[i][j] != ""):
                    style[i + off_x][j + off_y] += stl[i][j]

class item_square(item):

    def __init__(s):
        super().__init__()
        s.paths = [0 for i in range(4)]
    

    def sketch(s, x, y):
        grid = [[0 for i in range(3)] for j in range(3)]
        grid[1][1]=1
        for i in range(4):
            grid[1 + AIM[i][0] ][ 1 + AIM[i][1] ] = s.paths[i]

        out = [''.join(['.' if grid[i*3//x][j*3//y] else '#' for j in range(y)]) for i in range(x)]

        style = [[s.style for i in range(y)] for i in range(x)]
        return (out, style)

class canvas:
    '''
    My custom canvas to support transparent overlay of static layers
    '''
    # def resize(s, x, y):
    #     # s._x = x
    #     # s._y = y
    #     s.char =  [[' ' for j in range(y)] for i in range(x)]
    #     s.style =  [['' for j in range(y)] for i in range(x)]

    def __init__(self):
        # self.resize(x, y)
        pass

    def _render(self, x, y):
        char =  [['_' for j in range(y)] for i in range(x)]
        style =  [['' for j in range(y)] for i in range(x)]
        '''Pre-process rendering thy contents in seperate tabs char and style'''
        return(char, style)
    def render(self, size : tuple[int, int], focus: bool = False):
        '''Render thy contents and return the result'''
        (y, x) = size
        (char, style) = self._render(x, y)
        result = [[style[i][j] + char[i][j] for j in range(y)] for i in range(x)]
        for i in range(x):
            print(''.join(result[i]))

class canvas_grid(canvas):

    def __init__(s, n, m):
        s._n = n
        s._m = m
        s.grid = []
        for i in range(n):
            s.grid.append([])
            for j in range(m):
                s.grid[i].append(item_square())
                s.grid[i][j].style = ["banner", "outside", "bg"][(i+j)%3]
   
    def _render(s, x, y):
        (char, style) = super()._render(x, y)
        for i in range(s._n):
            for j in range(s._m):
                x0 = x * i // s._n
                y0 = y * j // s._m
                x1 = x * (i+1) // s._n
                y1 = y * (j+1) // s._m
                print(i, j, x0, y0, x1, y1)
                s.grid[i][j].apply(x0, y0, x1-x0, y1-y0, char, style)
        return (char, style)        

global a
a=None
if __name__ == "__main__":
    while(True):
        a, b = input().split(' ')
        a=int(a)
        b=int(b)
        size = os.get_terminal_size()
        a = canvas_grid(a, b)
        a.render((size.columns, size.lines))
            



