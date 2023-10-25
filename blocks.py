class Block(object):
    def __init__(self, type: str, tooltip: str) -> None:
        self.type = type
        self.tooltip = tooltip
        self.routes = {}

    def __repr__(self) -> str:
        return f"<type={self.type}, tooltip='{self.tooltip}', routes={self.routes}>"
