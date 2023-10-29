from abc import ABC, abstractmethod

from blocks import Block
from traversing import TraverseContext
from traversing.traverser_state import StateHolder





class StateHandler(ABC):
    @abstractmethod
    def _handle(self, context: TraverseContext):
        pass

    @staticmethod
    def get_current_route(context: TraverseContext):
        return context.state_stack[-1].route

    @staticmethod
    def get_last_block(context: TraverseContext) -> Block:
        return context.state_stack[-1].route[-1]
