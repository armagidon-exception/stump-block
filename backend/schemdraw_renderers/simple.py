from schemdraw import Drawing
from schemdraw.elements import Element, ElementDrawing
from schemdraw.flow import Box, Data, Subroutine, Terminal
from schemdraw.util import XY

from backend.schemdraw_renderers import Renderer
from blocks import Block


class SimpleRenderer(Renderer):
    def render_element(
        self,
        element: Element,
        drawing: Drawing,
        block: Block,
        render_dict: dict[str, Renderer],
    ) -> tuple[XY, XY]:
        drawing += element
        return element.N, element.S

    @classmethod
    def get_size(cls, el: Element) -> tuple[float, float]:
        with Drawing(show=False) as d:
            d += el
        box = ElementDrawing(d).get_bbox(includetext=True)
        return box.xmax - box.xmin, box.ymax - box.ymin


class BoxRenderer(SimpleRenderer):
    def produce(self, block: Block) -> Element:
        dims = SimpleRenderer.get_size(Box().label(block.tooltip))
        return Box(w=dims[0], h=dims[1]).label(block.tooltip)


class SubroutineRenderer(SimpleRenderer):
    def produce(self, block: Block) -> Element:
        return Subroutine().label(block.tooltip)


class TerminalRenderer(SimpleRenderer):
    def __init__(self, title: str, create_arrow: bool = True) -> None:
        self.title = title
        self.create_arrow = create_arrow

    def produce(self, block: Block) -> Element:
        return Terminal().label(self.title)


class InputRenderer(SimpleRenderer):
    def produce(self, block: Block) -> Element:
        return Data().label(f"Enter: {block.tooltip}")


class OutputRenderer(SimpleRenderer):
    def produce(self, block: Block) -> Element:
        return Data().label(f"Output: {block.tooltip}")
