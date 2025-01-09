
from src.events.game import CombatEvent, GameEvent, ConversationEvent, DamageEvent
from src.globals import player
from src.graphics import tui_main
from src.graphics.common import CustomButton, notificationWidget
from src.graphics.common import buttonAttr
import urwid
import asyncio
from typing import Any, List, Tuple
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

class NotifyEventTUI(GameEventTUI):
    def __enter__(self):
        tui_main.add_frame(notificationWidget(self.text, self.event.complete.set), len(self.text)+10, 3, ('center', 'middle'), 'Notification', True)
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        tui_main.rem_frame()
        pass

class DamageEventTUI(NotifyEventTUI):
    def __init__(self, event : DamageEvent):
        super().__init__(event)
        self.text = f"You have been dealt {self.event.hp} damage!"

class ChangeLevelEventTUI(NotifyEventTUI):
    def __init__(self, event : DamageEvent):
        super().__init__(event)
        self.text = f"You have found a passage to {self.event.nextLevel.removesuffix(".json").replace('_', ' ').capitalize()}"

class ItemGiveEventTUI(NotifyEventTUI):
    def __init__(self, event : DamageEvent):
        super().__init__(event)
        self.text = f"You got a {self.event.item_id.replace('_', ' ').capitalize()}"
# class DamageEvent(GameEvent):
#     localConfig = {
#         'health': 0,
#         "nextEvent": ""
#     }

#     def __init__(self, eventId: str, config: dict):
#         self.defaultConfig |= self.localConfig
#         super().__init__(eventId, config)

#     def __call__(self):
#         return super().__call__()

class MenuEventTUI(GameEventTUI):
    def itemChosen(self, button: urwid.Button):
        self.event.select(self.event.entryList.index(button.label))

    def makeWidget(self):
        pile = [urwid.Text(('magenta', 'Choose action'))]
        self.y = len('Choose action')
        for it in self.event.entryList:
            pile.append(buttonAttr(urwid.Button(it, self.itemChosen)))
            self.y = max(self.y, len(it))

        self.x = len(pile)
        w = urwid.Pile(pile)
        return w

    def __enter__(self):
        logger.info("Entering TUI!")
        self.widget=urwid.WidgetPlaceholder(self.makeWidget())

        # self.widget.keypress = self.keypress
        tui_main.add_frame(self.widget, self.y+10, self.x, 'bottom', 'Choice', True)
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

#     def __init__(self, eventId: str, config: dict):
#         self.defaultConfig |= self.localConfig
#         super().__init__(eventId, config)

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
        self.y = 0
        for it in self.event.dialogue:
            self.y = max(self.y, len(it[0]), len(it[1]))
        self.x=3
        return urwid.Pile([urwid.Text(('magenta', character+":")), (urwid.Text(('cyan', text))), urwid.Filler(buttonAttr(urwid.Button("Next", self.keypress )))])
    def keypress(self, size: tuple[int, int] = None, key: str = None) -> str | None:    #         logger.info("UwuSync Sleeping")
        if(key in [" ", "enter"]):
            self.event.nextLine()
            if not(self.event.complete.is_set()):
                self.widget.original_widget = self.makeWidget()
                tui_main.loop.draw_screen()
            return None
        if(key in ['up', 'down', 'left', 'right']): return None
        return key
    def __enter__(self):
        logger.info("Entering TUI!")
        (character, text) = self.event.currentLine()
        # tui_main.aloop.create_task(self.tui_loop())
        self.widget=urwid.WidgetPlaceholder(self.makeWidget())
        self.widget.keypress = self.keypress
        tui_main.add_frame(self.widget, self.y+5, self.x, 'bottom', 'Conversation', True)
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        logger.info("Exitting TUI!")
        tui_main.rem_frame()
        pass



class CombatEventTUI(GameEventTUI):
    def __init__(self, event: CombatEvent) -> None:
        super().__init__(event)
        self.widget = None
        self.message = ""

    def update_message(self, text: str) -> None:
        """
        Update the message displayed to the player and redraw the TUI.
        """
        self.message = text
        self.widget.original_widget = self.makeWidget()
        self.redraw()

    def makeWidget(self) -> urwid.Widget:
        """
        Create the combat interface widget, displaying the opponent's health,
        the player's health, and available actions.
        """
        pile = [
            urwid.Text(('magenta', f"Opponent Health: {self.event.opponentHealth}")),
            urwid.Text(('cyan', f"Your Health: {player.player['health']}")),
            urwid.Text(('yellow', self.message)),
            buttonAttr(urwid.Button("Attack", on_press=lambda _: self.choose_action("attack"))),
            buttonAttr(urwid.Button("Brace", on_press=lambda _: self.choose_action("brace"))),
            buttonAttr(urwid.Button("Flee", on_press=lambda _: self.choose_action("flee"))),
        ]
        return urwid.Pile(pile)

    def choose_action(self, action: str) -> None:
        """
        Handle the player's action and update the TUI with the results.
        """
        messages = self.event.action(action)  # Use the `action` method from CombatEvent
        logger.info("Update combat with %s", messages)
        self.update_message("\n".join(messages))  # Display all resulting messages

        # Check if the event is complete and close the TUI if so

    def redraw(self) -> None:
        """
        Redraw the TUI interface.
        """
        tui_main.loop.draw_screen()

    def __enter__(self) -> "CombatEventTUI":
        """
        Set up the TUI when entering the context.
        """
        logger.info("Entering CombatEventTUI context.")
        self.widget = urwid.WidgetPlaceholder(self.makeWidget())
        tui_main.add_frame(self.widget, width=('relative', 70), height='pack', side=('center', 'middle'), title='Combat with %s'%(self.event.name), block_move=True)
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """
        Clean up the TUI when exiting the context.
        """
        logger.info("Exiting CombatEventTUI context.")
        tui_main.rem_frame()
