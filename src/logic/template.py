from jinja2 import Environment, PackageLoader, select_autoescape
import logging

from src.logic import player
logger = logging.getLogger(__name__)

env = Environment(
    autoescape=select_autoescape()
)
def ev_template(template : str):
    temp = env.from_string(template)
    # return temp.render(player.player = player.player.config, fields = fieldDict)
    
def boolEval(template : str):
    out = ev_template(template).replace(' ', '').lower()
    if(out=='false'): return False
    if(out=='true'): return True
    logger.error("Type error while rendering template %s : '%s' not a boolean", template, out)
    return False

def intEval(template : str) -> int:
    value = ev_template(template).replace(' ', '').lower()
    try:
        return int(value)
    except ValueError as e:
        logger.error("Error rendering template %s : %s", template, e)
        return 0    

def autoEval(template : str):
    value = ev_template(template).replace(' ', '').lower()
    try:
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value  # Leave as string if all conversions fail

def setValue(key:str, value):
    key = key.split('.')
    try:
        if(key[0] == 'player.player'):
            player.player[key[1]] = type(player.player[key[1]])(value)
        # elif(key[0]=='field'):
        #     fieldDict[key[1]][key[2]]=type(fieldDict[key[1]][key[1]])(value)
    except Exception as e:
        logger.error("Setting value %s failed: %s", key, e)
            