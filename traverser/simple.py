from tree_sitter import TreeCursor
from clause import Clause
from clause.utils import MetaCommentStateClause
from command import Command
from state import State, StateType
from traverser import TraverseContext, Traverser


class ParserTraverser(Traverser):
    def __init__(self) -> None:
        super().__init__()
        self.state_stack: list[State] = []
        self.clauses: list[Clause] = [
            MetaCommentStateClause('input', StateType.INPUT)
        ]
        self.commands: list[Command] = []

    def handle_discover(self, cursor: TreeCursor):
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
                return clause.handle(context)
