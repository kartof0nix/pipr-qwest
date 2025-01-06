from src.events.game import registeredEvents
from src.events.graphics import eventTUIs

import traceback
import logging
logger = logging.getLogger(__name__)

async def runEvent(eventId : str) -> str:
    logger.info(eventId)
    event = registeredEvents[eventId]
    if(type(event).__name__+"TUI" in eventTUIs):
        with eventTUIs[type(event).__name__+"TUI"](event) as tui:
            res = await event()
    else:
        res = await event()
    return res

async def launchEvents(eventId : str):
    while(eventId != "" and eventId != None):
        try:
            logger.info("launching %s", eventId)
            eventId = await runEvent(eventId)
        except Exception as e:
            logger.error("Running event %s failed: %s", eventId, e)
            logger.error(traceback.format_exc())
            return