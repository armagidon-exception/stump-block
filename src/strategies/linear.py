from tree_sitter import Node
from traverser_state import State
from blocks import Block, SingleBlock, SubRoutineBlock


def handle_linear_mode(current: Node, state_stack: list[State], blocks: list[Block]):
    code = current.text.decode("utf-8").replace("\n", "")
    current_state: State = state_stack[-1]

    if current.type == "variable_declaration":
        blocks.append(SingleBlock(code))
    elif current.type == "invocation_expression":
        if current.parent and current.parent.type == "expression_statement":
            blocks.append(SubRoutineBlock(code))
    elif current.type == "comment" and code == "//stumpblock-meta-input-start":
        state_stack.append(State.INPUT)
