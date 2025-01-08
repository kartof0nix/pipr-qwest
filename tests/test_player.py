from src.globals.player import removeSave, PlayerClass
from src.globals.template import ev_template, boolEval, autoEval

def test_template():
    # removeSave("test")
    player = PlayerClass("test.json")

    # Give items to the player
    player.giveItem("sword")
    player.giveItem("shield")

    assert( player.hasItem("sword") ==True )
    assert( player.hasItem("dagger") == False )

    assert( player.calcAttack() == 10)
    assert( player.calcDefense() == 15) 

    # Save and persist the inventory