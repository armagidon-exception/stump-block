from os import statvfs
from re import S
from typing import cast
from tree_sitter import TreeCursor, Node
from blocks import Block

from traverser_state import State


def handle_node(
    cursor: TreeCursor,
    current: Node,
    text: str,
    enter: bool,
    state_stack: list[State],
    route_stack: list[list[Block]],
    depth,
):
    current_state = state_stack[-1]
    if current_state == State.LINEAR and enter:
        handle_linear_mode(
            current,
            text,
            state_stack,
            route_stack[-1],
        )
    elif current_state == State.INPUT and enter:
        handle_input_mode(current, text, state_stack, route_stack[-1])
    elif current_state == State.OUTPUT and enter:
        handle_output_mode(current, text, state_stack, route_stack[-1])
    elif (
        current_state == State.CONDITION
        or current_state == State.CONDITIONAL_CONSEQUENCE
        or current_state == State.CONDITION_ALTERNATIVE
    ):
        handle_conditional(current, text, state_stack, route_stack, enter)


def handle_linear_mode(
    current: Node,
    text: str,
    state_stack: list[State],
    route: list[Block],
):
    if current.type == "variable_declaration":
        route.append(Block("single", text))

    elif current.type == "invocation_expression":
        func_name = cast(Node, current.child_by_field_name("function"))
        if func_name.text.decode() == "Console.WriteLine":
            state_stack.append(State.OUTPUT)
        elif current.parent and current.parent.type == "expression_statement":
            route.append(Block("invoke", text))
    elif current.type == "comment" and text == "//stumpblock-meta-input-start":
        state_stack.append(State.INPUT)
    elif current.type == "if_statement":
        block = Block("conditional", current.named_children[0].text.decode())
        block.routes["consequence"] = []
        block.routes["alternative"] = []
        route.append(block)
        state_stack.append(State.CONDITION)


def handle_input_mode(
    current: Node,
    text: str,
    state_stack: list[State],
    route: list[Block],
):
    if current.type == "variable_declaration":
        route.append(Block("input", text))
    elif current.type == "comment" and text == "//stumpblock-meta-input-end":
        state_stack.pop()


def handle_output_mode(current: Node, text, state_stack, route):
    if current.type == "argument":
        if current.children[0].type == "string_literal":
            route.append(Block("output", current.children[0].children[1].text.decode()))
        else:
            route.append(Block("output", text))
        state_stack.pop()


def handle_conditional(
    current: Node,
    text: str,
    state_stack: list[State],
    route_stack: list[list[Block]],
    enter: bool,
):
    if not current.parent:
        return
    current_state = state_stack[-1]
    conseq = current.parent.child_by_field_name("consequence")
    alter = current.parent.child_by_field_name("alternative")
    if current_state == State.CONDITION:
        if enter and conseq and current.id == conseq.id:
            state_stack.append(State.CONDITIONAL_CONSEQUENCE)
            route_stack.append(route_stack[-1][-1].routes["consequence"])
        elif enter and alter and current.id == alter.id:
            state_stack.append(State.CONDITION_ALTERNATIVE)
            route_stack.append(route_stack[-1][-1].routes["alternative"])
    elif (
        current_state == State.CONDITIONAL_CONSEQUENCE
        or current_state == State.CONDITION_ALTERNATIVE
    ):
        if (
            not enter
            and (conseq and current.id == conseq.id)
            or (alter and current.id == alter.id)
        ):
            state_stack.pop()
            route_stack.pop()
        elif enter:
            handle_linear_mode(current, text, state_stack, route_stack[-1])

