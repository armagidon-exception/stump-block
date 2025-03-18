from typing_extensions import Self
from tree_sitter import Node


class Block(object):
    def __init__(
        self, type: str, tooltip: str, routes: dict[str, list[Self]] = {}
    ) -> None:
        self.type = type
        self.tooltip = tooltip
        self.routes = routes

    # def __repr__(self) -> str:
    #     return (
    #         f"Block(type={self.type}, tooltip='{self.tooltip}', routes={self.routes})"
    #     )

    @staticmethod
    def conditional_from_if_statement(node: Node):
        condition_node = node.child_by_field_name("condition")
        assert condition_node
        return Block(
            "condition",
            condition_node.text.decode(),
            {"consequence": [], "alternative": []},
        )

    @staticmethod
    def loop_from_while_statement(node: Node):
        condition_node = node.child(2)
        assert condition_node
        return Block("preloop", condition_node.text.decode(), {"body": []})

    @staticmethod
    def loop_from_do_statement(node: Node):
        condition_node = node.child(4)
        assert condition_node
        return Block("postloop", condition_node.text.decode(), {"body": []})

    @staticmethod
    def loop_from_for_statement(node: Node):
        initializer = node.child_by_field_name("initializer")
        condition = node.child_by_field_name("condition")
        update = node.child_by_field_name("update")
        assert initializer and condition and update

        return Block(
            "parameterloop",
            f"{initializer.text.decode()}; {condition.text.decode()}; {update.text.decode()}",
            {"body": []},
        )

    @staticmethod
    def loop_from_foreach_statement(node: Node):
        initializer = node.child_by_field_name("type")
        condition = node.child_by_field_name("left")
        update = node.child_by_field_name("right")
        assert initializer and condition and update

        return Block(
            "parameterloop",
            f"{initializer.text.decode()} {condition.text.decode()} in {update.text.decode()}",
            {"body": []},
        )
