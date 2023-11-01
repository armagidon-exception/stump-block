from abc import ABC, abstractmethod
from math import ceil, floor

from schemdraw import Drawing
from schemdraw.elements import Element, ElementDrawing, Label
from schemdraw.flow import *
from schemdraw.util import XY, Point

from blocks import Block


class Renderer(ABC):
    def __init__(self, min_dims=(3, 2)) -> None:
        super().__init__()
        self.min_dims = min_dims

    def render_element(
        self,
        element: Element,
        drawing: Drawing,
        block: Block,
        render_dict: dict[str, "Renderer"],
    ) -> tuple[XY, XY]:
        drawing += element
        return element.N, element.S

    def compile(self, block: Block) -> Element:
        label = self.label(block)
        dims = tuple(map(max, zip(self.min_dims, Renderer.get_size(label))))
        return self.supplier(block, **{'w': dims[0], 'h': dims[1]}).label(label)

    def label(self, block: Block) -> str:
        return block.tooltip

    @abstractmethod
    def supplier(self, block: Block, **kwargs) -> Element:
        pass

    def render(self, drawing, block, render_dict: dict[str, "Renderer"]) -> tuple:
        return self.render_element(self.compile(block), drawing, block, render_dict)

    @staticmethod
    def merge_block(blocks: list[Block], render_dict: dict[str, "Renderer"]) -> Element:
        with Drawing(show=False) as context:
            context.config(unit=1)
            if blocks:
                prev_anchor: XY | None = None
                start_anchor: XY | None = None
                for i in range(len(blocks)):
                    block = blocks[i]
                    renderer = render_dict[block.type]
                    element = renderer.compile(block)
                    if prev_anchor:
                        element = element.at(prev_anchor)
                    anchors = renderer.render_element(
                        element, context, block, render_dict
                    )
                    prev_anchor = anchors[1]
                    if i == 0:
                        start_anchor = anchors[0]
                    if i < len(blocks) - 1:
                        context += (arrow := Arrow().at(prev_anchor).down())
                        prev_anchor = arrow.end
                assert prev_anchor and start_anchor
                # Create North anchor
                context.move_from(Point(start_anchor))
                context.set_anchor("N")
                # Create South anchor
                context.move_from(Point(prev_anchor))
                context.set_anchor("S")

                # Compute east and west anchors
                basis = Point((0, 0))
                bbox = context.get_bbox()
                half_height = (bbox.ymax - bbox.ymin) / 2
                context.move_from(basis, bbox.xmin, bbox.ymin + half_height)
                context.set_anchor("W")

                context.move_from(basis, bbox.xmax, bbox.ymin + half_height)
                context.set_anchor("E")

            context.move_from(Point(context.anchors["S"]))

        return ElementDrawing(context)

    @staticmethod
    def get_size(text) -> tuple[float, float]:
        with Drawing() as d:
            d += Label().label(text).right()
        box = ElementDrawing(d).get_bbox(includetext=True)
        return (
            ceil(box.xmax) - floor(box.xmin),
            box.ymax - box.ymin
        )
