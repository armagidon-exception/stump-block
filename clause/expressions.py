from clause.utils import AnyClause
from command import PlaceBlock
from state import StateType
from traverser import TraverseContext


class ExpressionStatementClause(AnyClause):
    def __init__(self) -> None:
        super().__init__({StateType.LINEAR})

    def handle_enter(self, context: TraverseContext):
        return context.save_state(StateType.EXPRESSION, [])


class InvocationExpressionClause(AnyClause):
    def __init__(self, function_name: str | None) -> None:
        super().__init__({StateType.EXPRESSION})
        self.function_name = function_name

    def trigger_enter(self, context: TraverseContext) -> bool:
        function = context.current_node.child_by_field_name("function")
        if not function:
            return False
        return not self.function_name or function.text.decode() == self.function_name


class SubroutineClause(InvocationExpressionClause):
    def __init__(self) -> None:
        super().__init__(None)

    def handle_enter(self, context: TraverseContext):
        context.commands.append(PlaceBlock('subroutine', tooltip=context.text))


class OutputClause(InvocationExpressionClause):
    def __init__(self, function_name: str) -> None:
        super().__init__(function_name)

    def handle_enter(self, context: TraverseContext):
        arguments = context.current_node.child_by_field_name("arguments")
        assert arguments
        context.commands.append(PlaceBlock(
            "output", output=arguments.named_children[0].text.decode()))

class AssignmentExpressionClause(AnyClause):
    def __init__(self) -> None:
        super().__init__({StateType.EXPRESSION})

    def handle_enter(self, context: TraverseContext):
        context.commands.append(PlaceBlock('assignment', tooltip=context.text))
