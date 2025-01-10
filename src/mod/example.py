
from asyncio.log import logger
from typing import Any, Dict
from src.events.game import GameEvent
from src.events.graphics import NotifyEventTUI
from src.globals import player

'''This is an exaple mod ilustrating the idea of modding.
Note that ItemGiveEvent is defined in the base-game levels, so removing this file will cause the game to fail'''


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


class ItemGiveEventTUI(NotifyEventTUI):
    def __init__(self, event: ItemGiveEvent):
        super().__init__(event)
        self.text = f"You got a {
            self.event.item_id.replace('_', ' ').capitalize()}"
