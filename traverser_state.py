from enum import Enum, auto, unique

@unique
class State(Enum):
    LINEAR =  auto()
    INPUT = auto()
    OUTPUT = auto()
    CONDITION = auto()
    CONDITIONAL_CONSEQUENCE = auto()
    CONDITION_ALTERNATIVE = auto()
    ITERATOR = auto()
    PARAMETER_LOOP = auto()
    PRE_LOOP = auto()
    POST_LOOP = auto()
