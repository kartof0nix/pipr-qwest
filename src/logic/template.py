from jinja2 import Environment, PackageLoader, select_autoescape
from player import player
import logging
logger = logging.getLogger(__name__)

env = Environment(
    autoescape=select_autoescape()
)

def eval(template : str):
    template = env.from_string(template)
    return template.render(player = player)
    
def boolEval(template : str) -> bool:
    a = eval(template).replace(' ', '').replace('\n', '').lower()
    if a == "true": return True
    if a == "false": return False
    logger.error("Template '%s' eval error: '%s' not a boolean", template, a)
    return False
        



