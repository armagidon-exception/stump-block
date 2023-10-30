from blocks import Block
from traversing import TraverseContext
from traversing.traverser_handler import StateHandler
from traversing.traverser_state import State, StateHolder


class LinearStateHandler(StateHandler):
    def _handle(self, context: TraverseContext):
        route = context.state_stack[-1].route
        if not context.enter: return
        if context.current_node.type == "local_declaration_statement":
            declaration_node = context.current_node.child(0)
            assert (
                    declaration_node and declaration_node.type == "variable_declaration"
            ), "Received local_declaration_expression without variable declaration"
            route.append(Block("declaration", declaration_node.text.decode()))
        elif context.current_node.type == "expression_statement":
            context_node = context.current_node.child(0)
            assert context_node, "Received expression_statement without context node"
            if context_node.type == "assignment_expression":
                route.append(Block("assignment", context_node.text.decode()))
            elif context_node.type == "invocation_expression":
                function_node = context_node.child_by_field_name("function")
                arguments_node = context_node.child_by_field_name("arguments")
                assert (
                        function_node and function_node.type == "member_access_expression"
                ), "Received node without function node"
                assert (
                        arguments_node and arguments_node.type == "argument_list"
                ), "Received node without argument node"
                if function_node.text.decode() == "Console.WriteLine":
                    context.state_stack.append(
                        StateHolder(
                            State.OUTPUT,
                            context.current_node,
                            StateHandler.get_current_route(context),
                        )
                    )
                else:
                    route.append(Block("invocation", context_node.text.decode()))
        elif (
                context.current_node.type == "comment"
                and context.current_node.text.decode() == "//input-start"
        ):
            context.state_stack.append(StateHolder(State.INPUT, context.current_node, route))
        elif context.current_node.type == "if_statement":
            block = Block.conditional_from_if_statement(context.current_node)
            route.append(block)
            context.state_stack.append(StateHolder(State.CONDITION, context.current_node, route))
        elif context.current_node.type == "while_statement":
            block = Block.loop_from_while_statement(context.current_node)
            route.append(block)
            context.state_stack.append(StateHolder(State.PRE_LOOP, context.current_node, route))
        elif context.current_node.type == "do_statement":
            block = Block.loop_from_do_statement(context.current_node)
            route.append(block)
            context.state_stack.append(StateHolder(State.POST_LOOP, context.current_node, route))
