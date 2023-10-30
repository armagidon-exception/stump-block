from typing import Self

from schemdraw import Drawing
from schemdraw.elements import Element
from schemdraw.flow import Terminal
from schemdraw.util import XY

from backend.schemdraw_renderers import Renderer
from blocks import Block


class TerminalRenderer(Renderer):
    def __init__(self, title: str, create_arrow: bool = True) -> None:
        self.title = title
        self.create_arrow = create_arrow

    def render_element(
        self,
        element: Element,
        drawing: Drawing,
        block: Block,
        render_dict: dict[str, Self],
    ) -> tuple[XY, XY]:
        drawing += element
        return element.N, element.S

    def produce(self, block: Block) -> Element:
        return Terminal().label(self.title)
