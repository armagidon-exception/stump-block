from abc import ABC, abstractmethod
from typing import Self
from schemdraw import Drawing
from schemdraw.elements import Element

from schemdraw.types import XY

from blocks import Block


class Renderer(ABC):

    @abstractmethod
    def render_element(self, element: Element, drawing: Drawing, block: Block, render_dict: dict[str, Self]) -> XY | tuple[Element, str]:
        pass

    @abstractmethod
    def produce(self, block: Block) -> Element:
        pass

    def render(self, drawing, block, render_dict) -> XY | tuple[Element, str]:
        return self.render_element(self.produce(block), drawing, block, render_dict)
