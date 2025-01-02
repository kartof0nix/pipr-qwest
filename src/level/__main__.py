'''
Test the module.
'''

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='qwest.log',
                        level=logging.DEBUG, filemode="w")

from src.graphics.main import render
from src.level import callLevel
from src.logic.player import PlayerClass


# a = fabricCanvas([["a", "b"], ["c", "d"]], [["", ""], ["", ""]])
# for c in a.content():
#     print(c)
# print(a.content())
async def test():
    # return
    logger.info(f"Starting test module {__package__}")
    player = PlayerClass("testLevel.json")
    callLevel("asriel_den.json", player=player)
    
render(test)