from abc import ABC


class State(ABC):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

class Linear(State):
    def __init__(self) -> None:
        super().__init__("linear")

class InputState(State):
    def __init__(self) -> None:
        super().__init__("input")
        self.vars = []
