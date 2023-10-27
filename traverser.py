from tree_sitter import TreeCursor, Node
from abc import ABC, abstractmethod


class TraverseHandler(ABC):
    @abstractmethod
    def _handle_enter(self, cursor: TreeCursor, current: Node, prev: Node | None, text: str):
        pass

    @abstractmethod
    def _handle_leave(self, cursor: TreeCursor, current: Node, prev: Node | None, text: str):
        pass

    def handle_enter(self, cursor: TreeCursor, prev: Node | None = None):
        self._handle_enter(cursor, cursor.node, prev, cursor.node.text.decode())

    def handle_leave(self, cursor: TreeCursor, prev: Node | None = None):
        self._handle_leave(cursor, cursor.node, prev, cursor.node.text.decode())


def traverse(cursor: TreeCursor, handler: TraverseHandler):
    prev = cursor.node
    while True:
        if cursor.goto_first_child():
            handler.handle_enter(cursor)
        elif cursor.goto_next_sibling():
            handler.handle_enter(cursor)
        elif cursor.goto_parent():
            handler.handle_leave(cursor, prev)
            while not cursor.goto_next_sibling():
                prev = cursor.node
                if not cursor.goto_parent():
                    return
                handler.handle_leave(cursor, prev)

            handler.handle_enter(cursor)
        else:
            return
        prev = cursor.node
