from abc import ABC, abstractmethod

from tree_sitter import TreeCursor, Node


class TraverseHandler(ABC):
    @abstractmethod
    def handle_discover(
            self, cursor: TreeCursor, prev: Node | None, prev_name: str | None
    ):
        pass

    @abstractmethod
    def handle_retreating(
            self, cursor: TreeCursor, prev: Node | None, prev_name: str | None
    ):
        pass


def traverse(cursor: TreeCursor, handler: TraverseHandler):
    prev: Node | None = None
    prev_name: str | None = None

    def handle(discover: bool):
        nonlocal prev, prev_name
        if discover:
            handler.handle_discover(cursor, prev, prev_name)
        else:
            handler.handle_retreating(cursor, prev, prev_name)
        prev = cursor.node
        prev_name = cursor.field_name

    handle(True)
    while True:
        if cursor.goto_first_child():
            handle(True)
        elif cursor.goto_next_sibling():
            handle(True)
        else:
            while True:
                if not cursor.goto_parent():
                    return
                handle(False)
                if cursor.goto_next_sibling():
                    handle(True)
                    break
