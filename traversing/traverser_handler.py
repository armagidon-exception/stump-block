from tree_sitter.binding import Node, TreeCursor

from handlers import StateHandler
from handlers.conditional import ConditionalStateHandler
from handlers.input import InputStateHandler
from handlers.linear import LinearStateHandler
from handlers.loop import LoopStateHandler
from handlers.output import OutputStateHandler
from traversing import TraverseContext
from traversing.traverser import TraverseHandler
from traversing.traverser_state import State, StateHolder


class StateMachineTraverser(TraverseHandler):
    def __init__(self, initial_stack: list[StateHolder] = []) -> None:
        super().__init__()
        self.state_stack: list[StateHolder] = initial_stack
        self.state_handlers: dict[State, StateHandler] = {
            State.LINEAR: LinearStateHandler(),
            State.INPUT: InputStateHandler(),
            State.OUTPUT: OutputStateHandler(),
            State.CONDITION: ConditionalStateHandler(),
            State.PRE_LOOP: LoopStateHandler(),
            State.POST_LOOP: LoopStateHandler(),
            State.PARAMETER_LOOP: LoopStateHandler()
        }

    def handle_discover(self, cursor: TreeCursor, prev: Node, prev_name: str | None):
        current_state = self.state_stack[-1]
        self.state_handlers[current_state.type]._handle(
            TraverseContext(
                cursor.node, prev, cursor.field_name, prev_name, self.state_stack, True
            )
        )

    def handle_retreating(self, cursor: TreeCursor, prev: Node, prev_name: str | None):
        current_state = self.state_stack[-1]
        self.state_handlers[current_state.type]._handle(
            TraverseContext(
                cursor.node, prev, cursor.field_name, prev_name, self.state_stack, False
            )
        )
        if current_state.marker.id == cursor.node.id:
            self.state_stack.pop()
