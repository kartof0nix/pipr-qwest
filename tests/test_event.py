from ..src.logic.event import registeredEvents, GameEvent, IfEvent, ConversationEvent, menuEvent

def test_next():

    ev1 = ConversationEvent("wstep_dialog", [("andy", "Hi There"), ("andy", "Chose your class")], "wstep")
    ev2 = menuEvent("wstep_class", ["Male", "Female"], ["wstep_class_man", "wstep_class_fem"])
    
    assert(ev1())
    