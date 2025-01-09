'''
Call the package directly to test it.
'''

from src.common.event_queue import loop
from src.globals import player
from src.level import LevelManager
from src.graphics import tui_main
import asyncio
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='qwest.log',
                    level=logging.INFO, filemode="w")


# a = fabricCanvas([["a", "b"], ["c", "d"]], [["", ""], ["", ""]])
# for c in a.content():
#     print(c)
# print(a.content())

async def test():
    logger.info(f"Starting test module {__package__}")
    # player.player = PlayerClass("testLevel.json")
    player.loadSave("testLevel.json")
    LevelManager.callLevel("asriel_den.json")
    tui_main.aloop.create_task(loop())
    await asyncio.sleep(10)
    LevelManager.delLevel()
    # del lvl
tui_main.render(test)
