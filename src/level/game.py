from src.logic.player import PlayerClass
from src.logic.template import ev_template
from src.events import eventFromDict, GameEvent, registeredEvents
import json

from pathlib import Path
from typing import List, Tuple, Dict
import logging
import traceback
import asyncio

from src.common.config import Config, Setting
logger = logging.getLogger(__name__)

async def runEvent(event : GameEvent):
    return event()

async def launchEvents(eventId : str):
    while(eventId != "" and eventId != None):
        try:
            event = registeredEvents[eventId]
            eventId = event()
        except Exception as e:
            logger.error("Running event %s failed: %s", eventId, e)

DIRECTIONS = {
    'right' : [0, 1],
    'down' : [1, 0],
    'left' : [0, -1],
    'up' : [-1, 0]
}

class Field:
    def __init__(self, player : PlayerClass, neighbours : Dict[str, int] = {}, eventOnEnter : str = "", eventOnInspect : str = "", eventOnLeave : str = ""):
        self.neighbours = dict(neighbours)
        self.eventOnEnter = eventOnEnter
        self.eventOnInspect = eventOnInspect
        self.eventOnLeave = eventOnLeave
        
    @classmethod
    def from_dict(self, player, cfg:Dict):
        res = Field(player)
        self.player = player
        if ('neighbours') in cfg: res.neighbours = cfg['neighbours']     
        if ('eventOnEnter') in cfg: res.eventOnEnter = cfg['eventOnEnter']     
        if ('eventOnInspect') in cfg: res.eventOnInspect = cfg['eventOnInspect']     
        if ('eventOnLeave') in cfg: res.eventOnLeave = cfg['eventOnLeave']     
        return res

    def enter(self):
        asyncio.create_task(launchEvents(self.eventOnEnter))

    def exit(self):
        asyncio.create_task(launchEvents(self.eventOnExit))
    
    def inspect(self):
        asyncio.create_task(launchEvents(self.eventOnInspect))
        
    def move(self, direction:str) -> bool:
        if( direction not in self.neighbours ): return False
        logger.debug("Neighbours of %s : %s", self.player['currentField'], str(self.neighbours))
        logger.debug("Move %s from %s to %s", direction, self.player['currentField'], self.neighbours[direction])
        self.player['currentField'] = self.neighbours[direction]
        return True
    
        
class Level:
    def __init__(self, player : PlayerClass, name : str, fieldsInit : Dict[int, Dict[str, str]], startField : int, graph : List[Tuple], grid : List[List[int]]= None):
        self.queue = asyncio.Queue()
        self.player = player
        # self.eventList = eventList
        player['currentField'] = startField
        registeredEvents.clear()
        self.name = name
        self.graph = graph
        self.fieldDict = {}
        # Initialize fields
        for i in fieldsInit:
            logger.debug("Init field %d from dict %s", int(i), fieldsInit[i])
            self.fieldDict[int(i)] = Field.from_dict(player=player, cfg=fieldsInit[i])
                
        #Initialize grid
        self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        for i in range(self.height):
            for j in range(self.width):
                if not grid[i][j] in self.fieldDict:                
                    logger.info("Level %s undefined field %d", self.name, grid[i][j])
                    self.fieldDict[grid[i][j]] = Field(player)
                for d in DIRECTIONS:
                    i2 = i + DIRECTIONS[d][0]
                    j2 = j + DIRECTIONS[d][1]
                    if( 0 <= i2 < self.height and 0 <= j2 < self.width):
                        fieldA = grid[i][j]
                        fieldB = grid[i2][j2]
                        if([fieldA, fieldB] in self.graph or [fieldB, fieldA] in self.graph):
                            logger.debug("Adding %s path from %s to %s ", d, fieldA, fieldB)
                            self.fieldDict[fieldA].neighbours[d] = fieldB
    def getField(self, i, j) -> Field:
        return self.fieldDict[self.grid[i][j]]
    async def move(self, direction : str):
        res = self.fieldDict[self.player['currentField']].move(direction)
        if(not res): return False
        await self.queue.put("move")
        self.fieldDict[self.player['currentField']].enter()
        return True
        

    def inspect(self):
        return self.fieldDict[self.player['currentField']].inspect()
    
levelsPaths = "res/levels/"

class levelConfig(Config):
    CONFIG_PATH=Path("res/levels").expanduser()

"""Load level from file"""
def loadLevel(filename : str, player : PlayerClass, startField: int = None) -> Level:
    s = levelConfig(filename,
        {
            "name" : filename,
            "fields" : {},
            "startField": 1,
            "graph" : [],
            "grid": [[1]],
            "events" : {}
        } 
    )
    try:
        # for event in s.events
        if(startField == None): startField = s['startField']
        logger.debug(s.config)
        lvl = Level(player=player,
                    name=s['name'],
                    fieldsInit=s['fields'],
                    startField=startField,
                    graph=s['graph'],
                    grid=s['grid'] 
                )
        for ev in s['events']:
            eventFromDict(type=ev['eventType'], eventId=ev['eventId'], player=player, config=ev['params'])
        return lvl
    except Exception as e:
        logger.error("Loading level %s failed: %s", filename, e)
        logger.debug(traceback.print_exc())
        