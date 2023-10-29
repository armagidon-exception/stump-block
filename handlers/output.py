from blocks import Block
from handlers import StateHandler
from traversing import TraverseContext


class OutputStateHandler(StateHandler):
    def _handle(self, context: TraverseContext):
        route = context.state_stack[-1].route
        if context.current_node.type == "argument":
            value_node = context.current_node.children[0]
            assert value_node
            if value_node.type == "string_literal":
                route.append(
                    Block("output", value_node.children[1].text.decode())
                )
            else:
                route.append(Block("output", context.current_node.text.decode()))
            context.state_stack.pop()
