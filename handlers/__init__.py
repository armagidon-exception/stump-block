from abc import ABC, abstractmethod

from tree_sitter import Node, TreeCursor

from traverser_state import StateHolder


class StateHandler(ABC):

    @abstractmethod
    def _handle(self, current: Node, name: str | None, text: str, state_stack: list[StateHolder], enter: bool):
        pass

    def handle(self, cursor: TreeCursor, state_stack: list[StateHolder], enter: bool):
        self._handle(cursor.node, cursor.field_name, cursor.node.text.decode(), state_stack, enter)
