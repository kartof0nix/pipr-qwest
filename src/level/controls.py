from src.level import Level
import logging
from src.graphics import tui_main
logger = logging.getLogger(__name__)

class Control:
    def __init__(self, level:Level):
        self.level = level
        pass

    def handleKey(self, key:str):
        logger.info("Captured key %s", key)
        if(key in ['up', 'down', 'right', 'left']):
            tui_main.aloop.create_task(self.level.move(key))
            
            
    