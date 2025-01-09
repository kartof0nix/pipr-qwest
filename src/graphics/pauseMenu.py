
from __future__ import annotations
import asyncio
from typing import List, Any
import urwid
from collections.abc import Iterable

from src.common.config import Setting, registered_settings
from src.graphics import tui_main
from src.graphics.settings import launchSettings
from src.graphics.common import CustomButton, buttonAttr, notify
from src.globals import player, fields
from src.common import event_queue
import logging
logger = logging.getLogger(__name__)


def saveGame():
    player.player.save_to_file()
    for field in fields.fields:
        fields.fields[field].attr.save_to_file()


class PauseMenu(urwid.Pile):
    def saveButton(self, butt: urwid.Button):
        saveGame()
        notify("Game saved!")

    def saveAndExitButton(self, butt: urwid.Button):
        saveGame()
        event_queue.pushEvent("gameover")

    def exitButton(self, butt: urwid.Button):
        event_queue.pushEvent("gameover")

    def settingsButton(self, butt: urwid.Button):
        asyncio.create_task(launchSettings())

    def unpauseButton(self, butt: urwid.Button = None):
        tui_main.rem_frame()

        # asyncio.create_task(launchSettings())
    def keypress(self, size, key):
        if (key == 'esc'):
            self.unpauseButton()
        else:
            return super().keypress(size, key)

    def __init__(self):
        menu = [
            buttonAttr(urwid.Button("Save game", self.saveButton)),
            buttonAttr(urwid.Button("Save and exit", self.saveAndExitButton)),
            buttonAttr(urwid.Button("Exit without saving", self.exitButton)),
            # buttonAttr(urwid.Button("Settings", self.settingsButton )),
            buttonAttr(urwid.Button("Unpause", self.unpauseButton))
        ]
        super().__init__(menu)
