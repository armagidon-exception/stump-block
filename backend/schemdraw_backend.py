from schemdraw import Drawing
import schemdraw

from backend.schemdraw_renderers import Renderer
from backend.schemdraw_renderers.conditional import ConditionalRenderer
from backend.schemdraw_renderers.loops import (
    ParameterLoopRenderer,
    PostLoopRenderer,
    PreLoopRenderer,
)
from backend.schemdraw_renderers.simple import (
    BoxRenderer,
    InputRenderer,
    OutputRenderer,
    SubroutineRenderer,
    TerminalRenderer,
)
from blocks import Block


schemdraw.svgconfig.text = "text"


def handle(route: list[Block], d: Drawing):
    render_dict = {
        "start": TerminalRenderer(),
        "end": TerminalRenderer(False),
        "input": InputRenderer(),
        "output": OutputRenderer(),
        "condition": ConditionalRenderer(0.5),
        "declaration": BoxRenderer(),
        "assignment": BoxRenderer(),
        "invocation": SubroutineRenderer(),
        "preloop": PreLoopRenderer(),
        "postloop": PostLoopRenderer(),
        "parameterloop": ParameterLoopRenderer(),
    }

    d.add(Renderer.merge_block(route, render_dict))


def render(filename: str, route: list[Block]):
    with Drawing(file=filename, show=False) as d:
        handle(route, d)
