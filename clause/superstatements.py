
from clause import Clause
from clause.utils import AnyClause
from command import BreakStatement, CloseChunk, ContinueStatement, OpenChunk, PlaceBlock, ReturnStatement
from state import StateType
from traverser import TraverseContext
from utils import capture_within

# Used for named blocks

class StatementClause(Clause):
    def __init__(self, base: Clause, working_states: set[StateType]) -> None:
        super().__init__()
        self.base = base
        self.working_states = working_states

    def trigger_enter(self, context: TraverseContext) -> bool:
        assert context.current_node.parent
        if (not context.current_name in context.last_state.routes
                and not context.last_state.marker.id == context.current_node.parent.id):
            return False
        return self.base.trigger_enter(context)

    def handle_enter(self, context: TraverseContext):
        assert context.current_name
        context.commands.append(OpenChunk(context.current_name))
        context.save_state(StateType.LINEAR, [])
        self.base.handle_enter(context)

    def handle_exit(self, context: TraverseContext):
        self.base.handle_exit(context)
        context.commands.append(CloseChunk())

    def states(self) -> set[StateType]:
        return self.working_states

# Used for unnamed blocks

class UnnamedStatementClause(Clause):
    def __init__(self, base: Clause, working_states: set[StateType]) -> None:
        super().__init__()
        self.base = base
        self.working_states = working_states

    def trigger_enter(self, context: TraverseContext) -> bool:
        assert context.current_node.parent
        if (not context.last_state.marker.id == context.current_node.parent.id):
            return False
        return self.base.trigger_enter(context)

    def handle_enter(self, context: TraverseContext):
        context.commands.append(OpenChunk(context.last_state.routes[0]))
        context.save_state(StateType.LINEAR, [])
        self.base.handle_enter(context)

    def handle_exit(self, context: TraverseContext):
        self.base.handle_exit(context)
        context.commands.append(CloseChunk())

    def states(self) -> set[StateType]:
        return self.working_states


class IfStatementClause(AnyClause):
    def __init__(self) -> None:
        super().__init__({StateType.LINEAR})

    def handle_enter(self, context: TraverseContext):
        assert (condition := context.current_node.child_by_field_name("condition"))
        tooltip = condition.text.decode()
        context.commands.append(PlaceBlock("condition", condition=tooltip))
        context.save_state(StateType.IF_STATEMENT, [
                           "consequence", "alternative"])

# Loops

class WhileStatement(AnyClause):
    def __init__(self) -> None:
        super().__init__({StateType.LINEAR})

    def handle_enter(self, context: TraverseContext):
        assert (condition := context.current_node.named_child(0))
        tooltip = condition.text.decode()
        context.commands.append(PlaceBlock('preloop', condition=tooltip))
        context.save_state(StateType.PRE_LOOP, ["body"])


class DoStatement(AnyClause):
    def __init__(self) -> None:
        super().__init__({StateType.LINEAR})

    def handle_enter(self, context: TraverseContext):
        assert (condition := context.current_node.named_child(1))
        tooltip = condition.text.decode()
        context.commands.append(PlaceBlock('postloop', condition=tooltip))
        context.save_state(StateType.POST_LOOP, ["body"])


class ForStatement(AnyClause):
    def __init__(self) -> None:
        super().__init__({StateType.LINEAR})

    def handle_enter(self, context: TraverseContext):
        init = context.current_node.child_by_field_name('initializer')
        cond = context.current_node.child_by_field_name('condition')
        upda = context.current_node.child_by_field_name('update')
        tooltip = ""
        tooltip += (init.text.decode() if init else "") + ";"
        tooltip += (" " + cond.text.decode() if cond else "") + ";"
        tooltip += (" " + upda.text.decode() if upda else "")
        context.commands.append(PlaceBlock(
            'parameter_loop', condition=tooltip))
        context.save_state(StateType.PARAMETER_LOOP, ["body"])


class ForEachStatement(AnyClause):
    def __init__(self) -> None:
        super().__init__({StateType.LINEAR})

    def handle_enter(self, context: TraverseContext):
        init = context.current_node.child_by_field_name('type')
        upda = context.current_node.child_by_field_name('right')
        assert init and upda
        tooltip = ' '.join(map(lambda x: x.text.decode(),
                           capture_within(init, upda)))
        context.commands.append(PlaceBlock(
            'iterator', condition=tooltip))
        context.save_state(StateType.ITERATOR, ["body"])


# Control flow operators

class ReturnStatementClause(AnyClause):
    def __init__(self) -> None:
        super().__init__({StateType.LINEAR})

    def handle_enter(self, context: TraverseContext):
        context.commands.append(ReturnStatement())


class BreakStatementClause(AnyClause):
    def __init__(self) -> None:
        super().__init__({StateType.LINEAR})

    def handle_enter(self, context: TraverseContext):
        context.commands.append(BreakStatement())


class ContinueStatementClause(AnyClause):
    def __init__(self) -> None:
        super().__init__({StateType.LINEAR})

    def handle_enter(self, context: TraverseContext):
        context.commands.append(ContinueStatement())
