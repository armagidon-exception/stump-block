from os import stat
from typing import cast
from tree_sitter.binding import Node
from blocks import Block
from traverser_handler import StateHandler
from traverser_state import State, StateHolder


class LinearStateHandler(StateHandler):
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
        if current.type == "local_declaration_statement" and enter:
            declaration_node = current.child(0)
            assert (
                declaration_node and declaration_node.type == "variable_declaration"
            ), "Received local_declaration_expression without variable declaration"
            route.append(
                Block("declaration", cast(bytes, declaration_node.text).decode())
            )
        elif current.type == "expression_statement" and enter:
            context_node = current.child(0)
            assert context_node, "Received expression_statement without context node"
            if context_node.type == "assignment_expression":
                route.append(Block("assignment", context_node.text.decode()))
            elif context_node.type == "invocation_expression":
                function_node = context_node.child_by_field_name("function")
                arguments_node = context_node.child_by_field_name("arguments")
                assert function_node and function_node.type == "member_access_expression", "Received node without function node"
                assert arguments_node and arguments_node.type == "argument_list", "Received node without argument node"
                if function_node.text.decode() == "Console.WriteLine":
                    state_stack.append(StateHolder(State.OUTPUT, current, state_stack[-1].route))
                else:
                    route.append(Block("invocation", context_node.text.decode()))
        elif current.type == "comment" and text == "//input-start" and enter:
            state_stack.append(StateHolder(State.INPUT, current, route))
        elif current.type == "if_statement" and enter:
            condition_node = current.child_by_field_name("condition")
            assert condition_node, "Received node without condition"
            route.append(Block("if_statement", condition_node.text.decode(), {"consequence": [], "alternative":[]}))
            state_stack.append(StateHolder(State.CONDITION, current, state_stack[-1].route))
