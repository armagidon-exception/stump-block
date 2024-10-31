#!/bin/python3 -B

import os
import sys
from argparse import ArgumentParser

from tree_sitter import Language, Parser

from backend.schemdraw_backend import render
from blocks import Block
from traversing.traverser import *
from traversing.traverser_handler import StateMachineTraverser
from traversing.traverser_state import State, StateHolder


def find_data_file(filename):
    if getattr(sys, "frozen", False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


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
    render(os.path.join(os.getcwd(), method_name + ".svg"), blocks)
    print("Rendering done. Saved to file", method_name + ".svg")


if __name__ == "__main__":
    if not os.path.exists(find_data_file("build")):
        os.mkdir(find_data_file("build"))
    Language.build_library(
        find_data_file("build/languages.so"),
        [find_data_file("parsers/tree-sitter-c-sharp")],
    )
    CS_LANGUAGE = Language(find_data_file("build/languages.so"), "c_sharp")
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

    input_file = os.path.join(os.getcwd(), args.input)
    with open(input_file, "rb") as file:
        text = file.read()
        tree = parser.parse(text)
        captures = methods_query.captures(tree.root_node)
        for i in range(0, len(captures) - 1, 2):
            render_method(captures[i][0], captures[i + 1][0].text.decode())
