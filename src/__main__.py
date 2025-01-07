'''
Call the package directly to run it.
'''

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='qwest.log',
                        level=logging.INFO, filemode="w")

import urwid
import asyncio
from src.graphics import tui_main
from src.level import LevelManager
from src.logic.player import PlayerClass
from src.common.event_queue import loop

# a = fabricCanvas([["a", "b"], ["c", "d"]], [["", ""], ["", ""]])
# for c in a.content():
#     print(c)
# print(a.content())
class Main:
    async def exit(self):
        self.player.save_to_file()
        tui_main.view.stop()
    async def start(self):
        logger.info(f"Starting game")
        self.player = PlayerClass("player.json")
        lvl = LevelManager.callLevel("asriel_den.json", player=self.player)
        tui_main.aloop.create_task(loop())
        await asyncio.sleep(10)
        LevelManager.delLevel()
        # del lvl
# a = input("Select level")
main = Main()

tui_main.render(main.start, main.exit)

