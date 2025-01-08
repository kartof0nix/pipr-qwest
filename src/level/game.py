from src.globals import player, fields
from src.globals.template import ev_template
from src.events import eventFromDict, launchEvents, registeredEvents
from src.common.event_queue import pushEvent
import json
 
from pathlib import Path
from typing import Any, List, Tuple, Dict
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
    def __init__(self, num:int,  neighbours : Dict[str, int] = {}, eventOnEnter : str = "", eventOnInspect : str = "", eventOnLeave : str = "", obstacles:List=[], decorations:List=[], blocked=0):
        self.updateCallback = None
        self.ev_task = None
        self.num = num
        self.eventOnEnter = eventOnEnter
        self.eventOnInspect = eventOnInspect
        self.eventOnLeave = eventOnLeave
        self.attr={
            'neighbours' : dict(neighbours),
            'decorations' : decorations,
            'obstacles' : obstacles,
            'blocked' : blocked
        }    
    @property
    def blocked(self):
        return self.attr['blocked']
    @property
    def neighbours(self):
        return self.attr['neighbours']
    @property
    def decorations(self):
        return self.attr['decorations']
    @property
    def obstacles(self):
        return self.attr['obstacles']
    
    def __getitem__(self, key: str) -> Any:
        return self.attr[key]

    def __setitem__(self, key: str, value: Any):
        self.attr[key] = value
        if(self.updateCallback) != None: self.updateCallback()

    
    @blocked.setter
    def blocked(self, value):
        self['blocked']=value
    @neighbours.setter
    def neighbours(self, value):
        self['neighbours']=value
    @decorations.setter
    def decorations(self, value):
        self['decorations']=value
    @obstacles.setter
    def obstacles(self, value):
        self['obstacles']=value
    
    
    
    @classmethod
    def from_dict(self, num:int, cfg:Dict):
        res = Field(num=num)
        player.player = player.player
        if ('neighbours') in cfg: res.neighbours = cfg['neighbours']     
        if ('eventOnEnter') in cfg: res.eventOnEnter = cfg['eventOnEnter']     
        if ('eventOnInspect') in cfg: res.eventOnInspect = cfg['eventOnInspect']     
        if ('eventOnLeave') in cfg: res.eventOnLeave = cfg['eventOnLeave']     
        if ('decorations') in cfg: res.decorations = cfg['decorations']     
        if ('obstacles') in cfg: res.obstacles = cfg['obstacles']     
        if ('blocked') in cfg: res.blocked = cfg['blocked']     
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
        return self.neighbours[direction]
    
    def exit(self):
        if self.ev_task != None:
            self.ev_task.cancel()
    
class Level:
    def __init__(self,  name : str, fieldsInit : Dict[int, Dict[str, str]], startField : int, graph : List[Tuple], grid : List[List[int]]= None):
        player.player = player.player
        # self.eventList = eventList
        player.player['currentField'] = startField
        registeredEvents.clear()
        self.name = name
        self.graph = graph
        fields.fields = {}
        # Initialize fields
        for i in fieldsInit:
            # logger.debug("Init field %d from dict %s", int(i), fieldsInit[i])
            fields.fields[int(i)] = Field.from_dict(int(i), cfg=fieldsInit[i])
                
        #Initialize grid
        self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        for i in range(self.height):
            for j in range(self.width):
                if not grid[i][j] in fields.fields:                
                    logger.info("Level %s undefined field %d", self.name, grid[i][j])
                    fields.fields[grid[i][j]] = Field(grid[i][j])
                for d in DIRECTIONS:
                    i2 = i + DIRECTIONS[d][0]
                    j2 = j + DIRECTIONS[d][1]
                    if( 0 <= i2 < self.height and 0 <= j2 < self.width):
                        fieldA = grid[i][j]
                        fieldB = grid[i2][j2]
                        if([fieldA, fieldB] in self.graph or [fieldB, fieldA] in self.graph):
                            fields.fields[fieldA].neighbours[d] = fieldB
        fields.setFields(fields.fields)
        
    def getField(self, i, j) -> Field:
        return fields.fields[self.grid[i][j]]
    def move(self, direction : str):
        cur = player.player['currentField']
        res = fields.fields[cur].move(direction)
        if(res == False): return False
        if(fields.fields[res].blocked): return False
        fields.fields[cur].exit()
        player.player['currentField'] = res
        pushEvent("move", {"src" : cur, "dest":res})
        fields.fields[res].enter()
        return True
    def start(self):
        fields.fields[player.player['currentField']].enter()

    def inspect(self):
        return fields.fields[player.player['currentField']].inspect()
    
    def get_cord(self, fieldId:int) -> Tuple[int, int]:
        for i in range(self.height):
            for j in range(self.width):
                if(self.grid[i][j] == fieldId): return (i, j)
        return None
    def exit(self):
        for f in fields.fields:
            fields.fields[f].exit()

class levelConfig(Config):
    CONFIG_PATH=Path(LEVEL_PATH).expanduser()
    def save_to_file(self):
        pass #Don't overrite the file contents

"""Load level from file"""
def loadLevel(filename : str,  startField: int = None) -> Level:
    s = levelConfig(filename,
        {
            "name" : filename,
            "fields" : {},
            "startField": None,
            "graph" : [],
            "grid": [[1]],
            "events" : {}
        } 
    )
    try:
        if(startField == None): startField = s['startField'] # startField <- level config  
        if(startField == None): startField = player.player['currentField']
        logger.debug(s.config)
        lvl = Level(
                    name=s['name'],
                    fieldsInit=s['fields'],
                    startField=startField,
                    graph=s['graph'],
                    grid=s['grid'] 
                )
        for ev in s['events']:
            eventFromDict(type=ev['eventType'], eventId=ev['eventId'], config=ev['params'])
        lvl.start()
        return lvl
    except Exception as e:
        logger.error("Loading level %s failed: %s", filename, e)
        logger.debug(traceback.print_exc())
        