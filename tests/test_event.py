from src.events import registeredEvents, GameEvent, IfEvent, ConversationEvent, menuEvent, eventFromDict
from src.logic.player import PlayerClass
import pytest
import logging


def test_nextEvent():
    
    player = PlayerClass("test1")
    ev_dial = ConversationEvent("wstep_dialog", {'dialogue' : [("andy", "Hi There"), ("andy", "Chose your class")], "nextEvent" : "wstep_class"}, player)
    ev_menu = menuEvent("wstep_class", {"entryList": ["Male", "Female", "Enby"], "eventList" : ["wstep_class_man", "wstep_class_fem", "wstep_class_enby"]}, player=player)
    
    assert(ev_dial() == ev_menu.eventId)
    
def test_eventLib(caplog):
    caplog.set_level(logging.ERROR)
    player = PlayerClass("test2")
    ev1 = eventFromDict("DogEvent", "id1", player=player, config={"nextEvent": "id2"})
    assert(ev1() == "id2")
    assert("Event type 'DogEvent' undefined" in caplog.text)
    
    ev2 = eventFromDict("ConversationEvent", "id2", player=player, config={'dialogue' : [("andy", "Hi There"), ("andy", "Chose your class")], "nextEvent" : "wstep_class"})
    assert(type(ev2) == ConversationEvent)
    assert(type(ev2.dialogue) == list)
    
