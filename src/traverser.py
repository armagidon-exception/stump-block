from typing import cast
from tree_sitter import Language, TreeCursor
from blocks import Block, IOBlock, SingleBlock, SubRoutineBlock
from traverser_state import State

class Traverser(object):
    def __init__(self, lang: Language) -> None:
        self.lang = lang
        state_stack: list[State] = [State.LINEAR]
        self.state_stack = state_stack

    def traverse(self, cursor: TreeCursor, blocks: list[Block]):
        depth = 0
        accumulator = blocks
        while True:
            if cursor.goto_first_child():
                depth += 1
                self.handle_node(cursor, blocks, depth)
            elif cursor.goto_next_sibling():
                self.handle_node(cursor, blocks, depth)
            elif cursor.goto_parent():
                depth -= 1
                while not cursor.goto_next_sibling():
                    if not cursor.goto_parent():
                        return
                    else:
                        depth -= 1
                self.handle_node(cursor, blocks, depth)
            else:
                return

    def handle_node(self, cursor: TreeCursor, blocks: list[Block], depth: int):
        current = cursor.node
        if not current.is_named:
            return

        code = current.text.decode("utf-8").replace("\n", "")
        current_state: State = self.state_stack[-1]
        print(" " * depth, current.type)

        if current_state.name == "input":
            self.handle_io_state(cursor, blocks)
        else:
            if current.type == "variable_declaration":
                blocks.append(SingleBlock(code))
            elif current.type == "invocation_expression":
                if current.parent and current.parent.type == "expression_statement":
                    blocks.append(SubRoutineBlock(code))
            elif current.type == "comment" and code == "//stumpblock-meta-input-start":
                self.state_stack.append(InputState())

    def handle_io_state(self, cursor: TreeCursor, blocks: list[Block]):
        current = cursor.node

        code = current.text.decode("utf-8").replace("\n", "")

        current_state: InputState = cast(InputState, self.state_stack[-1])
        if current.type == "variable_declaration":
            query = self.lang.query(
                """
                (variable_declarator name:(identifier) @name)
            """
            )
            var_name = query.captures(current)[0][0].text
            current_state.vars.append(var_name)
        elif current.type == "comment" and code == "//stumpblock-meta-input-end":
            self.state_stack.pop()
            blocks.append(IOBlock("Enter", current_state.vars))
