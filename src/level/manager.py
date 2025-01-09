import os
from typing import List
from src.graphics import tui_main
from src.level.game import Field, Level, loadLevel, LEVEL_PATH
from src.level.graphics import LevelView
from src.common import event_queue
from src.events.game import ChangeLevelEvent
from src.globals import player

import asyncio
import logging
import traceback
logger = logging.getLogger(__name__)

class LevelManagerClass:
    lvl = None
    # view = None
    def __init__(self):
        self.exitEvent = asyncio.Event()
        event_queue.registerHandler("event_end", self.changeLevelListener)
        event_queue.registerHandler("gameover", self.gameOverListener)
    def callLevel(self, filename : str, startField=None):
        asyncio.create_task(self._callLevel(filename, startField=startField))

    async def _callLevel(self, filename : str, startField=None) -> Level:
        try:
            self.lvl = loadLevel(filename, startField=startField)
            with LevelView(self.lvl) as l:
                await self.exitEvent.wait()
            logger.info("Closing level %s", self.lvl.name)
            self.exitEvent.clear()
        except Exception as e:
            logger.error("Running level failed: %s", e)
            logger.error("Traceback : %s", traceback.format_exc())

    def delLevel(self):
        self.exitEvent.set()
        self.lvl.exit()
        tui_main.loop.draw_screen()
        
    
    async def _changeLevel(self, nextLevel : str, nextField:int = None):
        player.player['currentLevel'] = nextLevel
        self.delLevel()
        while self.exitEvent.is_set():
            await asyncio.sleep(0.1)
        await self._callLevel(nextLevel, startField=nextField)
    def changeLevel(self, nextLevel : str, nextField:int = None):
        asyncio.create_task(self._changeLevel(nextLevel=nextLevel, nextField=nextField))

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
    async def changeLevelListener(self, params:dict):
        event = params['event']
        if(isinstance(event, ChangeLevelEvent)):
            await self._changeLevel(event.nextLevel, event.nextField)
    async def gameOverListener(self, params:dict):
        self.delLevel()
            
        
        
        
LevelManager = LevelManagerClass()
    
    