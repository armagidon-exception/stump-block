from tree_sitter import Node
from blocks import Block
from handlers import StateHandler
from traverser_state import StateHolder


class InputStateHandler(StateHandler):
    def _handle(
        self,
        current: Node,
        prev: Node | None,
        name: str | None,
        text: str,
        state_stack: list[StateHolder],
        enter: bool,
    ):
        route = state_stack[-1].route
        if current.type == "variable_declaration" and enter:
            route.append(Block("input", text))
        elif current.type == "comment" and text == "//input-end" and enter:
            state_stack.pop()
