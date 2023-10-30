from enum import Enum, auto, unique

from tree_sitter.binding import Node

from blocks import Block


@unique
class State(Enum):
    LINEAR = auto()  # State when algorithm is executed sequentially
    INPUT = auto()  # State when algorithm is trying to take input
    OUTPUT = auto()  # State when algorithm is trying to output
    CONDITION = auto()  # State when algorithm is branching based on the condition
    ITERATOR = auto()
    PARAMETER_LOOP = auto()
    PRE_LOOP = auto()
    POST_LOOP = auto()
    LOOPING = auto()


class StateHolder(object):
    def __init__(self, state: State, marker: Node, route: list[Block] = []) -> None:
        self.route = route
        self.marker = marker
        self.type = state

    def __repr__(self) -> str:
        return f"StateHolder(state={self.type}, marker={self.marker}, route={self.route})"
