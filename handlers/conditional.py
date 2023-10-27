from tree_sitter import Node
from handlers import StateHandler
from handlers.linear import LinearStateHandler
from traverser_state import State, StateHolder


class ConditionalStateHandler(StateHandler):
    _linear_state_hander = LinearStateHandler()

    def _handle(
        self,
        current: Node,
        prev: Node | None,
        name: str | None,
        text: str,
        state_stack: list[StateHolder],
        enter: bool,
    ):
        if name == "consequence" and enter:
            state_stack.append( StateHolder( State.LINEAR, current, state_stack[-1].route[-1].routes["consequence"]))
        elif name == "alternative" and enter:
            state_stack.append(
                StateHolder(
                    State.LINEAR, current, state_stack[-1].route[-1].routes["alternative"]
                )
            )
        elif name == "condition":
            pass
