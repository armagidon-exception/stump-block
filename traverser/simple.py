from tree_sitter import TreeCursor
from command import Command
from data import Clause
from state import State
from traverser import TraverseContext, TraverseHandler


class ParserTraverser(TraverseHandler):
    def __init__(self, state_stack: list[State]) -> None:
        super().__init__()
        self.state_stack = state_stack
        self.clauses: list[Clause] = []
        self.commands: list[Command] = []

    def handle_discover(self, cursor: TreeCursor) -> bool:
        context = TraverseContext(
            cursor.node, cursor.field_name, self.state_stack, self.commands, True
        )
        for clause in self.clauses:
            if clause.trigger(context):
                return clause.handle(context)

        return False

    def handle_retreating(self, cursor: TreeCursor):
        context = TraverseContext(
            cursor.node, cursor.field_name, self.state_stack, self.commands, False
        )
        for clause in self.clauses:
            if clause.trigger(context):
                clause.handle(context)
