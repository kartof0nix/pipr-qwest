from src.logic.template import ev_template, boolEval
from src.logic.player import PlayerClass

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
    """Base class for events. Every instance of any child class registers the instance"""
    defaultConfig = {
        "nextEvent": "",
        "assignValues": []
    }

    def __init__(self, eventId, config: dict, player : PlayerClass):
        global registeredEvents
        registeredEvents |= {eventId: self}
        self.player = player
        self.eventId = eventId
        for key in self.defaultConfig:
            self.__dict__[
                key] = config[key] if key in config else self.defaultConfig[key]

    def __call__(self) -> str:
        for (key, template) in self.assignValues:
            self.player[key] = ev_template(template, self.player)
        return self.nextEvent


class IfEvent(GameEvent):
    localConfig = {
        'condition': "True",
        'eventIdTrue': "",
        'eventIdFalse': ""
    }

    def __init__(self, eventId: str, config: dict, player : PlayerClass):
        self.defaultConfig |= self.localConfig
        super().__init__(eventId, config, player)

    def __call__(self, *args, **kwds) -> str:
        super().__call__()
        if(boolEval(self.condition, self.player)):
            return self.eventIdTrue
        else:
            return self.eventIdFalse
        pass


class DamageEvent(GameEvent):
    localConfig = {
        'health': 0,
        "nextEvent": ""
    }

    def __init__(self, eventId: str, config: dict, player : PlayerClass):
        self.defaultConfig |= self.localConfig
        super().__init__(eventId, config, player)

    def __call__(self):
        return super().__call__()


class menuEvent(GameEvent):
    localConfig = {
        'entryList': [],
        'eventList': []
    }

    def __init__(self, eventId: str, config: dict, player : PlayerClass):
        self.defaultConfig |= self.localConfig
        super().__init__(eventId, config, player)

    def __call__(self):
        return super().__call__()


class ConversationEvent(GameEvent):
    localConfig = {
        'dialogue': [],
        "nextEvent": ""
    }

    def __init__(self, eventId: str, config: dict, player : PlayerClass):
        self.defaultConfig |= self.localConfig
        super().__init__(eventId, config, player)

    def __call__(self):
        return super().__call__()


def eventFromDict(type: str, eventId: str, player : PlayerClass, config: dict = {}):
    try:
        return eventTypes[type](eventId, config, player)
    except KeyError as e:
        logger.error("Event type '%s' undefined", type)
        # Return dummy event as quick-fix
        return GameEvent(eventId, config, player)
