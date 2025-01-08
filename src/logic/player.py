from typing import List
from src.common.config import Config

from pathlib import Path

from logging import getLogger
logger = getLogger(__name__)

class Item:
    def __init__(self, itemId : str, name : str = None, desc : str = ""):
        self.itemId = itemId
        if(name == None): name = self.itemId.capitalize()
        self.name = name
        self.desc = desc
    def use(self):
        pass
    
class WeaponItem(Item):
    def __init__(self, itemId : str, dmg : int, name : str = None, desc : str = ""):
        super().__init__(itemId, name, desc)
        self.dmg = dmg

class ArmorItem(Item):
    def __init__(self, itemId : str, ac : int, name : str = None, desc : str = ""):
        super().__init__(itemId, name, desc)
        self.ac = ac
    

item_lib = {i.itemId : i for i in [
    WeaponItem("mace", 3),
    ArmorItem("plaete armor", 2)
    
]}

"""Define a universal player.player (save) class since multiple saves are possible"""
class PlayerClass(Config):
    CONFIG_PATH=Path("~/.pipr-qwest/saves").expanduser()
    def __init__(self, filename):
        super().__init__(filename,
        {
            'health': 100,
            'armor': 0,
            'attack': 1,
            'currentLevel':'asriel_den.json'
        },
        readAll=True)
        
    def set_value(self, name, value):
        self.config[name] = value
    

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
    save += ".json"
    file = Path(PlayerClass.CONFIG_PATH).joinpath(save)
    file.unlink()
    
def loadSave(save:str):
    global player
    player = PlayerClass(save + ".json")
    
    