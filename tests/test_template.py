from src.globals import player
from src.globals.template import ev_template, boolEval, autoEval

def test_template():
    player.loadSave("pytest")
    player.player['goblinFlag'] = True
    assert(boolEval("{{ player.goblinFlag}}") == True)
    player.player['goblinFlag'] = False
    assert(autoEval("{{ player['goblinFlag']}}") == False)
    
    player.player['goblinsKilled'] = 8
    assert(boolEval("{{ player['goblinsKilled'] > 10}}") == False)
    player.player['goblinsKilled'] = autoEval("{{player.goblinsKilled + 3}}")
    assert(autoEval("{{ player.goblinsKilled > 10 }}") == True)