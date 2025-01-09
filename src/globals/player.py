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
    "helmet": {"item_id": "helmet", "display_name": "Helmet", "attack": 0, "defense": 5},

    # AI-generated Items
    "greatsword": {"item_id": "greatsword", "display_name": "Greatsword", "attack": 20, "defense": 5},
    "longbow": {"item_id": "longbow", "display_name": "Longbow", "attack": 15, "defense": 3},
    "battle_axe": {"item_id": "battle_axe", "display_name": "Battle Axe", "attack": 18, "defense": 4},
    "magic_staff": {"item_id": "magic_staff", "display_name": "Magic Staff", "attack": 12, "defense": 8},
    "iron_shield": {"item_id": "iron_shield", "display_name": "Iron Shield", "attack": 1, "defense": 20},
    "plate_armor": {"item_id": "plate_armor", "display_name": "Plate Armor", "attack": 0, "defense": 25},
    "chainmail": {"item_id": "chainmail", "display_name": "Chainmail", "attack": 0, "defense": 15},
    "spiked_club": {"item_id": "spiked_club", "display_name": "Spiked Club", "attack": 14, "defense": 6},
    "poisoned_dagger": {"item_id": "poisoned_dagger", "display_name": "Poisoned Dagger", "attack": 10, "defense": 0},
    "warhammer": {"item_id": "warhammer", "display_name": "Warhammer", "attack": 22, "defense": 7},
    "enchanted_cloak": {"item_id": "enchanted_cloak", "display_name": "Enchanted Cloak", "attack": 0, "defense": 12},
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
    try:
        saveFile = save + ".json"
        Path(PlayerClass.CONFIG_PATH).joinpath(saveFile).unlink()
        shutil.rmtree(Path(PlayerClass.CONFIG_PATH).joinpath(save).absolute() )
    except:
        logger.info("Deleting saves failed, hopefully they gone now")
    
def loadSave(save:str):
    global player
    player = PlayerClass(save + ".json")
    
    