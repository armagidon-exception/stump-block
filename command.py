class Command:
    def __init__(self, identifier: str, **args) -> None:
        self.identifier = identifier
        self.args = args

        for k, v in self.args.items():
            setattr(self, k, v)


class OpenChunk(Command):
    def __init__(self, chunk_name: str, **args) -> None:
        super().__init__("open-chunk", chunk_name=chunk_name, **args)


class CloseChunk(Command):
    def __init__(self, **args) -> None:
        super().__init__("close-chunk", **args)


class ReturnStatement(Command):
    def __init__(self, **args) -> None:
        super().__init__("return", **args)


class ContinueStatement(Command):
    def __init__(self, **args) -> None:
        super().__init__("continue", **args)


class BreakStatement(Command):
    def __init__(self, **args) -> None:
        super().__init__("break", **args)


class PlaceBlock(Command):
    def __init__(self, block_type: str, routes: list[str], **args) -> None:
        super().__init__("block", block_type=block_type, routes=routes, **args)
