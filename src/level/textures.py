
from src.common.config import Setting, registered_settings
from src.level import Level, Field
from src.graphics import tui_main as tui_main
from src.logic import player

from time import time
from pathlib import Path
from typing import Dict, Iterator, List, Literal, Tuple

from math import ceil
import json
import urwid
import asyncio

import logging
logger = logging.getLogger(__name__)
# Urwid.Widget

from random import shuffle
import random


TRANSPARENT = "\t"
AIM_LABEL=['right', 'down', 'left', 'up']
AIM = [(0, 1), (1, 0), (0, -1), (-1, 0)]

cfg = Setting(
    name="Level graphics",
    defaultValues={
        "anim speed": 1.0,
        "theme":"default"
    },
    constrains={
        "anim speed":{
            "type" : float,
            "value_type" : "bound",
            "min_val" : 0,
            "max_val" : 5
        },
        "theme":{
            "type" : str,
            "value_type" : "selectable",
            "selectable" : ["default", "forest"]
        }
    }
)
registered_settings += [cfg]

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


    def sketch(s, item_size:Tuple[int, int]) -> Tuple[List[List[chr]], List[List[chr]]]:
        (x, y) = item_size
        '''Sketch the item with size (x, y)'''
        grid = [[TRANSPARENT for i in range(y)] for j in range(x)]
        style = [[s.style for i in range(y)] for j in range(x)]
        return (grid, style)
    
    def apply(s, offset : Tuple[int, int], item_size : Tuple[int, int], char: List[List[str]], style : List[List[str]]):
        (x, y) = item_size
        (off_x, off_y) = offset
        '''Apply the rendered item on canvas (char, style) with offset'''
        (grid, stl) = s.sketch(item_size)
        for i in range (x):
            for j in range (y):

                if(grid[i][j] != TRANSPARENT):
                    char[i + off_x][j + off_y] = grid[i][j]
                if(stl[i][j] != ''):
                    style[i + off_x][j + off_y] = stl[i][j]

class texture(item):
    '''texture loaded from file, intented to be displayed in one place'''
    TEXTURE_PATH=Path("res/texture").expanduser()
    def __init__(self, filename:str):
        # logger.info("Creating texture %s", filename)
        self.filename = filename
        try:
            with open(self.TEXTURE_PATH.joinpath(filename), "r") as f:
                data = json.load(f)
            self.attrmap = data['attrmap']
            self.textures = data['textutes']
            #Debug to-delete
            # for t in self.textures:
                # logger.info( " Texture %s : '%s' => '%s'", filename, self.textures[t][0][0], bytes(self.textures[t][0][0], 'UTF-8'))
        except Exception as e:
            logger.error("Failed to load file: %s", e)
    def getSize(self, item_size:Tuple[int, int]):
        (x, y) = item_size
        # Find the texture approieate for thy size
        best = "0x0"
        for t in self.textures:
            (tx, ty) = t.split("x")
            (bx, by) = best.split("x")
            (tx, ty) = (int(tx), int(ty))
            (bx, by) = (int(bx), int(by))
            # logger.info("Looking: %s vs %s", (bx, by), (tx, ty))
            if(tx <= x and ty <= y and tx+ty >= bx+by):
                best=t
        if(best == "0x0"):
            logger.error("Texture %s has no size suitale for %s", self.filename, item_size)
            return ([[]], [[]])
        (tx, ty) = best.split("x")
        (tx, ty) = (int(tx), int(ty))
        return (tx, ty)
        
    def sketch(self, item_size:Tuple[int, int]) -> Tuple[List[List[str]], List[List[str]]]:
        (x, y) = item_size
        (tx, ty) = self.getSize(item_size)
        (grid, style) = super().sketch(item_size)
        tex = self.textures[str(tx)+'x'+str(ty)]
        # Find middle of drawing area
        x0 = int((x - tx+1)/2)
        y0 = int((y - ty+1)/2)
        #Apply appropieate texture
        for i in range(tx):
            for j in range(ty):
                grid[i+x0][j+y0] = tex[0][i][j]
                style[i+x0][j+y0] = self.attrmap[tex[1][i][j]]
        # logger.debug("Apply: %s, %s", grid, style)
        return(grid, style)
            
class dynamicTexture(texture):
    '''texture loaded from file, intented to have animated movement'''
    def __init__(self, filename : str, item_size : Tuple[int, int]):
        self.move_queue = asyncio.Queue()
        super().__init__(filename)
        # Keep track of last display parameters
        self.item_size = item_size
        self.pos = (None, None)
        self.prev_pos = (None, None)
        self.next_pos = (None, None)
        self.loopTask = tui_main.aloop.create_task(self.move_loop())
    def cancel_anim(self):
        while(not self.move_queue.empty()): self.move_queue.get_nowait() 
        self.loopTask.cancel()
        self.loopTask = tui_main.aloop.create_task(self.move_loop())
    def resize(self, item_size : Tuple[int, int]):
        if(self.item_size != item_size):
            #Stop any animation as resize may cause it to be distorted
            self.cancel_anim()
            self.pos = self.next_pos
            self.item_size=item_size
            # urwid.CanvasCache.clear()
            # tui_main.loop.draw_screen()
            
    async def move_loop(self):
        while(True):
            target_offset = await self.move_queue.get()
            if(self.pos == (None, None)): self.pos = target_offset
            self.prev_pos = self.pos
            self.next_pos = target_offset
            
            start = time()
            end = start + cfg["anim speed"]
            delay = cfg["anim speed"] / 1000
            while(time() < end):
                (dx, dy) = (self.next_pos[0] - self.prev_pos[0], self.next_pos[1] - self.prev_pos[1])
                prog = min((time() - start) / cfg["anim speed"], 1)
                self.pos = (int(self.prev_pos[0] + dx * prog ), int(self.prev_pos[1] + dy * prog))
                urwid.CanvasCache.clear()
                tui_main.loop.draw_screen()
                await asyncio.sleep(delay)
            self.pos = self.next_pos
            urwid.CanvasCache.clear()
            tui_main.loop.draw_screen()
        
    def move_instant(self, target_offset : Tuple[int, int]):
        self.cancel_anim()
        self.pos = target_offset
        self.prev_pos = target_offset
        self.next_pos = target_offset
    
    def move_anim(self, target_offset : Tuple[int, int]):
        self.move_queue.put_nowait(target_offset)
    def apply(s, offset : Tuple[int, int], item_size : Tuple[int, int], char, style):
        #Save-check resize
        s.resize(item_size)
        return super().apply(offset, item_size, char, style)
    def apply_anim(self, char, style):
        # logger.info("Apllying anim %s", self.pos)
        '''Ignores argument offset and size, use functions resize and move to animate'''
        if(self.pos == (None, None)): return
        return self.apply((self.pos[0], self.pos[1]), self.item_size, char, style)
        # super().__init__()
      
class PlayerTexture(dynamicTexture):
    def __init__(self, level : Level, size : Tuple[int, int] = (0, 0)):
        self.level = level
        super().__init__("player.json", size)
    def update(self, grid_size : Tuple[int, int], instant:bool=False):
        try:
            (x, y) = grid_size
            self.resize((x//self.level.height//3, y//self.level.width//3))
            field = player.player['currentField']
            (gx, gy) = self.level.get_cord(field)
            (n, m) = (self.level.height, self.level.width)
            x0 = x0 = x * gx// n
            y0 = y * gy // m
            x1 = x * (gx+1) // n
            y1 = y * (gy+1) // m
            
            (off_x, off_y) = (x0 + (x1-x0+2)//3, y0 + (y1-y0+2)//3 )
            # logger.info("Drawing player.player : size=%s, field=%d, (gx, gy)=%s, (ox, oy)=%s", grid_size, field, (gx, gy), (off_x, off_y))
            if(not instant):
                self.move_anim((off_x, off_y))
            else:
                self.move_instant(((off_x), (off_y)))
        except TypeError as e:
            logger.error('Update dailed : %s, to field:%s ', e, player.player['currentField'])

class itemSquare(item):
    bg='#'
    fg='.'
    bg_style = ''
    fg_style = ''
    blocked='x'
    blocked_style='yellow'
    
    def __init__(self, field : Field):
        # super().__init__()
        self.cache = None
        self.cacheSize = None
        self.field = field
        self.paths = [bool(i in field.neighbours) for i in AIM_LABEL]
        self.used_tiles = []

        self.seed = self.field.num
        self.bg_style=["magenta", "cyan", "default"][self.seed%3]
        self.fg_style=["magenta", "cyan", "default"][(self.seed+1)%3]
        self.decorations = list(self.field.decorations)
        self.update()
        self.field.updateCallback = self.update
        
    def update(self):
        self.grid = [[0 for i in range(3)] for j in range(3)]
        self.grid[1][1]=True
        for i in range(4):
            self.grid[1 + AIM[i][0] ][ 1 + AIM[i][1] ] = self.paths[i]
        if(not True in self.paths): self.grid[1][1]=False
        self.cacheSize=None
    def cords_to_pos(self, item_size:Tuple[int, int], cord:Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        (x, y) = item_size
        def calc(n:int, poz:int): return int((n//3)*poz + min(n%3, poz))
        (x0, y0) = (calc(x, cord[0]), calc(y, cord[1]))
        (x1, y1) = (calc(x, cord[0]+1), calc(y, cord[1]+1))
        return ((x0, y0), (x1-x0, y1-y0))
        
    def is_empty(self, poz:Tuple[int, int], size:Tuple[int, int], char:List[List[str]]):
        for i in range(poz[0], poz[0]+size[0]):
            for j in range(poz[1], poz[1]+size[1]):
                if(char[i][j] != self.bg):
                    return False
        return True
    
    def sketch(self, item_size:Tuple[int, int]):
        if(self.cache != None and self.cacheSize == item_size):
            return self.cache
        self.cacheSize = item_size
        self.cache = self._sketch(item_size)
        return self.cache
    
    def _sketch(self, item_size:Tuple[int, int]):
        rnd = random.Random(self.seed)
        (x, y) = item_size
        if(self.field.blocked):
            out   = [[self.blocked if self.grid[i*3//x][j*3//y] else self.bg for j in range(y)] for i in range(x)]
            style = [[self.blocked_style if self.grid[i*3//x][j*3//y] else self.bg_style for j in range(y)] for i in range(x)]
        else:
            out   = [[self.fg if self.grid[i*3//x][j*3//y] else self.bg for j in range(y)] for i in range(x)]
            style = [[self.fg_style if self.grid[i*3//x][j*3//y] else self.bg_style for j in range(y)] for i in range(x)]
        max_size = (item_size[0]//3, item_size[1]//3)

        # Apply decorations
        for it in self.decorations:
            dec = texture(it+".json")
            (dec_x, dec_y) = dec.getSize(max_size)
            poz = (rnd.randint(0, x-dec_x), rnd.randint(0, y-dec_y))
            for i in range(100):
                # logger.info("Checking poz=%s, dec=%s, grid=%s", poz, (dec_x, dec_y), item_size)
                if(not self.is_empty(poz, (dec_x, dec_y), out)):
                    poz = (rnd.randint(0, x-dec_x), rnd.randint(0, y-dec_y))
                else: break
            if(not self.is_empty(poz,  (dec_x, dec_y), out)):
                logger.info("Field %s could not draw decoration %s", self.field.num, dec)
            logger.info("dec %s, %s, %s", item_size, poz, (dec_x, dec_y))
            dec.apply(poz, (dec_x, dec_y), out, style)
        return (out, style)

    def __del__(self):
        self.field.updateCallback = None
class itemSquareForest(itemSquare):
    def __init__(self, field):
        super().__init__(field)
        self.fg = ' '
        self.bg = '.'
        self.bg_style = 'green'
        self.fg_style = 'default'
        self.seed = self.field.num + int(bytes(player.player['currentField']).hex(), 16)
        self.rnd = random.Random(self.seed)
        self.decorations 
    def _sketch(self, item_size):
        rnd = random.Random(self.seed)
        dec = texture("tree.json")
        max_size = (item_size[0]//3, item_size[1]//3)
        dec_size = dec.getSize(max_size)
        max_deco = (6*max_size[0]*max_size[1]) // int((dec_size[0]*dec_size[1])**(1.2))
        now_deco = rnd.randint(1, max_deco)
        self.decorations += ["tree"]*now_deco
        (out, style) = super()._sketch(item_size)
        self.decorations = self.decorations[:-now_deco]
        
        return (out, style)
    @property
    def blocked(self):
        chars=[' ', ' ', ' ', '@', '.', '!', ' ', ' ', '&', ',', ' ', ' ', ' ']
        return chars[self.rnd.randint(0, len(chars)-1)]
squareThemes = {
    "default":itemSquare,
    "forest":itemSquareForest
}
def current_itemSquare():
    return squareThemes[cfg["theme"]]