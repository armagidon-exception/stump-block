from schemdraw import Drawing
from schemdraw.elements import Element
from schemdraw.flow import Arrow, Decision, Line, Wire
from schemdraw.util import XY
from backend.schemdraw_renderers import Renderer
from blocks import Block


class PreLoopRenderer(Renderer):
    def __init__(self, loop_back_y_offset=0.5) -> None:
        super().__init__((4, 2))
        self.loop_back_y_offset = loop_back_y_offset

    def supplier(self, block: Block, **kwargs) -> Element:
        return Decision(**kwargs)

    def render_element(
        self,
        element: Element,
        drawing: Drawing,
        block: Block,
        render_dict: dict[str, "Renderer"],
    ) -> tuple[XY, XY]:
        drawing += element.drop("S")
        route = block.routes["body"]
        loop_end_anchor = element.S
        k = 1
        if route:
            arrow = drawing.add(Arrow().down().at(element.S))
            body_el = drawing.add(
                Renderer.merge_block(route, render_dict)
                .anchor("N")
                .at(arrow.end)
                .right()
            )
            loop_end_anchor = body_el.S
            k = (Renderer.get_element_size(body_el)[0] / 2) + 1

        drawing += Line().down().at(loop_end_anchor)
        drawing += (
            loop := Wire("c", -k, "->").to(element.N, 0, self.loop_back_y_offset)
        )
        drawing += Line().at(element.E).right().length(drawing.unit)
        drawing += Line().down().toy(loop.start)

        return (element.N, drawing.here)



class PostLoopRenderer(Renderer):
    def __init__(self, loop_back_y_offset=0.5):
        super().__init__((4, 2))
        self.loop_back_y_offset = loop_back_y_offset

    def supplier(self, block: Block, **kwargs) -> Element:
        return Decision(**kwargs)

    def render_element(
        self,
        element: Element,
        drawing: Drawing,
        block: Block,
        render_dict: dict[str, "Renderer"],
    ) -> tuple[XY, XY]:
        route = block.routes["body"]
        k = 1
        loop_end_anchor = drawing.here
        loop_start_anchor = drawing.here
        if route:
            body_el = drawing.add(
                Renderer.merge_block(route, render_dict)
                .at(loop_end_anchor)
                .anchor("N")
                .right()
            )
            loop_end_anchor = body_el.S
            k = (Renderer.get_element_size(body_el)[0] / 2) + 1

        drawing.add(Arrow().down().at(loop_end_anchor))
        drawing += element
        drawing += Wire('c', -1, '->').at(element.W).to(loop_start_anchor, 0, self.loop_back_y_offset)
        return loop_start_anchor, element.S
