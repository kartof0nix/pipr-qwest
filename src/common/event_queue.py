'''Common event queue for all game events. Modules may push and listen for events.'''

from asyncio import Queue
import asyncio
from src.graphics import tui_main
import logging
logger = logging.getLogger(__name__)

q = Queue()
def pushEvent(event : str, params:dict = {}):
    q.put_nowait((event, params))

registered={}
def registerHandler(event:str, func):
    if event not in registered:
        registered[event] = []
    registered[event] += [func]
    
def unregisterHandler(event:str, func):
    try:
        registered[event].pop(registered[event].index(func))
    except Exception as e:
        logger.info("Attemptet to pop function from listers, but it already has no listeners : %s", e)
    
async def loop():
    while(True):
        (ev, par) = await q.get()
        logger.info("Event %s, %s", ev, par)
        if(ev in registered):
            for f in registered[ev]:
                asyncio.create_task(f(par))
    
    
    
    