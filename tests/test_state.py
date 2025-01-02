from src.logic.player import PlayerClass
from src.logic.template import ev_template, boolEval, autoEval

def test_template():
    player = PlayerClass("test_state.json")
    player['goblinFlag'] = True
    assert(boolEval("{{ player.goblinFlag}}", player) == True)
    player['goblinFlag'] = False
    assert(autoEval("{{ player['goblinFlag']}}", player) == False)
    
    player['goblinsKilled'] = 8
    assert(boolEval("{{ player['goblinsKilled'] > 10}}", player) == False)
    player['goblinsKilled'] = autoEval("{{player.goblinsKilled + 3}}", player)
    assert(autoEval("{{ player.goblinsKilled > 10 }}", player) == True)
    