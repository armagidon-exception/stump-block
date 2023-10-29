from schemdraw import Drawing
from schemdraw.elements import Element
from schemdraw.flow import *
from backend.schemdraw_renderers.conditional import Conditional
from backend.schemdraw_renderers.data import InputRenderer, OutputRenderer
from backend.schemdraw_renderers.terminal import TerminalRenderer

from blocks import Block


# Branching
#cond = Decision().label('condition')
#d += cond
#conseq = Box().label("YES")
#d.move_from(cond.W, -1.5, -1)
#d += conseq.anchor('N')
#d += Wire('-|', 1.5, arrow='->').at(cond.W).to(conseq.N)
#
#alter = Box().label("YES")
#d.move_from(cond.E, 1.5, -1)
#d += alter.anchor('N')
#d += Wire('-|', 1.5, arrow='->').at(cond.E).to(alter.N)
#
#d += (c := Wire('n', -1, arrow='-').at(conseq.S).to(alter.S))
#d += Arrow().down().at(c.mid)

# Bypass

#cond = Decision().label('condition')
#d += cond
#conseq = Box().label("YES")
#d.move_from(cond.W, -1.5, -1)
#d += conseq.anchor('N')
#d += Wire('-|', 1.5, arrow='->').at(cond.W).to(conseq.N)
#
#d += Line().right(1).at(cond.E)
#d += (alter:=Line().toy(conseq.S))
#
#d += (c := Wire('n', -1, arrow='-').at(conseq.S).to(alter.end))
#d += Arrow().down().at(c.mid)

def handle(route: list[Block], d: Drawing, prev: Element | None):
    prev_anchor = None
    render_dict = {
        'start': TerminalRenderer('Start'),
        'end': TerminalRenderer('End', False),
        'input': InputRenderer(),
        'output': OutputRenderer(),
        'condition': Conditional(),
    }
    for block in route:
        if block.type in render_dict:
            element = render_dict[block.type].produce(block)
            if prev_anchor:
                element = element.at(prev_anchor)
            prev_anchor = render_dict[block.type].render_element(element, d, block, render_dict)



def render(filename: str, route: list[Block]):
    with Drawing(file=filename, show=False) as d:
        d.config(unit=1)
        handle(route, d, None)
