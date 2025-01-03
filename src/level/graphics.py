from src.graphics import main as tui_main
from src.level import Level, Field
# from urwid import Sizing, Widget, BigText, TextCanvas

from random import shuffle
from pathlib import Path
import json
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
        style = [[s.style for i in range(y)] for j in range(x)]
        return (grid, style)
    
    def apply(s, off_x, off_y, x, y, char, style):
        '''Apply the rendered item on canvas (char, style) with offset'''
        (grid, stl) = s.sketch(x, y)
        for i in range (x):
            for j in range (y):

                if(grid[i][j] != TRANSPARENT):
                    char[i + off_x][j + off_y] = grid[i][j]
                if(stl[i][j] != ''):
                    style[i + off_x][j + off_y] = stl[i][j]

class texture(item):
    TEXTURE_PATH=Path("res/texture").expanduser()
    def __init__(self, filename:str):
        logger.info("Creating texture %s", filename)
        try:
            with open(self.TEXTURE_PATH.joinpath(filename), "r") as f:
                data = json.load(f)
            self.attrmap = data['attrmap']
            self.textures = data['textutes']
        except Exception as e:
            logger.error("Failed to load file: %s", e)
    def sketch(self, x, y):
        (grid, style) = super().sketch(x, y)
        # Find the texture approieate for thy size
        best = "0x0"
        for t in self.textures:
            (tx, ty) = t.split("x")
            (bx, by) = best.split("x")
            (tx, ty) = (int(tx), int(ty))
            (bx, by) = (int(bx), int(by))
            if(tx <= x and ty <= y and tx+ty >= bx+by):
                best=t
        (tx, ty) = best.split("x")
        (tx, ty) = (int(tx), int(ty))
        tex = self.textures[best]
        # Find middle of drawing area
        x0 = int((x - tx)/2)
        y0 = int((y - ty)/2)
        #Apply appropieate texture
        for i in range(tx):
            for j in range(ty):
                grid[i+x0][j+y0] = tex[0][i][j]
                style[i+x0][j+y0] = self.attrmap[tex[1][i][j]]
        logger.warn("Apply: %s, %s", grid, style)
        return(grid, style)
            
            
        # super().__init__()
class item_square(item):

    def __init__(s, field : Field):
        # super().__init__()
        s.field = field
        s.paths = [bool(i in field.neighbours) for i in AIM_LABEL]
        # s.paths = paths
        s.used_tiles = []

    def sketch(s, x, y):
        grid = [[0 for i in range(3)] for j in range(3)]
        grid[1][1]=1
        for i in range(4):
            grid[1 + AIM[i][0] ][ 1 + AIM[i][1] ] = s.paths[i]

        out = [['.' if grid[i*3//x][j*3//y] else '#' for j in range(y)] for i in range(x)]

        style = [[s.style for i in range(y)] for i in range(x)]
        available_tiles = [(i, j) if not grid[i][j] and (i, j) not in s.used_tiles  else None for j in range(3) for i in range(3)] 
        while None in available_tiles:
            available_tiles.remove(None)
        shuffle(available_tiles)
        shuffle(available_tiles)
        tile_queue = s.used_tiles + available_tiles
        s.used_tiles=[]
        # logger.info(available_tiles)
        for it in s.field.items:
            
            poz = tile_queue[0]
            tile_queue.remove(poz)
            s.used_tiles += [poz]
            tex = texture(it+".json")
            logger.info("Showing texture on %s", str(poz))
            def calc(n:int, poz:int): return int((n//3)*poz + min(n%3, poz))
            (x0, y0) = (calc(x, poz[0]), calc(y, poz[1]))
            (x1, y1) = (calc(x, poz[0]+1), calc(y, poz[1]+1))
            logger.debug("Properties : (%d, %d) (%d, %d) (%d, %d)", x, y, x0, y0, x1, y1)
            tex.apply(x0, y0, x1-x0, y1-y0, out, style)
        return (out, style)


class fabric(urwid.Widget):

    _sizing = frozenset((urwid.BOX,))
    def _render(self, x, y):
        char =  [['_' for j in range(y)] for i in range(x)]
        style =  [['bg' for j in range(y)] for i in range(x)]
        '''Pre-process rendering thy contents in seperate tabs char and style'''
        return(char, style)
    
    def render(self, size : tuple[int, int], focus: bool = False) -> urwid.TextCanvas:
        logger.info("Start render %s", size)
        '''Render thy contents and return the result'''
        (y, x) = size
        (char, style) = self._render(x, y)
        attr = [[(style[i][j], len(bytes(char[i][j], 'UTF-8'))) for j in range(len(style[0]))] for i in range(len(style))]
        char = [bytes(''.join(i), 'UTF-8') for i in char]
        # result = [''.join([style[i][j] + char[i][j] for j in range(y)]) for i in range(x)]
        return urwid.TextCanvas(char, attr=attr)

class fabricGrid(fabric):
    def init(self, level : Level):
        self.n = level.height
        self.m = level.width
        self.level = level
        self.grid = []
        for i in range(self.n):
            self.grid.append([])
            for j in range(self.m):
                a=level.getField(i, j)
                self.grid[i].append(item_square(a))
                self.grid[i][j].style = ["magenta", "cyan", "default"][(i+j)%3]
   
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
            v=fabricGrid()
            v.init(self.level)
            tui_main.view.bottom = v
            tui_main.loop.draw_screen()
            await asyncio.sleep(4)
            tui_main.add_frame(urwid.Text("£"), 1, 1, 'left')
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
        