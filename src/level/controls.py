from src.level import Level
from src.common import event_queue
import logging
# from src.graphics import tui_main
logger = logging.getLogger(__name__)

class Control:
    def __init__(self, level:Level):
        self.level = level
        pass

    def handleKey(self, key:str):
        if(key in ['up', 'down', 'right', 'left']):
            self.level.move(key)
        if(key=='i'):
            self.level.inspect()
        if(key=='esc'):
            event_queue.pushEvent("gameover")