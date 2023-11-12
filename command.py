class Command:
    def __init__(self, **args) -> None:
        for k, v in args.items():
            setattr(self, k, v)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(['{}={!r}'.format(k, v) for k, v in self.__dict__.items()])})"


class OpenChunk(Command):
    def __init__(self, chunk_name: str, **args) -> None:
        super().__init__(chunk_name=chunk_name, **args)
        self.chunk_name = chunk_name


class CloseChunk(Command):
    def __init__(self, **args) -> None:
        super().__init__(**args)


class ReturnStatement(Command):
    def __init__(self, **args) -> None:
        super().__init__(**args)


class ContinueStatement(Command):
    def __init__(self, **args) -> None:
        super().__init__(**args)


class BreakStatement(Command):
    def __init__(self, **args) -> None:
        super().__init__(**args)


class CreateBreak(Command):
    def __init__(self, **args) -> None:
        super().__init__(**args)


class PlaceBlock(Command):
    def __init__(self, block_type: str, **args) -> None:
        super().__init__(block_type=block_type, **args)
        self.block_type = block_type
