from typing import cast
from tree_sitter.binding import Node
from blocks import Block
from traverser_handler import StateHandler
from traverser_state import State, StateHolder


class LinearStateHandler(StateHandler):
    def _handle(self, current: Node, name: str | None, text: str, state_stack: list[StateHolder], enter: bool):
        route = state_stack[-1].route
        if current.type == "variable_declaration":
            route.append(Block("single", text))
        elif current.type == "invocation_expression":
            func_name = cast(Node, current.child_by_field_name("function"))
            if func_name.text.decode() == "Console.WriteLine":
                state_stack.append(StateHolder(State.OUTPUT, route))
            elif current.parent and current.parent.type == "expression_statement":
                route.append(Block("invoke", text))
        elif current.type == "comment" and text == "//stumpblock-meta-input-start":
            state_stack.append(StateHolder(State.INPUT, route))
        elif current.type == "if_statement":
            block = Block("conditional", current.named_children[0].text.decode())
            block.routes["consequence"] = []
            block.routes["alternative"] = []
            route.append(block)
            state_stack.append(StateHolder(State.CONDITION, route))
