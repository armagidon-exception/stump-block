import os
import sys

from tree_sitter import Node


def resolve_dependency_path(path: str) -> str:
    if getattr(sys, "frozen", False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, path)


def capture_within(start: Node, end: Node, named_only=False) -> list[Node]:
    curr = start
    buf = []
    while curr.id != end.id:
        if not curr:
            break
        buf.append(curr)
        curr = curr.next_named_sibling if named_only else curr.next_sibling
    buf.append(end)
    return buf
