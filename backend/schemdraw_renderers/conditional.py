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
                dx = -width / 2
                base_anchor = base_element.W
            elif type == "alternative":
                dx = width / 2
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

        if conseq_height > alter_height:
            arrow = drawing.add(Line().down().at(conseq_anchor))
            conseq_anchor = arrow.end
            arrow = drawing.add(Line().down().at(alter_anchor).toy(conseq_anchor))
            alter_anchor = arrow.end
        else:
            arrow = drawing.add(Line().down().at(alter_anchor))
            alter_anchor = arrow.end
            arrow = drawing.add(Line().down().toy(alter_anchor).at(conseq_anchor))
            conseq_anchor = arrow.end

        connective = drawing.add(Line().at(conseq_anchor).to(alter_anchor))

        return (element.N, connective.center)

    def supplier(self, block: Block, **kwargs) -> Element:
        return Decision(W="yes", E="no", **kwargs)
