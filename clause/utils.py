from functools import reduce
from typing import Callable

from tree_sitter import Node

from clause import Clause
from state import StateType
from traverser import TraverseContext

CommentHandler = Callable[[TraverseContext, list[str]], None]


def _prep_comment(input: str):
    return input.removeprefix("//").strip()


class DelegatedClause(Clause):
    def __init__(self, child: Clause) -> None:
        super().__init__()
        self.child = child

    def states(self):
        return self.child.states()

    def handle_enter(self, context: TraverseContext):
        self.child.handle_enter(context)

    def handle_exit(self, context: TraverseContext):
        self.child.handle_exit(context)

    def trigger_enter(self, context: TraverseContext) -> bool:
        return self.child.trigger_enter(context)

    def trigger_exit(self, context: TraverseContext) -> bool:
        return self.child.trigger_exit(context)


class JoinClause(Clause):
    def __init__(self, *clauses: Clause) -> None:
        super().__init__()
        self.clauses = clauses

    def states(self):
        return set(reduce(lambda x1, x2: x1 & x2.states(), self.clauses, set()))

    def handle_enter(self, context: TraverseContext):
        print(self)
        for clause in self.clauses:
            clause.handle_enter(context)

    def handle_exit(self, context: TraverseContext):
        for clause in self.clauses:
            clause.handle_exit(context)

    def trigger_enter(self, context: TraverseContext) -> bool:
        return bool(self.clauses) and all(
            map(lambda x: x.trigger_enter(context), self.clauses)
        )

    def trigger_exit(self, context: TraverseContext) -> bool:
        return bool(self.clauses) and all(
            map(lambda x: x.trigger_exit(context), self.clauses)
        )


class MetaCommentClause(Clause):
    def __init__(self, id: str, closable=False) -> None:
        super().__init__()
        self.id = id
        self.closable = closable

    def trigger_enter(self, context: TraverseContext) -> bool:
        if not context.current_type == "comment":
            return False

        input_string = _prep_comment(context.text)
        if self.closable and input_string in [f"{self.id}-start", f"{self.id}-end"]:
            return True
        elif input_string == self.id:
            return True
        return False

    def handle_enter(self, context: TraverseContext):
        input_string = _prep_comment(context.text)
        if self.closable and input_string == f"{self.id}-start":
            self.tag_enter(context)
        elif input_string == f"{self.id}-end":
            self.tag_exit(context)
        elif input_string == self.id:
            self.tag_enter(context)

    def tag_enter(self, context: TraverseContext):
        pass

    def tag_exit(self, context: TraverseContext):
        pass

class AnyClause(Clause):
    def __init__(self, states: set[StateType] = set()) -> None:
        super().__init__()
        self.s = states

    def trigger_enter(self, context: TraverseContext) -> bool:
        return True

    def trigger_exit(self, context: TraverseContext) -> bool:
        return True

    def handle_enter(self, context: TraverseContext):
        ...

    def handle_exit(self, context: TraverseContext):
        ...

    def states(self) -> set[StateType]:
        return self.s


class BlockClause(DelegatedClause):
    def __init__(self, block_type, child: Clause = AnyClause()) -> None:
        super().__init__(child)
        self.child = child
        self.block_type = block_type

    def trigger_enter(self, context: TraverseContext) -> bool:
        return context.current_type == self.block_type and super().trigger_enter(
            context
        )

    def trigger_exit(self, context: TraverseContext) -> bool:
        return context.current_type == self.block_type and super().trigger_exit(context)
