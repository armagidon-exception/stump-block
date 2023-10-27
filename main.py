#!/bin/python3

import os
from tree_sitter import Language, Parser
from argparse import ArgumentParser
from blocks import Block
from traverser import traverse

from pprint import pprint
from traverser_state import State, StateHolder
from traverser_handler import StateMachineTraverser

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
    arg_parser.add_argument("filename")
    args = arg_parser.parse_args()

    query = CS_LANGUAGE.query(
        '((method_declaration name: (identifier) @name (#eq? @name "Main")) @method)'
    )

    blocks:list[Block] = []
    traverse_handler = StateMachineTraverser([StateHolder(State.LINEAR, blocks)])

    with open(args.filename, "rb") as file:
        text = file.read()
        tree = parser.parse(text)
        cursor = query.captures(tree.root_node)[0][0].walk()
        traverse(cursor, traverse_handler)
        pprint(blocks)
