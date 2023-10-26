from tree_sitter.binding import TreeCursor, Node
from blocks import Block
from handlers import StateHandler
from handlers.conditional import BranchStateHandler, ConditionalStateHandler
from handlers.input import InputStateHandler
from handlers.linear import LinearStateHandler
from handlers.output import OutputStateHandler
from traverser import TraverseHandler
from traverser_state import State, StateHolder





class StateMachineTraverser(TraverseHandler):
    def __init__(self, initial_stack: list[StateHolder] = []) -> None:
        super().__init__()
        self.state_stack: list[StateHolder] = initial_stack
        self.state_handlers: dict[State, StateHandler] = {
            State.LINEAR: LinearStateHandler(),
            State.INPUT: InputStateHandler(),
            State.OUTPUT: OutputStateHandler(),
            State.CONDITION: ConditionalStateHandler(),
            State.CONDITIONAL_CONSEQUENCE: BranchStateHandler(),
            State.CONDITIONAL_ALTERNATIVE: BranchStateHandler(),
        }

    def handle(self, cursor: TreeCursor, current: Node, text: str, enter: bool):
        current_state = self.state_stack[-1]
        self.state_handlers[current_state.type].handle(cursor, self.state_stack, enter)
        return super().handle(cursor, current, text, enter)
