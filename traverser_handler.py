from tree_sitter.binding import Node, TreeCursor

from handlers import StateHandler
from handlers.conditional import ConditionalStateHandler
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
        }

    def _handle_enter(
        self, cursor: TreeCursor, current: Node, prev: Node | None, text: str
    ):
        current_state = self.state_stack[-1]
        self.state_handlers[current_state.type]._handle(
            cursor.node,
            prev,
            cursor.field_name,
            current.text.decode(),
            self.state_stack,
            True,
        )

        #print(self.state_stack)

    def _handle_leave(
        self, cursor: TreeCursor, current: Node, prev: Node | None, text: str
    ):
        current_state = self.state_stack[-1]
        self.state_handlers[current_state.type]._handle(
            cursor.node,
            prev,
            cursor.field_name,
            current.text.decode(),
            self.state_stack,
            False,
        )
