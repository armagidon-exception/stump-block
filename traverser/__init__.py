from abc import ABC, abstractmethod

from tree_sitter import Node, TreeCursor

from state import State


class TraverseContext:
    def __init__(
        self,
        current_node: Node,
        current_name: str | None,
        state_stack: list[State],
        commands: list[State],
        enter: bool,
    ) -> None:
        self.current_node = current_node
        self.current_name = current_name
        self.state_stack = state_stack
        self.enter = enter
        self.commands = commands


class TraverseHandler(ABC):
    @abstractmethod
    def handle_discover(self, cursor: TreeCursor):
        pass

    @abstractmethod
    def handle_retreating(self, cursor: TreeCursor):
        pass


def traverse(cursor: TreeCursor, handler: TraverseHandler):
    handler.handle_discover(cursor)
    while True:
        if cursor.goto_first_child() or cursor.goto_next_sibling():
            handler.handle_discover(cursor)
        else:
            while True:
                if not cursor.goto_parent():
                    return
                handler.handle_retreating(cursor)
                if cursor.goto_next_sibling():
                    handler.handle_discover(cursor)
                    break
