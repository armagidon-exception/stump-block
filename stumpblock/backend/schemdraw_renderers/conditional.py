from schemdraw import Drawing
from schemdraw.elements import Element
from schemdraw.flow import Arrow, Decision, Line, Wire
from schemdraw.util import XY

from backend.schemdraw_renderers import Renderer
from blocks import Block


class ConditionalRenderer(Renderer):
    def __init__(self, branch_length: float = 1) -> None:
        super().__init__((4, 2))
        self.branch_length = min(1, branch_length)

    def render_route(
        self,
        route: list[Block],
        drawing: Drawing,
        render_dict,
        base_element: Element,
        type: str,
    ):
        if route:
            conseq_element = Renderer.merge_block(route, render_dict).right()
            bbox = conseq_element.get_bbox()
            width = bbox.xmax - bbox.xmin
            conseq_height = bbox.ymax - bbox.ymin

            dx = 0
            base_anchor = None
            if type == "consequence":
                dx = -width
                base_anchor = base_element.W
            elif type == "alternative":
                dx = width
                base_anchor = base_element.E
            dx *= self.branch_length

            assert base_anchor
            conseq_element = conseq_element.anchor("N").at(base_anchor, dx, -2)

            drawing.add(conseq_element)

            drawing.add(Wire("-|", arrow="->").at(base_anchor).to(conseq_element.N))
            return conseq_element.S, conseq_height
        elif type == "consequence":
            return base_element.W, 0
        elif type == "alternative":
            return base_element.E, 0
        else:
            assert False

    def render_element(
        self,
        element: Element,
        drawing: Drawing,
        block: Block,
        render_dict: dict[str, Renderer],
    ) -> XY | tuple[Element, str]:
        drawing.add(element.drop("S"))
        conseq_route = block.routes["consequence"]
        alter_route = block.routes["alternative"]

        conseq_anchor, conseq_height = self.render_route(
            conseq_route, drawing, render_dict, element, "consequence"
        )

        alter_anchor, alter_height = self.render_route(
            alter_route, drawing, render_dict, element, "alternative"
        )

        conseq_ends = conseq_route[-1].type in ["return", "end"] if len(conseq_route) > 0 else False
        alter_ends = alter_route[-1].type in ["return", "end"] if len(alter_route) > 0 else False

        if conseq_height > alter_height:
            if not conseq_ends:
                arrow = drawing.add(Line().down().at(conseq_anchor))
                conseq_anchor = arrow.end
            if not alter_ends:
                arrow = drawing.add(Line().down().at(alter_anchor).toy(conseq_anchor))
                alter_anchor = arrow.end
        else:
            if not conseq_ends:
                arrow = drawing.add(Line().down().at(alter_anchor))
                alter_anchor = arrow.end
            if not alter_ends:
                arrow = drawing.add(Line().down().toy(alter_anchor).at(conseq_anchor))
                conseq_anchor = arrow.end

        if not conseq_ends and not alter_ends:
            connective = drawing.add(Line().at(conseq_anchor).to(alter_anchor))
            return (element.N, connective.center)
        elif not conseq_ends:
            return (element.N, conseq_anchor)
        elif not alter_ends:
            return (element.N, alter_anchor)
        else:
            return (element.N, conseq_anchor)

    def supplier(self, block: Block, **kwargs) -> Element:
        return Decision(W="yes", E="no", **kwargs)
