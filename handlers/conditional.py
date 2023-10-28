from blocks import Block
from handlers import StateHandler, TraverseContext
from handlers.linear import LinearStateHandler
from traverser_state import State, StateHolder


class ConditionalStateHandler(StateHandler):
    _linear_state_hander = LinearStateHandler()

    def _handle(self, context: TraverseContext):
        current_route = context.state_stack[-1].route
        linear_types = ['empty_statement', 'block', 'expression_statement']
        if context.enter and context.current_name in current_route[-1].routes:
            if context.current_node.type in linear_types:
                context.state_stack.append(StateHolder(State.LINEAR, context.current_node, current_route[-1].routes[context.current_name]))
            elif context.current_node.type == "if_statement":
                current_route = current_route[-1].routes[context.current_name]
                block = Block.conditional_from_if_statement(context.current_node)
                current_route.append(block)
                context.state_stack.append(StateHolder(State.CONDITION, context.current_node, current_route))
