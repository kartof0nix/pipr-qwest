import asyncio
import logging
from src.level import loadLevel
from src.globals import player

logger = logging.getLogger(__name__)
async def _test_level_main(queue):
    player.loadSave("pytest")
    lvl = loadLevel("pytest.json")
    assert(queue.empty())
    assert(player.player['currentField'] == 1)
    lvl.move("right")
    assert(player.player['currentField'] == 2)
    mv = await queue.get()
    assert(mv == "move")
    lvl.move("up")
    assert(player.player['currentField'] == 2)
    lvl.move("right")
    assert(player.player['currentField'] == 3)
    lvl.move("down")
    assert(player.player['currentField'] == 6)
    lvl.move("up")
    assert(player.player['currentField'] == 3)

    
    

def _test_level():
    queue = asyncio.Queue()
    asyncio.run(_test_level_main(queue))
