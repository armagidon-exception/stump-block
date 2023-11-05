from enum import Enum, auto, unique

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
