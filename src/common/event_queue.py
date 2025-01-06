'''Common event queue for all game events. Modules may push and listen for events.'''

from asyncio import Queue
from src.graphics import tui_main
import logging
logger = logging.getLogger(__name__)

q = Queue()
async def push(event : str, params:dict = {}):
    await q.put((event, params))

registered={}
def register(event:str, func):
    if event not in registered:
        registered[event] = []
    registered[event] += [func]
    
def unregister(event:str, func):
    try:
        registered[event].pop(registered[event].index(func))
    except Exception as e:
        logger.info("Attemptet to pop function from listers, but it already has no listeners : %s", e)
    
async def loop():
    while(True):
        (ev, par) = await q.get()
        if(ev in registered):
            for f in registered[ev]:
                tui_main.aloop.create_task(f(par))
    
    
    
    