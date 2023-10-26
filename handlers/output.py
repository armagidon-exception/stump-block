from tree_sitter import Node
from blocks import Block
from handlers import StateHandler
from traverser_state import StateHolder


class OutputStateHandler(StateHandler):
    def _handle(self, current: Node, name: str | None, text: str, state_stack: list[StateHolder], enter: bool):
        route = state_stack[-1].route
        if current.type == "argument":
            if current.children[0].type == "string_literal":
                route.append(Block("output", current.children[0].children[1].text.decode()))
            else:
                route.append(Block("output", text))
            state_stack.pop()
