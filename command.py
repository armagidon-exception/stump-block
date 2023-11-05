from typing import Any


class Command:
    def __init__(self, identifier: str, *args: dict[str, Any]) -> None:
        self.identifier = identifier
        self.args = args
