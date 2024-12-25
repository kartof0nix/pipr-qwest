from player import player
from typing import List, Tuple
import logging
logger = logging.getLogger(__name__)

global eventTypes
eventTypes = {}
global registeredEvents
registeredEvents = {}


class RegisterEventMeta(type):
    """Meta class to keep track of registered event classes"""
    def __new__(mcs, name, bases, class_dict):
        global eventTypes
        cls = super().__new__(mcs, name, bases, class_dict)
        if name != "GameEvent":  # Don't register the base class
            eventTypes |= {name: cls}
        return cls


class GameEvent(metaclass=RegisterEventMeta):
    """Single instance registers the single event"""
    def __init__(self, eventId, nextEvent: str = ""):
        global registeredEvents
        registeredEvents |= {eventId: self}
        self.eventId = eventId
        self.nextEvent = nextEvent

    def __call__(self, *args, **kwds) -> str:
        return self.nextEvent


class IfEvent(GameEvent):
    defaultConfig = {
        'condition' : "True",
        'eventIdTrue' : "",
        'eventIdFalse' : ""
    }
    def __init__(self, eventId: str, config : dict = {}):
        config = self.defaultConfig | config
        self.condition = config['condition']
        self.eventIdTrue = config['eventIdTrue']
        self.eventIdFalse = config['eventIdFalse']
        super().__init__(eventId)

    def __init__(self, dict):
        pass

    def __call__(self, *args, **kwds) -> str:
        pass

class DamageEvent(GameEvent):
    defaultConfig = {
        'health': 0,
        "nextEvent" : ""
    }
    def __init__(self, eventId: str, config : dict = {}):
        config = self.defaultConfig | config
        self.health = config['health']
        super().__init__(eventId, config['nextEvent'])
    def __call__(self):
        player.
        return super().__call__() 

class menuEvent(GameEvent):
    defaultConfig = {
        'entryList' : [],
        'eventList' : []
    }
    def __init__(self, eventId: str, config : dict = {}):
        config = self.defaultConfig | config
        self.entryList = config['entryList']
        self.eventList = config['eventList']
        super().__init__(eventId, self.eventList[0])
    def __call__(self):
        pass
    
class ConversationEvent(GameEvent):
    defaultConfig = {
        'dialogue' : [],
        "nextEvent" : ""
    }
    def __init__(self, eventId: str, config : dict = {}):
        config = self.defaultConfig | config
        self.dialogue = config['dialogue']
        super().__init__(eventId, config['nextEvent'])


def eventFromDict(type: str, eventId: str, config : dict = {}):
    try:
        return eventTypes[type](eventId, config)
    except KeyError as e:
        logger.error("Event type '%s' undefined", type)
        # Return dummy event as quick-fix
        return GameEvent(eventId, config['nextEvent'] if 'nextEvent' in config else "")
