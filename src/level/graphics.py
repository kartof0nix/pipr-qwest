from src.graphics import tui_main
from src.level import Level, Field
from src.logic.player import PlayerClass
from src.level.textures import dynamicTexture, itemSquare, PlayerTexture
from src.common.event_queue import registerHandler, unregisterHandler
from src.level.controls import Control
# from urwid import Sizing, Widget, BigText, TextCanvas

import json
import urwid
import asyncio
import traceback
from typing import Dict, Iterator, List, Literal, Tuple
import logging
logger = logging.getLogger(__name__)
# Urwid.Widget



class fabric(urwid.Widget):
    _selectable=True
    _sizing = frozenset((urwid.BOX,))
    def _render(self, size : Tuple[int, int]):
        (x, y) = size
        char =  [['_' for j in range(y)] for i in range(x)]
        style =  [['bg' for j in range(y)] for i in range(x)]
        '''Pre-process rendering thy contents in seperate tabs char and style'''
        return(char, style)
    
    def render(self, size : tuple[int, int], focus: bool = False) -> urwid.TextCanvas:
        # logger.info("Start render %s", size)
        '''Render thy contents and return the result'''
        (y, x) = size # Urwid stores the coordinates swapped, so swap them back on integration
        (char, style) = self._render((x, y))
        # for dt in self.dynamic_textures:
        #     dt.apply_anim(char, style)
        attr = [[(style[i][j], len(bytes(char[i][j], 'UTF-8'))) for j in range(len(style[0]))] for i in range(len(style))]
        char = [bytes(''.join(i), 'UTF-8') for i in char]
        # result = [''.join([style[i][j] + char[i][j] for j in range(y)]) for i in range(x)]
        self._invalidate()
        return urwid.TextCanvas(char, attr=attr)

    # def add_dynamic_texture(self, dt : dynamicTexture):
    #     self.dynamic_textures.append(dt)
        
class fabricGrid(fabric):
    _selectable=True
    def init(self, level : Level, handlekey):
        _selectable=True
        self.handlekey = handlekey
        self.lastSize = (0, 0)
        self.playerTexture = PlayerTexture(level, (0, 0)) # Can't init player texture coz canva
        self.n = level.height
        self.m = level.width
        self.level = level
        self.grid = []
        for i in range(self.n):
            self.grid.append([])
            for j in range(self.m):
                a=level.getField(i, j)
                self.grid[i].append(itemSquare(a))
                self.grid[i][j].style = ["magenta", "cyan", "default"][(i+j)%3]
   
    def _render(self, size:Tuple[int, int]):
        (x, y) = size
        # logger.info("Render Grid %d x %d", x, y)
        if(self.lastSize != (x, y)):
            self.lastSize = (x, y)
            self.playerTexture.update(size, instant=True)
            #Re-size all dynamic textures and re-calculate 
        (char, style) = super()._render(size)
        for i in range(self.n):
            for j in range(self.m):
                x0 = x * i // self.n
                y0 = y * j // self.m
                x1 = x * (i+1) // self.n
                y1 = y * (j+1) // self.m
                # print(i, j, x0, y0, x1, y1)
                self.grid[i][j].apply((x0, y0), (x1-x0, y1-y0), char, style)
        self.playerTexture.apply_anim(char, style)
        return (char, style)        

    async def update(self, params=None):
        '''Update the screen (possibly with animations) based on current game state'''
        # logger.info("Updating screen...")
        self.playerTexture.update(self.lastSize)
        # logger.info("Finished updating screen...")
        
    def complete(self) -> bool:
        return self.playerTexture.pos == self.playerTexture.next_pos
    def keypress(self, size, key):
        if(self.complete() ):
            return self.handlekey(key)

class LevelView:
    async def loop(self):
        try:
            v=fabricGrid()
            self.controlModule = Control(self.level)
            v.init(self.level, self.controlModule.handleKey)
            tui_main.view.bottom = v
            tui_main.loop.draw_screen()
            registerHandler("move", v.update)
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())

        while True:
            await asyncio.sleep(1)
    def __init__(self, level : Level):
        self.level = level
        self.task = tui_main.aloop.create_task(self.loop())
    def __del__(self):
        self.task.cancel()
        del self.task
        