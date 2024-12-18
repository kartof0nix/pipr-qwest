from player import player
from typing import List, Tuple

global eventTypes
eventTypes = {}
global registeredEvents
registeredEvents = {}


class RegisterEventMeta(type):
    def __new__(mcs, name, bases, class_dict):
        global eventTypes
        cls = super().__new__(mcs, name, bases, class_dict)
        if name != "GameEvent":  # Don't register the base class
            eventTypes |= {name: cls}
        return cls


class GameEvent(metaclass=RegisterEventMeta):
    def __init__(self, eventId, nextEventId: str = None):
        global registeredEvents
        registeredEvents |= {eventId: self}
        self.eventId = eventId
        self.nextEvent = nextEventId

    def __call__(self, *args, **kwds) -> str:
        return self.nextEvent


class IfEvent(GameEvent):
    def __init__(self, eventId: str, condition: str = "", eventIdTrue: str = None, eventIdFalse: str = None):
        self.condition = condition
        self.eventIdTrue = eventIdTrue
        self.eventIdFalse = eventIdFalse
        super().__init__()

    def __init__(self, dict):
        pass

    def __call__(self, *args, **kwds) -> str:
        pass

class menuEvent(GameEvent):
    def __init__(self, eventId, entryList : List[str], eventIdList: List["str"]):
        self.entryList = entryList
        self.eventIdList =eventIdList
        super().__init__(eventId, eventIdList[0])
    def __call__(self):
        pass
class ConversationEvent(GameEvent):
    def __init__(self, eventId: str, dialogue: List[Tuple[str, str]], nextEventId: str = None):
        super().__init__(eventId, nextEventId)


def eventFromList(type: str, args: list):
    return eventTypes[type](*args)
