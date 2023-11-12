import logging

from tree_sitter import TreeCursor

from clause import Clause
from clause.bundles import *
from clause.expressions import AssignmentExpressionClause, OutputClause, SubroutineClause
from clause.linear import DeclarationClause, InputClause, InputMetaClause
from clause.superstatements import StatementClause, UnnamedStatementClause
from clause.utils import BlockClause
from command import Command
from state import State, StateType
from traverser import TraverseContext, Traverser


class ParserTraverser(Traverser):
    def __init__(self, cursor: TreeCursor) -> None:
        super().__init__(cursor)
        self.clauses: list[Clause] = [
            InputMetaClause(),
            InputClause(),
            DeclarationClause(),
            BlockClause('invocation_expression',
                        OutputClause('Console.WriteLine')),
            BlockClause('invocation_expression',
                        OutputClause('Console.Write')),
            BlockClause('invocation_expression', SubroutineClause()),
            BlockClause('assignment_expression', AssignmentExpressionClause())
        ]

        for statement_type, statement_clause in SUPER_STATEMENTS.items():
            self.clauses.append(BlockClause(statement_type, statement_clause))

        for statement_type, statement_clause in ALL_STATEMENTS.items():
            self.clauses.append(StatementClause(BlockClause(
                statement_type, statement_clause), {StateType.IF_STATEMENT, StateType.PARAMETER_LOOP, StateType.ITERATOR}))
            self.clauses.append(UnnamedStatementClause(BlockClause(
                statement_type, statement_clause), {StateType.PRE_LOOP, StateType.POST_LOOP}))

        self.commands: list[Command] = []
        self.state_stack: list[State] = [
            State(StateType.LINEAR, self.commands, self.cursor.node)
        ]
        self.marker_clauses: dict[int, Clause] = {}

    def handle_discover(self):
        if not self.cursor.node.is_named:
            return

        for clause in self.clauses:
            context = TraverseContext(
                self.cursor.node,
                self.cursor.field_name,
                self.state_stack,
                self.commands,
            )
            if (clause.trigger_enter(context) and context.last_state.type in clause.states()):
                logging.info(
                    f"Node of type '{context.current_node.type}' was handled by handler '{clause.__class__.__name__}' >")
                clause.handle_enter(context)
                if context.mark:
                    self.marker_clauses[self.cursor.node.id] = clause
                break

    def handle_retreating(self):
        if not self.cursor.node.is_named:
            return

        context = TraverseContext(
            self.cursor.node,
            self.cursor.field_name,
            self.state_stack,
            self.commands,
        )
        while self.state_stack and context.last_state.marker.id == context.current_node.id:
            prev_state = self.state_stack.pop()
            if prev_state.marker.id in self.marker_clauses:
                clause = self.marker_clauses[prev_state.marker.id]
                logging.info(
                    f"Node of type '{context.current_node.type}' was handled by handler '{clause.__class__.__name__}' <")
                clause.handle_exit(context)
                del self.marker_clauses[prev_state.marker.id]
            if not self.state_stack:
                return
