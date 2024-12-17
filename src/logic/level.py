from player import player

global eventTypes
eventTypes = {}
global registeredEvents
registeredEvents = {}

class RegisterEventMeta(type):
    def __new__(mcs, name, bases, class_dict):
        global eventTypes
        cls = super().__new__(mcs, name, bases, class_dict)
        if name != "GameEvent":  # Don't register the base class
            eventTypes |= {name : cls}
        return cls

class GameEvent(metaclass=RegisterEventMeta):
    def __init__(self, eventId, nextEventId:str=None):
        global registeredEvents
        registeredEvents |= {eventId : self}
        self.eventId = eventId
        self.nextEvent=nextEventId
    def __call__(self, *args, **kwds) -> str:
        return self.nextEvent

class IfEvent(GameEvent):
    def __init__(self, eventId, condition : str = "", eventIdTrue : str = None, eventIdFalse : str = None):
        self.condition = condition
        self.eventIdTrue = eventIdTrue
        self.eventIdFalse = eventIdFalse
        super().__init__()
    def __init__(self, dict):
        pass
    def __call__(self, *args, **kwds) -> str:
        pass
    
def eventFromDict(type : str, *args):
    return eventTypes[type](*args)
# class 