'''
Call the package directly to test it.
'''

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='qwest.log',
                        level=logging.DEBUG, filemode="w")
import asyncio
from src.graphics import tui_main
from src.level import callLevel
from src.logic.player import PlayerClass
from src.common.event_queue import loop

# a = fabricCanvas([["a", "b"], ["c", "d"]], [["", ""], ["", ""]])
# for c in a.content():
#     print(c)
# print(a.content())
async def test():
    # return
    logger.info(f"Starting test module {__package__}")
    player = PlayerClass("testLevel.json")
    lvl = callLevel("asriel_den.json", player=player)
    tui_main.aloop.create_task(loop())
    # await asyncio.sleep(5)
    # await lvl.move('right')
    # await asyncio.sleep(5)
    # await lvl.move('right')
    # await asyncio.sleep(5)
    # await lvl.move('down')
    # await asyncio.sleep(1)
    # await lvl.move('up')
tui_main.render(test)