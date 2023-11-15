from pprint import pprint
from command import Command
from schemdraw import *
from schemdraw.flow import *
import schemdraw

schemdraw.svgconfig.text = "text"


def render_method(name, commands: list[Command]):
    drawing_stack: list[Drawing] = [Drawing(file=f'{name}.svg')]
    drawing_stack[0].draw(show=False)
    print("--------------------------------------------")
    print(name)
    pprint(commands)
    print("--------------------------------------------")


def render(input: dict[str, list[Command]]):
    for name, cmds in input.items():
        render_method(name, cmds)
