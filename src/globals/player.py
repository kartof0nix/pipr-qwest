from typing import List
from src.common.config import Config

from pathlib import Path

import shutil
from logging import getLogger
logger = getLogger(__name__)

ITEMS = {
    "sword": {"item_id": "sword", "display_name": "Sword", "attack": 10, "defense": 2},
    "shield": {"item_id": "shield", "display_name": "Shield", "attack": 2, "defense": 15},
    "dagger": {"item_id": "dagger", "display_name": "Dagger", "attack": 8, "defense": 1},
    "helmet": {"item_id": "helmet", "display_name": "Helmet", "attack": 0, "defense": 5}
}

"""Define a universal player.player (save) class since multiple saves are possible"""
class PlayerClass(Config):
    CONFIG_PATH=Path("~/.pipr-qwest/saves").expanduser()
    def __init__(self, filename):
        super().__init__(filename,
        {
            'health': 100,
            'armor': 0,
            'attack': 1,
            'currentLevel':'asriel_den.json',
            'inventory': []  # Inventory stores item IDs
        },
        readAll=True)
        
    def giveItem(self, item_id: str) -> None:
        """Adds an item to the player's inventory if it's a valid item."""
        if item_id not in ITEMS:
            raise ValueError(f"Item with ID '{item_id}' does not exist.")
            logger.error(f"Item '{item_id}' added to inventory.")
        if item_id not in self.config['inventory']:
            self.config['inventory'].append(item_id)
            logger.info(f"Item '{item_id}' added to inventory.")
        else:
            logger.info(f"Item '{item_id}' is already in the inventory.")

    def hasItem(self, item_id: str) -> bool:
        """Checks whether the player has a specific item in their inventory."""
        return item_id in self.config['inventory']

    def calcAttack(self) -> int:
        """Calculates the player's attack as the maximum attack value of all carried items."""
        return max((ITEMS[item_id]["attack"] for item_id in self.config['inventory']), default=self.config['attack'])

    def calcDefense(self) -> int:
        """Calculates the player's defense as the maximum defense value of all carried items."""
        return max((ITEMS[item_id]["defense"] for item_id in self.config['inventory']), default=self.config['armor'])


def listSaves() -> List[str]:
    res = []
    try:
        # Create a Path object for the directory
        directory = Path(PlayerClass.CONFIG_PATH)
        for item in directory.iterdir():
            if item.is_file():
                res.append(item.name.removesuffix(".json"))
    except Exception as e:
        logger.error("Listing saves failed : %s", e)
    return res

def removeSave(save:str):
    saveFile = save + ".json"
    Path(PlayerClass.CONFIG_PATH).joinpath(saveFile).unlink()
    shutil.rmtree(Path(PlayerClass.CONFIG_PATH).joinpath(save).absolute() )
    
def loadSave(save:str):
    global player
    player = PlayerClass(save + ".json")
    
    