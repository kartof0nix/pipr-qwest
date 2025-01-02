from src.graphics import main as tui_main
from src.level import Level
# from urwid import Sizing, Widget, BigText, TextCanvas


import asyncio
import urwid
import traceback
from typing import Dict, Iterator, List, Literal
import logging
logger = logging.getLogger(__name__)
# Urwid.Widget
TRANSPARENT = None
AIM_LABEL=['right', 'down', 'left', 'up']
AIM = [(0, 1), (1, 0), (0, -1), (-1, 0)]
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
        clr = [[s.style for i in range(y)] for j in range(x)]
        return (grid, clr)
    
    def apply(s, off_x, off_y, x, y, char, style):
        '''Apply the rendered item on canvas (char, style) with offset'''
        (grid, stl) = s.sketch(x, y)
        for i in range (x):
            for j in range (y):

                if(grid[i][j] != TRANSPARENT):
                    char[i + off_x][j + off_y] = grid[i][j]
                if(style[i][j] != ''):
                    style[i + off_x][j + off_y] = stl[i][j]

class item_square(item):

    def __init__(s, neighbours:Dict[str, bool]):
        # super().__init__()
        logger.info("r")
        s.paths = [bool(i in neighbours) for i in AIM_LABEL]
        logger.debug("Ngb : %s", s.paths )
        # s.paths = paths
    

    def sketch(s, x, y):
        grid = [[0 for i in range(3)] for j in range(3)]
        grid[1][1]=1
        for i in range(4):
            grid[1 + AIM[i][0] ][ 1 + AIM[i][1] ] = s.paths[i]

        out = [''.join(['.' if grid[i*3//x][j*3//y] else '#' for j in range(y)]) for i in range(x)]

        style = [[s.style for i in range(y)] for i in range(x)]
        return (out, style)


class fabric(urwid.Widget):

    _sizing = frozenset((urwid.BOX,))
    def _render(self, x, y):
        char =  [['_' for j in range(y)] for i in range(x)]
        style =  [['bg' for j in range(y)] for i in range(x)]
        '''Pre-process rendering thy contents in seperate tabs char and style'''
        return(char, style)
    
    def render(self, size : tuple[int, int], focus: bool = False) -> urwid.TextCanvas:
        logger.info("Start render")
        '''Render thy contents and return the result'''
        (y, x) = size
        (char, style) = self._render(x, y)
        char = [bytes(''.join(i), 'UTF-8') for i in char]
        # result = [''.join([style[i][j] + char[i][j] for j in range(y)]) for i in range(x)]
        return urwid.TextCanvas(char, attr=[[(style[i][j], 1) for j in range(len(style[0]))] for i in range(len(style))])

class fabricGrid(fabric):
    def init(self, level : Level):
        self.n = level.height
        self.m = level.width
        self.level = level
        self.grid = []
        logger.info("t")
        for i in range(self.n):
            self.grid.append([])
            logger.info("p")
            for j in range(self.m):
                logger.info("q")
                a=level.getField(i, j).neighbours
                logger.info("o")
                self.grid[i].append(item_square(a))
                logger.info("r")
                self.grid[i][j].style = ["magenta", "cyan", ""][(i+j)%3]
   
    def _render(s, x, y):
        (char, style) = super()._render(x, y)
        for i in range(s.n):
            for j in range(s.m):
                x0 = x * i // s.n
                y0 = y * j // s.m
                x1 = x * (i+1) // s.n
                y1 = y * (j+1) // s.m
                # print(i, j, x0, y0, x1, y1)
                s.grid[i][j].apply(x0, y0, x1-x0, y1-y0, char, style)
        return (char, style)        



class LevelView:
    
    async def loop(self):
        try:
            logger.info("p1")
            v=fabricGrid()
            v.init(self.level)
            logger.info("p3")
            tui_main.view.bottom = v
            tui_main.loop.draw_screen()
            
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())

        while True:
            await asyncio.sleep(1)
    def __init__(self, level : Level):
        logger.info("p0")
        self.level = level
        self.task = tui_main.aloop.create_task(self.loop())
    def __del__(self):
        self.task.cancel()
        del self.task
        