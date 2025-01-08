import asyncio
import logging
from src.level import Level, loadLevel
from src.globals import player

logger = logging.getLogger(__name__)
async def _test_level_main(queue):
    player.player = player.PlayerClass("1")
    lvl = loadLevel("asriel_den.json", queue)
    assert(queue.empty())
    assert(player.player['currentField'] == 1)
    await lvl.move("right")
    assert(player.player['currentField'] == 2)
    mv = await queue.get()
    assert(mv == "move")
    await lvl.move("up")
    assert(player.player['currentField'] == 2)
    await lvl.move("right")
    assert(player.player['currentField'] == 3)
    await lvl.move("down")
    assert(player.player['currentField'] == 6)
    await lvl.move("up")
    assert(player.player['currentField'] == 3)

    
    

def test_level():
    queue = asyncio.Queue()
    asyncio.run(_test_level_main(queue))
