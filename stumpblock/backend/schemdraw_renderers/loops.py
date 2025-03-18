from schemdraw import Drawing, SegmentPoly
from schemdraw.elements import Element
from schemdraw.flow import Arrow, Box, Decision, Line, Wire
from schemdraw.util import XY
from backend.schemdraw_renderers import Renderer
from blocks import Block


class PreLoopRenderer(Renderer):
    def __init__(self, loop_back_y_offset=0.5) -> None:
        super().__init__((4, 2))
        self.loop_back_y_offset = loop_back_y_offset

    def supplier(self, block: Block, **kwargs) -> Element:
        return Decision(**kwargs, S="yes", E="no")

    def render_element(
        self,
        element: Element,
        drawing: Drawing,
        block: Block,
        render_dict: dict[str, "Renderer"],
    ) -> tuple[XY, XY]:
        drawing.add(element.drop("S"))
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
            k = (Renderer.get_element_size(body_el)[0]) + 1

        drawing.add(Line().down().at(loop_end_anchor))
        drawing.add(
            loop := Wire("c", k=-k, arrow="->").to(element.N, 0, self.loop_back_y_offset)
        )
        drawing.add(Line().at(element.E).right().length(k))
        drawing.add(Line().down().toy(loop.start))

        return (element.N, drawing.here)


class PostLoopRenderer(Renderer):
    def __init__(self, loop_back_y_offset=0.5):
        super().__init__((4, 2))
        self.loop_back_y_offset = loop_back_y_offset

    def supplier(self, block: Block, **kwargs) -> Element:
        return Decision(**kwargs, W="yes", S="no")

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
            k = body_el.W.x

        drawing.add(Arrow().down().at(loop_end_anchor))
        drawing.add(element)
        drawing.add(
            Wire("c", k=-abs(k - element.W.x) - 1, arrow="->")
            .at(element.W)
            .to(loop_start_anchor, 0, self.loop_back_y_offset)
        )
        return loop_start_anchor, element.S


class LoopElement(Box):
    _element_defaults = {
        'w': 3,
        'h':1.5,
        'lblloc': 'center',
        'lblofst': 0,
        'theta':0
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_anchors(self):
        super()._set_anchors()
        w, h = self.params['w'], self.params['h']
        x = w - h
        self.anchors['N'] = ( 0, 0 )
        self.anchors['S'] = ( 0, -h )
        self.anchors['E'] = ( 0.5*x + 0.5*h, -0.5*h )
        self.anchors['W'] = ( -0.5*x - 0.5*h, -0.5*h )
        self.anchors['center'] = ( 0, -0.5*h )

    def _set_segments(self):
        super()._set_segments()
        self.segments.clear()
        w, h = self.params['w'], self.params['h']

        x = w - h
        self.segments.append(
            SegmentPoly(
                [
                    (0, 0),
                    (0.5 * x, 0),
                    (0.5 * x + 0.5 * h, -0.5 * h),
                    (0.5 * x, -h),
                    (-0.5 * x, -h),
                    (-0.5 * x - 0.5 * h, -0.5 * h),
                    (-0.5 * x, 0),
                ]
            )
        )




class ParameterLoopRenderer(Renderer):
    def __init__(self) -> None:
        super().__init__((5, 1.5))

    def render_element(self, element: Element, drawing: Drawing, block: Block, render_dict: dict[str, "Renderer"]) -> tuple[XY, XY]:
        drawing.add(element.drop("S"))
        route = block.routes["body"]
        loop_end_anchor = element.S
        k = element.params['w']
        if route:
            arrow = drawing.add(Arrow().down().at(element.S))
            body_el = drawing.add(Renderer.merge_block(route, render_dict).anchor("N").at(arrow.end).right())
            loop_end_anchor = body_el.S
            # print(loop_end_anchor, Renderer.get_element_size(body_el), body_el.S[0] - body_el.W[0])
            k = body_el.S[0] - body_el.W[0] + 1
            # k = (Renderer.get_element_size(body_el)[0]) + 1

        iterout: Line = Line().down().length(2).at(loop_end_anchor).anchor('start')
        drawing.add(iterout)
        wi = Wire('c', k=-k, arrow='->').at(iterout.end).to(element.W)
        drawing.add(wi)

        k = body_el.E[0] - body_el.S[0] + 1
        drawing.add(Wire('-|', arrow='-').at(element.E).to((iterout.end[0] + k, iterout.end[1])))

        return (element.N, drawing.here)

    def supplier(self, block: Block, **kwargs) -> Element:
        return LoopElement()
