from blocks import Block
from handlers import StateHandler
from traversing import TraverseContext


class InputStateHandler(StateHandler):
    def _handle(
            self,
            context: TraverseContext
    ):
        if not context.enter:
            return
        route = context.state_stack[-1].route
        if context.current_node.type == "variable_declaration":
            route.append(Block("input", context.current_node.child(1).child_by_field_name('name').text.decode()))
            print(f"Processed block with type {route[-1].type} with captured text '{route[-1].tooltip}'")
        elif context.current_node.type == "comment" and context.current_node.text.decode() == "//input-end":
            context.state_stack.pop()
