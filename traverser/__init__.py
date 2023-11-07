from abc import ABC, abstractmethod

from tree_sitter import Node, TreeCursor
from command import Command
from state import State

class TraverseContext:
    def __init__(
        self,
        current_node: Node,
        current_name: str | None,
        state_stack: list[State],
        commands: list[Command],
        enter: bool,
    ) -> None:
        self.current_node = current_node
        self.current_name = current_name
        self.state_stack = state_stack
        self.enter = enter
        self.commands = commands

    @property
    def last_state(self):
        if not self.state_stack:
            return None
        return self.state_stack[-1]

    @property
    def text(self):
        return self.current_node.text.decode()

    def first_child_by_type(self, type: str):
        for child in self.current_node.children:
            if child.type == type:
                return child
        return None


class Traverser(ABC):
    @abstractmethod
    def handle_discover(self, cursor: TreeCursor) -> bool:
        pass

    @abstractmethod
    def handle_retreating(self, cursor: TreeCursor):
        pass

    def traverse(self, cursor: TreeCursor):
        self.handle_discover(cursor)
        while True:
            if cursor.goto_first_child() or cursor.goto_next_sibling():
                self.handle_discover(cursor)
            else:
                while True:
                    if not cursor.goto_parent():
                        return
                    self.handle_retreating(cursor)
                    if cursor.goto_next_sibling():
                        self.handle_discover(cursor)
                        break

