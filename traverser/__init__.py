from abc import ABC, abstractmethod

from tree_sitter import Node, TreeCursor

from command import Command
from state import State, StateType


class TraverseContext:
    def __init__(
            self,
            current_node: Node,
            current_name: str | None,
            state_stack: list[State],
            commands: list[Command],
            mark=False,
    ) -> None:
        self.current_node = current_node
        self.current_name = current_name
        self.state_stack = state_stack
        self.commands = commands
        self.mark = mark

    @property
    def last_state(self):
        return self.state_stack[-1]

    @property
    def text(self):
        return self.current_node.text.decode()

    @property
    def current_type(self):
        return self.current_node.type

    def save_state(self, state: StateType, routes: list[str] = []):
        self.state_stack.append(
            State(state, self.commands, self.current_node, routes))
        self.mark = True


class Traverser(ABC):
    def __init__(self, cursor: TreeCursor) -> None:
        super().__init__()
        self.cursor = cursor

    @abstractmethod
    def handle_discover(self) -> bool:
        pass

    @abstractmethod
    def handle_retreating(self):
        pass

    def traverse(self):
        self.handle_discover()
        while True:
            if self.cursor.goto_first_child() or self.cursor.goto_next_sibling():
                self.handle_discover()
            else:
                while True:
                    if not self.cursor.goto_parent():
                        return
                    self.handle_retreating()
                    if self.cursor.goto_next_sibling():
                        self.handle_discover()
                        break


def first_child_by_type(self, type: str) -> Node | None:
    for child in self.children:
        if child.type == type:
            return child
    return None


setattr(Node, "first_child_by_type", first_child_by_type)
