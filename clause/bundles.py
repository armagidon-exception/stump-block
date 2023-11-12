from clause.superstatements import *
from clause.expressions import ExpressionStatementClause

SUPER_STATEMENTS = {
    "do_statement": DoStatement(),
    "if_statement": IfStatementClause(),
    "while_statement": WhileStatement(),
    "for_statement": ForStatement(),
    "for_each_statement": ForEachStatement(),
    "expression_statement": ExpressionStatementClause(),
    "return_statement": ReturnStatementClause(),
    "break_statement": BreakStatementClause(),
    "continue_statement": ContinueStatementClause(),
}

ALL_STATEMENTS = {
    "block": AnyClause(),
    "empty_statement": AnyClause(),
    **SUPER_STATEMENTS,
}
