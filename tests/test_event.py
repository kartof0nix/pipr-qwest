from ..src.logic.event import registeredEvents, GameEvent, IfEvent, ConversationEvent, menuEvent, eventFromDict
import pytest
import logging

def test_nextEvent():

    ev_dial = ConversationEvent("wstep_dialog", {'dialogue' : [("andy", "Hi There"), ("andy", "Chose your class")], "nextEvent" : "wstep_class"})
    ev_menu = menuEvent("wstep_class", {"entryList": ["Male", "Female"], "eventList" : ["wstep_class_man", "wstep_class_fem"]})
    
    assert(ev_dial() == ev_menu.eventId)
    
def test_eventLib(caplog):
    caplog.set_level(logging.ERROR)
    ev1 = eventFromDict("DogEvent", "id1", {"nextEvent": "id2"})
    assert(ev1() == "id2")
    assert("Event type 'DogEvent' undefined" in caplog.text)
    
    ev2 = eventFromDict("ConversationEvent", "id2", {'dialogue' : [("andy", "Hi There"), ("andy", "Chose your class")], "nextEvent" : "wstep_class"})
    assert(type(ev2) == ConversationEvent)
    assert(type(ev2.dialogue) == list)
    
