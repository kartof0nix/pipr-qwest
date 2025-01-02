from src.logic.player import PlayerClass
from jinja2 import Environment, PackageLoader, select_autoescape
import logging
logger = logging.getLogger(__name__)

env = Environment(
    autoescape=select_autoescape()
)
def ev_template(template : str, player : PlayerClass):
    temp = env.from_string(template)
    return temp.render(player = player.config)
    
def boolEval(template : str, player : PlayerClass):
    out = ev_template(template, player).replace(' ', '').lower()
    if(out=='false'): return False
    if(out=='true'): return True
    logger.error("Type error while rendering template %s : '%s' not a boolean", template, out)
    return False

def intEval(template : str, player : PlayerClass) -> int:
    value = ev_template(template, player).replace(' ', '').lower()
    try:
        return int(value)
    except ValueError as e:
        logger.error("Error rendering template %s : %s", template, e)
        return 0    

def autoEval(template : str, player : PlayerClass):
    value = ev_template(template, player).replace(' ', '').lower()
    try:
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value  # Leave as string if all conversions fail
