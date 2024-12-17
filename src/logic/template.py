from jinja2 import Environment, PackageLoader, select_autoescape
from player import player

env = Environment(
    autoescape=select_autoescape()
)

def eval(template : str):
    template = env.from_string(template)
    return template.render(player = player)
    
def boolEval(template : str) -> bool:
    return eval(template).replace(' ', '').replace('\n', '') == "True"

