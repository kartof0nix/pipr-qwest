import os
from typing import List
from src.level.game import Field, Level, loadLevel, LEVEL_PATH
from src.level.graphics import LevelView

from src.logic.player import PlayerClass

import asyncio
import logging
logger = logging.getLogger(__name__)

class LevelManagerClass:
    lvl = None
    view = None
    def callLevel(self, filename : str, player : PlayerClass, startField=None) -> Level:
        self.lvl = loadLevel(filename, player=player, startField=startField)
        self.view = LevelView(self.lvl)
        return self.lvl

    def delLevel(self):
        del self.lvl
        del self.view
        self.lvl=None
        self.view=None
    def listLevels(self) -> List[str]:
        res = []
        try:
            # List all files and directories in the specified path
            with os.scandir(LEVEL_PATH) as entries:
                for entry in entries:
                    if entry.is_file():  # Check if the entry is a file
                        res += [entry.name]
        except Exception as e:
            logger.error("Could not load levels : %s", e)
        return res

LevelManager = LevelManagerClass()
    