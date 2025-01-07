from src.logic.player import PlayerClass
from src.logic.template import ev_template
from src.events import eventFromDict, launchEvents, registeredEvents
from src.common.event_queue import pushEvent
import json

from pathlib import Path
from typing import List, Tuple, Dict
import logging
import traceback
import asyncio

from src.common.config import Config, Setting
logger = logging.getLogger(__name__)


DIRECTIONS = {
    'right' : [0, 1],
    'down' : [1, 0],
    'left' : [0, -1],
    'up' : [-1, 0]
}
LEVEL_PATH = "res/levels/"

class Field:
    def __init__(self, num:int, player : PlayerClass, neighbours : Dict[str, int] = {}, eventOnEnter : str = "", eventOnInspect : str = "", eventOnLeave : str = "", items:List=[]):
        self.ev_task = None
        self.num = num
        self.neighbours = dict(neighbours)
        self.eventOnEnter = eventOnEnter
        self.eventOnInspect = eventOnInspect
        self.eventOnLeave = eventOnLeave
        self.items = items
        
    @classmethod
    def from_dict(self, num:int, player, cfg:Dict):
        res = Field(player, num)
        self.player = player
        if ('neighbours') in cfg: res.neighbours = cfg['neighbours']     
        if ('eventOnEnter') in cfg: res.eventOnEnter = cfg['eventOnEnter']     
        if ('eventOnInspect') in cfg: res.eventOnInspect = cfg['eventOnInspect']     
        if ('eventOnLeave') in cfg: res.eventOnLeave = cfg['eventOnLeave']     
        if ('items') in cfg: res.items = cfg['items']     
        return res

    def enter(self):
        pushEvent("enter", {"src" : self.num})
        self.ev_task = asyncio.create_task(launchEvents(self.eventOnEnter))

    def exit(self):
        pushEvent("exit", {"src" : self.num})
        self.ev_task = asyncio.create_task(launchEvents(self.eventOnLeave))
    
    def inspect(self):
        pushEvent("inspect", {"src" : self.num})
        self.ev_task = asyncio.create_task(launchEvents(self.eventOnInspect))
        
    def move(self, direction:str) -> bool:
        if( direction not in self.neighbours ): return False
        self.exit()
        self.player['currentField'] = self.neighbours[direction]
        pushEvent("move", {"src" : self.num, "dest":self.neighbours[direction]})
        return True
    
    def exit(self):
        if self.ev_task != None:
            self.ev_task.cancel()
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
            # logger.debug("Init field %d from dict %s", int(i), fieldsInit[i])
            self.fieldDict[int(i)] = Field.from_dict(int(i), player=player, cfg=fieldsInit[i])
                
        #Initialize grid
        self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        for i in range(self.height):
            for j in range(self.width):
                if not grid[i][j] in self.fieldDict:                
                    logger.info("Level %s undefined field %d", self.name, grid[i][j])
                    self.fieldDict[grid[i][j]] = Field(grid[i][j], player)
                for d in DIRECTIONS:
                    i2 = i + DIRECTIONS[d][0]
                    j2 = j + DIRECTIONS[d][1]
                    if( 0 <= i2 < self.height and 0 <= j2 < self.width):
                        fieldA = grid[i][j]
                        fieldB = grid[i2][j2]
                        if([fieldA, fieldB] in self.graph or [fieldB, fieldA] in self.graph):
                            self.fieldDict[fieldA].neighbours[d] = fieldB
    def getField(self, i, j) -> Field:
        return self.fieldDict[self.grid[i][j]]
    def move(self, direction : str):
        res = self.fieldDict[self.player['currentField']].move(direction)
        if(not res): return False
        
        self.fieldDict[self.player['currentField']].enter()
        return True
    def start(self):
        self.fieldDict[self.player['currentField']].enter()

    def inspect(self):
        return self.fieldDict[self.player['currentField']].inspect()
    
    def get_cord(self, fieldId:int) -> Tuple[int, int]:
        for i in range(self.height):
            for j in range(self.width):
                if(self.grid[i][j] == fieldId): return (i, j)
        return None
    def exit(self):
        for f in self.fieldDict:
            self.fieldDict[f].exit()
class levelConfig(Config):
    CONFIG_PATH=Path(LEVEL_PATH).expanduser()
    def save_to_file(self):
        pass #Don't overrite the file contents

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
        lvl.start()
        return lvl
    except Exception as e:
        logger.error("Loading level %s failed: %s", filename, e)
        logger.debug(traceback.print_exc())
        