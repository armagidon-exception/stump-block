class Block(object):
    def __init__(self, type: str, tooltip: str, blocks={}) -> None:
        self.type = type
        self.tooltip = tooltip
        self.routes = blocks

    def __repr__(self) -> str:
        return f"<type={self.type}, tooltip='{self.tooltip}', routes={self.routes}>"
