from schemdraw import Drawing
from schemdraw.elements import Element
from schemdraw.flow import Box, Subroutine
from schemdraw.util import XY

from backend.schemdraw_renderers import Renderer
from blocks import Block


class BoxRenderer(Renderer):
    def render_element(self, element: Element, drawing: Drawing, block: Block, render_dict: dict[str, Renderer]) -> XY:
        drawing += element
        return element.N, element.S

    def produce(self, block: Block) -> Element:
        return Box().label(block.tooltip)

class SubroutineRenderer(Renderer):
    def render_element(self, element: Element, drawing: Drawing, block: Block, render_dict: dict[str, Renderer]) -> tuple[XY, XY]:
        drawing += element
        return element.N, element.S

    def produce(self, block: Block) -> Element:
        return Subroutine().label(block.tooltip)
