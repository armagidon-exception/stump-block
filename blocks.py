from typing import Self

from tree_sitter import Node


class Block(object):
    def __init__(self, type: str, tooltip: str, blocks:dict[str, list[Self]]={}) -> None:
        self.type = type
        self.tooltip = tooltip
        self.routes = blocks

    def __repr__(self) -> str:
        return f"Block(type={self.type}, tooltip='{self.tooltip}', routes={self.routes})"


    @staticmethod
    def conditional_from_if_statement(node: Node):
        condition_node = node.child_by_field_name('condition')
        assert condition_node
        return Block('if_statement', condition_node.text.decode(), {'consequence': [], 'alternative': []})
