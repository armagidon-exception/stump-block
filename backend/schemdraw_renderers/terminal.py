from typing import Self
from schemdraw import Drawing
from schemdraw.elements import Element
from schemdraw.util import XY
from backend.schemdraw_renderers import Renderer
from schemdraw.flow import Arrow, Terminal

from blocks import Block


class TerminalRenderer(Renderer):

    def __init__(self, title: str, create_arrow:bool=True) -> None:
        self.title = title
        self.create_arrow = create_arrow

    def render_element(self, element: Element, drawing: Drawing, block: Block, render_dict: dict[str, Self]) -> XY | tuple[Element, str]:
        drawing += element
        anchor = element.S
        if self.create_arrow:
            drawing += (connective:= Arrow().down(drawing.unit) )
            anchor = connective.end
        return anchor

    def produce(self, block: Block) -> Element:
        return Terminal().label(self.title)
