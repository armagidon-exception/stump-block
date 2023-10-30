from abc import ABC, abstractmethod
from typing import Self

from schemdraw import Drawing
from schemdraw.elements import Element, ElementDrawing
from schemdraw.flow import *
from schemdraw.util import XY, Point

from blocks import Block


class Renderer(ABC):
    @abstractmethod
    def render_element(
        self,
        element: Element,
        drawing: Drawing,
        block: Block,
        render_dict: dict[str, Self],
    ) -> tuple[XY, XY]:
        pass

    @abstractmethod
    def produce(self, block: Block) -> Element:
        pass

    def render(self, drawing, block, render_dict) -> tuple:
        return self.render_element(self.produce(block), drawing, block, render_dict)

    @classmethod
    def merge_block(cls, blocks: list[Block], render_dict: dict[str, Self]) -> Element:
        with Drawing(show=False) as context:

            context.config(unit=1)
            if blocks:
                prev_anchor: XY | None = None
                start_anchor: XY | None = None
                for i in range(len(blocks)):
                    block = blocks[i]
                    renderer = render_dict[block.type]
                    element = renderer.produce(block)
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

            context.move_from(Point(context.anchors['S']))

        return ElementDrawing(context)
