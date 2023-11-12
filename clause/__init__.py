from abc import ABC, abstractmethod

from state import StateType
from traverser import TraverseContext


class Clause(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def trigger_enter(self, context: TraverseContext) -> bool:
        return False

    @abstractmethod
    def handle_enter(self, context: TraverseContext):
        pass

    def trigger_exit(self, context: TraverseContext) -> bool:
        return False

    def handle_exit(self, context: TraverseContext):
        pass

    def states(self) -> set[StateType]:
        return {StateType.LINEAR}
