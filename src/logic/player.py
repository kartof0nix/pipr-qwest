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

class PlayerClass:
    def __init__(self):
        self.inventory = []
        self.health = 100
        self.name = __name__
    
player = PlayerClass()