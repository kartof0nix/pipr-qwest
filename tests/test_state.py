from src.globals import player
from src.globals.template import ev_template, boolEval, autoEval

def test_template():
    player.player = player.PlayerClass("test_state.json")
    player.player['goblinFlag'] = True
    assert(boolEval("{{ player.player.goblinFlag}}") == True)
    player.player['goblinFlag'] = False
    assert(autoEval("{{ player.player['goblinFlag']}}") == False)
    
    player.player['goblinsKilled'] = 8
    assert(boolEval("{{ player.player['goblinsKilled'] > 10}}") == False)
    player.player['goblinsKilled'] = autoEval("{{player.player.goblinsKilled + 3}}")
    assert(autoEval("{{ player.player.goblinsKilled > 10 }}") == True)
    a