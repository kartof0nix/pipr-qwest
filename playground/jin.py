from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    autoescape=select_autoescape()
)

template = env.from_string()