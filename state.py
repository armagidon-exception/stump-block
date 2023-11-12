from enum import Enum, auto, unique

from tree_sitter import Node

from command import Command


@unique
class StateType(Enum):
    LINEAR = auto()  # State when algorithm is executed sequentially
    INPUT = auto()  # State when algorithm is trying to take input
    OUTPUT = auto()  # State when algorithm is trying to output
    IF_STATEMENT = auto()  # State when algorithm is branching based on the condition
    ITERATOR = auto()
    PARAMETER_LOOP = auto()
    PRE_LOOP = auto()
    POST_LOOP = auto()
    EXPRESSION = auto()



class State:
    def __init__(
            self,
            type: StateType,
            commands: list[Command],
            marker: Node,
            routes: list[str] = [],
    ) -> None:
        self.type = type
        self.commands = commands
        self.routes = routes
        self.marker = marker

    def __repr__(self) -> str:
        return f"State(type={self.type})"
