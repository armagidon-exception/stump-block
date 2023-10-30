from handlers import StateHandler
from traversing import TraverseContext
from traversing.traverser_state import State, StateHolder


class LoopStateHandler(StateHandler):

    def _handle(self, context: TraverseContext):
        linear_types = ['empty_statement', 'block', 'expression_statement']
        current_state = context.state_stack[-1]
        if current_state.type == State.PRE_LOOP or current_state.type == State.POST_LOOP:
            if context.current_node.type in linear_types:
                context.state_stack.append(StateHolder(State.LINEAR, context.current_node,
                                                       StateHandler.get_last_block(context).routes['body']))
