from src.globals.template import ev_template, boolEval, setValue
from src.common.event_queue import pushEvent
from src.globals import player
# from src.level import LevelManager
import asyncio
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
    def __init__(self, eventId, config: dict,  uiEvent:bool=False):
        global registeredEvents
        registeredEvents |= {eventId: self}
        self.eventId = eventId
        self.uiEvent = True
        for key in self.defaultConfig:
            self.__dict__[key] = config[key] if key in config else self.defaultConfig[key]
        if(uiEvent):
            self.complete = asyncio.Event()

    async def __call__(self) -> str:
        
        pushEvent("event_start", {"event":self})
        if(self.uiEvent):
            await self.complete.wait()
            self.complete.clear()
        pushEvent("event_end", {"event":self})
        # logger.info("Len: %s, %d", self.eventId,  len(self.assignValues))
        for (key, template) in self.assignValues:
            setValue(key, ev_template(template))
        return self.nextEvent


class IfEvent(GameEvent):
    localConfig = {
        'condition': "True",
        'eventIdTrue': "",
        'eventIdFalse': ""
    }

    def __init__(self, eventId: str, config: dict):
        self.defaultConfig |= self.localConfig
        super().__init__(eventId, config)

    async def __call__(self, *args, **kwds) -> str:
        await super().__call__()
        if(boolEval(self.condition)):
            return self.eventIdTrue
        else:
            return self.eventIdFalse
        pass


class DamageEvent(GameEvent):
    localConfig = {
        'hp': 0,
        "nextEvent": "",
        'assignValues': []
    }

    def __init__(self, eventId: str, config: dict):
        self.defaultConfig |= self.localConfig
        if('assignValues' not in config): config['assignValues'] = []
        config['assignValues'] += [('player.health', "{{ player['health']- %s}}" % (config['hp']))]
        super().__init__(eventId, config,  True)

    async def __call__(self):
        res = await super().__call__()
        if(player.player['health'] <= 0):
            pushEvent('gameover')
        return res



class menuEvent(GameEvent):
    localConfig = {
        'entryList': [],
        'eventList': []
    }
    def select(self, entryid=0):
        self.selection = entryid
        self.complete.set()
    def __init__(self, eventId: str, config: dict):
        self.defaultConfig |= self.localConfig
        self.selection = 0
        super().__init__(eventId, config,  uiEvent=True)

    async def __call__(self):
        await super().__call__()
        return self.eventList[self.selection]


class ConversationEvent(GameEvent):
    localConfig = {
        'dialogue': [],
        "nextEvent": ""
    }

    def __init__(self, eventId: str, config: dict):
        self.defaultConfig |= self.localConfig
        self.current = 0
        super().__init__(eventId, config,  uiEvent=True)

    def currentLine(self) -> Tuple[str, str]:
        return self.dialogue[self.current]
    def nextLine(self) -> Tuple[str, str]:
        self.current += 1
        if(self.current >= len(self.dialogue)): self.complete.set()

    async def __call__(self):
        res = await super().__call__()
        self.current = 0
        return res

class changeLevelEvent(GameEvent):
    localConfig = {
        'nextLevel': '',
        'nextField': 0,
        "nextEvent": ""
    }

    def __init__(self, eventId: str, config: dict):
        self.defaultConfig |= self.localConfig
        super().__init__(eventId, config,  uiEvent=True)

    async def __call__(self):
        res = await super().__call__()
        '''Don't call the level manager to avoid circular import.
        Level manager should listen for this event to hanndle changing thy level'''
        # LevelManager.changeLevel(self.nextLevel, self.nextField)
        return res
    
def eventFromDict(type: str, eventId: str,  config: dict = {}):
    try:
        return eventTypes[type](eventId, config)
    except KeyError as e:
        logger.error("Event type '%s' undefined", type)
        # Return dummy event as quick-fix
        return GameEvent(eventId, config)
# e = changeLevelEvent()
