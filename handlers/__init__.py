from abc import ABC, abstractmethod

from tree_sitter import Node

from traverser_state import StateHolder


class StateHandler(ABC):

    @abstractmethod
    def _handle(self, current: Node, prev: Node | None, name: str | None, text: str, state_stack: list[StateHolder], enter: bool):
        pass
