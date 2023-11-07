from abc import ABC, abstractmethod

from traverser import TraverseContext


class Clause(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def trigger(self, context: TraverseContext) -> bool:
        pass

    @abstractmethod
    def handle(self, context: TraverseContext):
        pass
