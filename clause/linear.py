from clause import Clause
from clause.expressions import ExpressionStatementClause
from clause.superstatements import BreakStatementClause, ContinueStatementClause, DoStatement, ForEachStatement, ForStatement, IfStatementClause, ReturnStatementClause, WhileStatement
from clause.utils import MetaCommentClause, AnyClause
from command import (
    BreakStatement,
    CloseChunk,
    ContinueStatement,
    OpenChunk,
    PlaceBlock,
    ReturnStatement,
)
from state import StateType
from traverser import TraverseContext
from utils import capture_within


class DeclarationClause(Clause):
    def trigger_enter(self, context: TraverseContext) -> bool:
        if not context.current_type == "variable_declaration":
            return False
        elif not context.current_node.parent:
            return False
        elif not context.current_node.parent.type == "local_declaration_statement":
            return False
        else:
            return True

    def handle_enter(self, context: TraverseContext):
        context.commands.append(PlaceBlock(
            "declaration", tooltip=context.text))


class InputMetaClause(MetaCommentClause):
    def __init__(self) -> None:
        super().__init__("input", True)

    def tag_enter(self, context: TraverseContext):
        context.save_state(StateType.INPUT, [])

    def tag_exit(self, context: TraverseContext):
        context.state_stack.pop()

    def states(self) -> set[StateType]:
        return super().states() | {StateType.INPUT}


class InputClause(Clause):
    def states(self) -> set[StateType]:
        return {StateType.INPUT}

    def trigger_enter(self, context: TraverseContext) -> bool:
        return context.current_type == "variable_declarator"

    def handle_enter(self, context: TraverseContext):
        name = context.current_node.child_by_field_name("name")
        assert name
        context.commands.append(PlaceBlock(
            "input", variable_name=name.text.decode()))


