from tree_sitter import Node
from blocks import Block
from handlers import StateHandler, TraverseContext
from traverser_state import StateHolder


class InputStateHandler(StateHandler):
    def _handle(
        self,
        context: TraverseContext
    ):
        route = context.state_stack[-1].route
        if context.current_node.type == "variable_declaration":
            route.append(Block("input", context.current_node.text.decode()))
        elif context.current_node.type == "comment" and context.current_node.text.decode() == "//input-end":
            context.state_stack.pop()
