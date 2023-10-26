from enum import Enum, auto, unique

from blocks import Block


@unique
class State(Enum):
    LINEAR = auto()
    INPUT = auto()
    OUTPUT = auto()
    CONDITION = auto()
    CONDITIONAL_CONSEQUENCE = auto()
    CONDITIONAL_ALTERNATIVE = auto()
    ITERATOR = auto()
    PARAMETER_LOOP = auto()
    PRE_LOOP = auto()
    POST_LOOP = auto()
    LOOPING = auto()


class StateHolder(object):
    def __init__(self, state: State, route: list[Block] = []) -> None:
        self.route = route
        self.type = state
