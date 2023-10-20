class Block(object):
    def __init__(self, type: str, tooltip: str) -> None:
        self.type = type
        self.tooltip = tooltip

    def __repr__(self) -> str:
        return f"<type={self.type}, tooltip='{self.tooltip}'>"


class SingleBlock(Block):
    def __init__(self, tooltip):
        super().__init__("single", tooltip)


class SubRoutineBlock(Block):
    def __init__(self, tooltip):
        super().__init__("subroutine", tooltip)


class FlagBlock(Block):
    def __init__(self, tooltip: str) -> None:
        super().__init__("flag", tooltip)


class IOBlock(Block):
    def __init__(self, action: str, var_names: list[str]) -> None:
        super().__init__("io", f"{action} {var_names}")
        self.var_names = var_names


class IteratorBlock(Block):
    def __init__(self, tooltip: str, statements: list[Block]) -> None:
        super().__init__("iterator", tooltip)
        self.statements = statements


class PreCondLoopBlock(Block):
    def __init__(self, tooltip: str, statements: list[Block]) -> None:
        super().__init__("precondloop", tooltip)
        self.statements = statements


class PostCondLoopBlock(Block):
    def __init__(self, tooltip: str, statements: list[Block]) -> None:
        super().__init__("postcondloop", tooltip)
        self.statements = statements


class ConditionalBlock(Block):
    def __init__(
        self, tooltip: str, consequence: list[Block], alternative: list[Block]
    ) -> None:
        super().__init__("conditional", tooltip)
        self.consequence = consequence
        self.alternative = alternative
