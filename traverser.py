from tree_sitter import TreeCursor, Node
from abc import ABC, abstractmethod


class TraverseHandler(ABC):
    @abstractmethod
    def handle(self, cursor: TreeCursor, node: Node, text: str, enter: bool):
        pass

    def handle_compact(self, cursor: TreeCursor, enter: bool):
        self.handle(cursor, cursor.node, cursor.node.text.decode(), enter)

def traverse(cursor: TreeCursor, handler: TraverseHandler):
    while True:
        if cursor.goto_first_child():
            handler.handle_compact(cursor, True)
        elif cursor.goto_next_sibling():
            handler.handle_compact(cursor, True)
        elif cursor.goto_parent():
            handler.handle_compact(cursor, False)
            while not cursor.goto_next_sibling():
                if not cursor.goto_parent():
                    return
                handler.handle_compact(cursor, False)

            handler.handle_compact(cursor, True)
        else:
            return
