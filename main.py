#!/bin/python3 -B

import os
from argparse import ArgumentParser

from tree_sitter import Language, Parser

from backend.schemdraw_backend import render
from blocks import Block
from traversing.traverser import *
from traversing.traverser_handler import StateMachineTraverser
from traversing.traverser_state import State, StateHolder


def render_method(node, method_name):
    blocks: list[Block] = []
    cursor = node.walk()
    traverse_handler = StateMachineTraverser(
        [StateHolder(State.LINEAR, cursor.node, blocks)]
    )
    if method_name == "Main":
        blocks.append(Block("start", "Start"))
    else:
        blocks.append(Block("start", "Start of " + method_name))
    traverse(cursor, traverse_handler)
    blocks.append(Block("end", "End"))
    print("Rendering.....")
    try:
        render(method_name + ".svg", blocks)
        print("Rendering done. Saved to file", method_name + ".svg")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if not os.path.exists("build"):
        os.mkdir("build")
    Language.build_library("build/languages.so", ["parsers/tree-sitter-c-sharp"])
    CS_LANGUAGE = Language("build/languages.so", "c_sharp")
    parser = Parser()
    parser.set_language(CS_LANGUAGE)

    arg_parser = ArgumentParser(
        prog="stumpblock", description="Converts C# code to block diagrams"
    )
    arg_parser.add_argument("input")
    args = arg_parser.parse_args()

    methods_query = CS_LANGUAGE.query(
        "((method_declaration name: (identifier) @name) @method)"
    )


    with open(args.input, "rb") as file:
        text = file.read()
        tree = parser.parse(text)
        captures = methods_query.captures(tree.root_node)
        for i in range(0, len(captures) - 1, 2):
            render_method(captures[i][0], captures[i + 1][0].text.decode())
