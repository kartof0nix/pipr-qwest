import random
from src.globals.template import ev_template, boolEval, setValue
from src.common.event_queue import pushEvent
from src.globals import player

# from src.level import LevelManager
import asyncio
from typing import Any, Dict, List, Literal, Tuple
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
        self.uiEvent = uiEvent
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
    
class MoveBackEvent(GameEvent):
    """Event to move the player back to the previous field."""
    localConfig = {
        "nextEvent": "",
        "assignValues": []
    }

    def __init__(self, eventId: str, config: dict):
        self.defaultConfig |= self.localConfig
        super().__init__(eventId, config)

    async def __call__(self):
        res = await super().__call__()
        player.player['currentField'] = player.player['previousField']
        pushEvent("move")
        return self.nextEvent


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


class MenuEvent(GameEvent):
    localConfig = {
        'entryList': [],
        'eventList': []
    }

    def __init__(self, eventId: str, config: Dict[str, Any]) -> None:
        self.defaultConfig |= self.localConfig
        super().__init__(eventId, config, uiEvent=True)
        self.selection: int = -1  # Default invalid selection

    def select(self, entryId: int) -> None:
        """
        Called by the TUI to select an entry and complete the event.
        """
        if 0 <= entryId < len(self.entryList):
            self.selection = entryId
            self.complete.set()  # Mark the event as complete
        else:
            raise ValueError(f"Invalid selection {entryId}. Must be within the range of entryList.")

    async def __call__(self) -> str:
        """
        Waits for the event to complete and returns the next event ID.
        """
        await super().__call__()  # Wait for the TUI to signal completion
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

class ChangeLevelEvent(GameEvent):
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

class CombatEvent(GameEvent):
    localConfig = {
        'name': "",
        'opponentHealth': 100,
        'opponentAttack': 10,
        'opponentDefense': 5,
        'playerAttackBoost': 5,
        'playerDefenseBoost': 5,
        'playerHealAmount': 10,
        'nextEvent': '',
        'eventFlee': '',
    }

    def __init__(self, eventId: str, config: Dict[str, Any]) -> None:
        self.defaultConfig |= self.localConfig
        super().__init__(eventId, config, uiEvent=True)
        # self.opponentHealth: int = config.get('opponentHealth', 100)
        # self.opponentAttack: int = config.get('opponentAttack', 10)
        # self.opponentDefense: int = config.get('opponentDefense', 5)
        # self.playerAttackBoost: int = config.get('playerAttackBoost', 5)
        # self.playerDefenseBoost: int = config.get('playerDefenseBoost', 5)
        # self.playerHealAmount: int = config.get('playerHealAmount', 10)
        self.fled: bool = False

    def player_attack(self) -> str:
        """Player attacks the opponent."""
        damage = max(1, random.randint(player.player.calcAttack() - 5, player.player.calcAttack() + 5) - self.opponentDefense)
        self.opponentHealth = max(0, self.opponentHealth - damage)
        return f"You dealt {damage} damage to the opponent. Opponent's health is now {self.opponentHealth}."

    def player_brace(self) -> str:
        """Player braces for the next attack."""
        player.player.set_value('health', min(100, player.player['health'] + self.playerHealAmount))
        self.playerHealAmount = max(1, self.playerHealAmount-5)
        return f"You brace, increasing defense and healing for {self.playerHealAmount} health.\n-->The combat tires you. Your next brace will be weaker."

    def player_flee(self) -> str:
        """Player attempts to flee."""
        self.fled = True
        self.complete.set()
        return "You fled the combat!"

    def opponent_attack(self) -> str:
        """Opponent attacks the player.player."""
        damage = max(1, random.randint(self.opponentAttack - 5, self.opponentAttack + 5) - player.player.calcDefense())
        player.player.set_value('health', max(0, player.player['health'] - damage))
        if player.player['health'] <= 0:
            pushEvent("gameover")
            return "The opponent defeated you. Game over!"
        return f"The opponent dealt {damage} damage. Your health is now {player.player['health']}."

    async def __call__(self) -> str:
        self.fled=False
        """
        Loop until the combat ends. Returns nextEvent if combat ends normally.
        """
        # while not self.complete.is_set():
        #     if self.opponentHealth <= 0 or player.player['health'] <= 0:
        #         self.complete.set()
        await super().__call__()
        return self.eventFlee if self.fled else self.nextEvent
    def action(self, action: Literal['attack', 'brace', 'flee']) -> List[str]:
        """
        Simulates a full combat round based on the player.player's chosen action.

        Args:
            action: The player.player's chosen action ('attack', 'brace', 'flee').

        Returns:
            A list of resulting messages from the combat round.
        """
        messages = []

        # Player's action
        if action == 'attack':
            messages.append(self.player_attack())
        elif action == 'brace':
            messages.append(self.player_brace())
        elif action == 'flee':
            messages.append(self.player_flee())
        else:
            raise ValueError(f"Invalid action: {action}")

        # Opponent's turn
        if not self.complete.is_set():
            messages.append(self.opponent_attack())

        # Check for end of combat
        if self.opponentHealth <= 0:
            messages.append("The opponent is defeated!")
            self.complete.set()
        elif player.player['health'] <= 0:
            messages.append("You are defeated. Game over!")
            self.complete.set()
        pushEvent("event_change")
        return messages


class ItemGiveEvent(GameEvent):
    localConfig = {
        'item_id': '',
        'nextEvent': '',
    }

    def __init__(self, eventId: str, config: Dict[str, Any]) -> None:
        """
        Initialize the ItemGiveEvent.
        
        Args:
            eventId (str): The unique ID of the event.
            config (Dict[str, Any]): Configuration for the event, including the item_id.
        """
        self.defaultConfig |= self.localConfig
        super().__init__(eventId, config, uiEvent=True)


    async def __call__(self) -> str:
        try:
            player.player.giveItem(self.item_id)
        except Exception as e:
            logger.info(e)
        return await super().__call__()

        
def eventFromDict(type: str, eventId: str,  config: dict = {}):
    try:
        return eventTypes[type](eventId, config)
    except KeyError as e:
        logger.error("Event type '%s' undefined", type)
        # Return dummy event as quick-fix
        return GameEvent(eventId, config)
# e = changeLevelEvent()

        return self.escapeEvent