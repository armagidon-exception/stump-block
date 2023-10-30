from tree_sitter.binding import Node

from traversing.traverser_state import StateHolder


class TraverseContext:
    def __init__(
            self,
            current_node: Node,
            prev_node: Node,
            current_name: str | None,
            prev_name: str | None,
            state_stack: list[StateHolder],
            enter: bool,
    ) -> None:
        self.current_node = current_node
        self.prev_node = prev_node
        self.current_name = current_name
        self.prev_name = prev_name
        self.state_stack = state_stack
        self.enter = enter
