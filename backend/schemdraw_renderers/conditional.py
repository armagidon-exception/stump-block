from typing import Self
from schemdraw import Drawing
from schemdraw.elements import Element, ElementDrawing
from schemdraw.flow import Decision, Wire
from schemdraw.util import XY
from backend.schemdraw_renderers import Renderer
from blocks import Block


class Conditional(Renderer):
    def render_element(
        self,
        element: Element,
        drawing: Drawing,
        block: Block,
        render_dict: dict[str, Self],
    ) -> XY | tuple[Element, str]:
        drawing += element
        conseq_route = block.routes["consequence"]
        alter_route = block.routes["alternative"]
        conseq_anchor = element.W
        alter_anchor = element.E
        if conseq_route:
            for i in range(len(conseq_route)):
                conseq_block = conseq_route[i]
                if conseq_block.type not in render_dict:
                    continue
                conseq_element = (
                    render_dict[conseq_block.type].produce(conseq_block).anchor("N")
                )
                if i == 0:
                    drawing.move_from(element.W, -2, -1)

                    drawing += Wire("-|", arrow="->").at(element.W).to(drawing.here)
                else:
                    conseq_element = conseq_element.at(conseq_anchor)
                conseq_anchor = render_dict[conseq_block.type].render_element(
                    conseq_element, drawing, conseq_block, render_dict
                )

        if alter_route:
            for i in range(len(alter_route)):
                alter_block = alter_route[i]
                if alter_block.type not in render_dict:
                    continue
                alter_element = (
                    render_dict[alter_block.type].produce(alter_block).anchor("N")
                )
                if i == 0:
                    drawing.move_from(element.E, 2, -1)
                    drawing += Wire("-|", arrow="->").at(element.E).to(drawing.here)
                else:
                    alter_element = alter_element.at(alter_anchor)
                alter_anchor = render_dict[alter_block.type].render_element(
                    alter_element, drawing, alter_block, render_dict
                )

        drawing += (connective := Wire("n", -1).at(conseq_anchor).to(alter_anchor))

        return connective.mid

    def produce(self, block: Block) -> Element:
        return Decision(W="yes", E="no").label(block.tooltip)
