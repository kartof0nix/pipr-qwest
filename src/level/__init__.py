from src.level.game import Field, Level, loadLevel
from src.level.graphics import LevelView

from src.logic.player import PlayerClass

import asyncio
def callLevel(filename : str, player : PlayerClass, startField=None) -> Level:
    lvl = loadLevel(filename, player=player, startField=startField)
    v = LevelView(lvl)
    return lvl

    
