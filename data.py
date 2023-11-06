class Block:
    def __init__(self, type: str, **args) -> None:
        self.type = type
        self.args = args
        for k, v in self.args.items():
            setattr(self, k, v)

class Chunk:
    def __init__(self, id: str, enter_marker=False, exit_marker=False) -> None:
        self.id = id
        self.enter_marker = enter_marker
        self.exit_marker = exit_marker
        self.blocks = []
