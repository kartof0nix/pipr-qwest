
from src.events.game import GameEvent, ConversationEvent
from src.graphics import tui_main
from src.graphics.common import CustomButton

import urwid
import asyncio
from typing import List, Tuple
import logging
logger = logging.getLogger(__name__)

global eventTUIs
eventTUIs = {}


class RegisterEventTUIMeta(type):
    """Meta class to keep track of registered event TUI classes"""
    def __new__(mcs, name, bases, class_dict):
        global eventTUIs
        cls = super().__new__(mcs, name, bases, class_dict)
        if name != "GameEvent":  # Don't register the base class
            eventTUIs |= {name: cls}
        return cls


class GameEventTUI(metaclass=RegisterEventTUIMeta):
    """Base class for event's TUI. Every instance of any child class registers the instance"""
    def __init__(self, event : GameEvent):
        self.event = event

    def __enter__(self) -> str:
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        pass


# class DamageEvent(GameEvent):
#     localConfig = {
#         'health': 0,
#         "nextEvent": ""
#     }

#     def __init__(self, eventId: str, config: dict, player : PlayerClass):
#         self.defaultConfig |= self.localConfig
#         super().__init__(eventId, config, player)

#     def __call__(self):
#         return super().__call__()

class menuEventTUI(GameEventTUI):

    def itemChosen(self, button: urwid.Button):
        self.event.select(self.event.entryList.index(button.label))

    def makeWidget(self):
        pile = [urwid.Text(('magenta', 'Choose action'))]
        for it in self.event.entryList:
            pile.append(urwid.Button(it, self.itemChosen))
        return urwid.Pile(pile)

    def __enter__(self):
        logger.info("Entering TUI!")
        self.widget=urwid.WidgetPlaceholder(self.makeWidget())
        # self.widget.keypress = self.keypress
        tui_main.add_frame(self.widget, 100, 10, 'bottom', 'Choice')
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        logger.info("Exitting TUI!")
        tui_main.rem_frame()
        pass
# class menuEvent(GameEvent):
#     localConfig = {
#         'entryList': [],
#         'eventList': []
#     }

#     def __init__(self, eventId: str, config: dict, player : PlayerClass):
#         self.defaultConfig |= self.localConfig
#         super().__init__(eventId, config, player)

#     def __call__(self):
#         return super().__call__()


class ConversationEventTUI(GameEventTUI):
    # def __init__(self, event : GameEvent):
    #     global registeredEvents
    #     registeredEventTUI |= {event.eventId: self}

    # async def tui_loop(self):
    #     while(True):
    #         await asyncio.sleep(2)

    def makeWidget(self):
        (character, text) = self.event.currentLine()
        return urwid.Pile([urwid.Text(('magenta', character)), (urwid.Text(('cyan', text))), urwid.Filler(urwid.Button("Next", self.keypress ))])
    def keypress(self, size: tuple[int, int] = None, key: str = None) -> str | None:    #         logger.info("UwuSync Sleeping")
        logger.info("kerypees")
        self.event.nextLine()
        if not(self.event.complete.is_set()):
            self.widget.original_widget = self.makeWidget()
            tui_main.loop.draw_screen()
    def __enter__(self):
        logger.info("Entering TUI!")
        (character, text) = self.event.currentLine()
        # tui_main.aloop.create_task(self.tui_loop())
        self.widget=urwid.WidgetPlaceholder(self.makeWidget())
        self.widget.keypress = self.keypress
        tui_main.add_frame(self.widget, 100, 10, 'bottom', 'Conversation')
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        logger.info("Exitting TUI!")
        tui_main.rem_frame()
        pass

