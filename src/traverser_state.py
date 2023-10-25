from enum import Enum, auto, unique

@unique
class State(Enum):
    LINEAR =  auto()
    INPUT = auto()
    OUTPUT = auto()
    CONDITION = auto()
    CONDITION_CONSEQ = auto()
    CONDITION_ALTERNATIVE = auto()
