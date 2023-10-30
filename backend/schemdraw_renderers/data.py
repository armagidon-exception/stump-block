from typing import Self

from schemdraw import Drawing
from schemdraw.elements import Element
from schemdraw.flow import Data
from schemdraw.util import XY

from backend.schemdraw_renderers import Renderer
from blocks import Block


class InputRenderer(Renderer):
    def render_element(
        self,
        element: Element,
        drawing: Drawing,
        block: Block,
        render_dict: dict[str, Self],
    ) -> XY | tuple[Element, str]:
        drawing += element
        return element.N, element.S

    def produce(self, block: Block) -> Element:
        return Data().label(f"Enter: {block.tooltip}")


class OutputRenderer(Renderer):
    def render_element(
        self,
        element: Element,
        drawing: Drawing,
        block: Block,
        render_dict: dict[str, Self],
    ) -> XY | tuple[Element, str]:
        drawing += element
        return element.N, element.S

    def produce(self, block: Block) -> Element:
        return Data().label(f"Output: {block.tooltip}")
