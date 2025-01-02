import asyncio
import logging
from src.level.level import Level, loadLevel
from src.logic.player import PlayerClass

logger = logging.getLogger(__name__)
async def _test_level_main(queue):
    player = PlayerClass("1")
    lvl = loadLevel("asriel_den.json", queue, player)
    assert(queue.empty())
    assert(player['currentField'] == 1)
    await lvl.move("right")
    assert(player['currentField'] == 2)
    mv = await queue.get()
    assert(mv == "move")
    await lvl.move("up")
    assert(player['currentField'] == 2)
    await lvl.move("right")
    assert(player['currentField'] == 3)
    await lvl.move("down")
    assert(player['currentField'] == 6)
    await lvl.move("up")
    assert(player['currentField'] == 3)

    
    

def test_level():
    queue = asyncio.Queue()
    asyncio.run(_test_level_main(queue))
