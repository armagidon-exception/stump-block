from abc import ABC, abstractmethod

from tree_sitter import Node
from blocks import Block

from traverser_state import StateHolder


class TraverseContext:
    def __init__(
        self,
        current_node: Node,
        prev_node: Node,
        current_name: str | None,
        prev_name: str | None,
        state_stack: list[StateHolder],
        enter: bool,
    ) -> None:
        self.current_node = current_node
        self.prev_node = prev_node
        self.current_name = current_name
        self.prev_name = prev_name
        self.state_stack = state_stack
        self.enter = enter


class StateHandler(ABC):
    @abstractmethod
    def _handle(self, context: TraverseContext):
        pass

    @staticmethod
    def get_current_route(context: TraverseContext):
        return context.state_stack[-1].route

    @staticmethod
    def get_last_block(context: TraverseContext):
        return context.state_stack[-1].route[-1]
