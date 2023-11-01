from schemdraw.elements import Element
from schemdraw.flow import Box, Data, Subroutine, Terminal

from backend.schemdraw_renderers import Renderer
from blocks import Block


class BoxRenderer(Renderer):

    def supplier(self, block: Block, **kwargs) -> Element:
        return Box(**kwargs)


class SubroutineRenderer(Renderer):
    def __init__(self) -> None:
        super().__init__((3.5, 2))

    def supplier(self, block: Block, **kwargs) -> Element:
        return Subroutine(**kwargs)

class TerminalRenderer(Renderer):
    def __init__(self, title: str, create_arrow: bool = True) -> None:
        super().__init__((3, 1.25))
        self.title = title
        self.create_arrow = create_arrow

    def supplier(self, block: Block, **kwargs) -> Element:
        return Terminal(**kwargs)

    def label(self, block: Block) -> str:
        return self.title


class InputRenderer(Renderer):

    def supplier(self, block: Block, **kwargs) -> Element:
        return Data(**kwargs)

    def label(self, block: Block) -> str:
        return f"Enter: {block.tooltip}"


class OutputRenderer(Renderer):

    def supplier(self, block: Block, **kwargs) -> Element:
        return Data(**kwargs)


    def label(self, block: Block) -> str:
        return f"Output: {block.tooltip}"

