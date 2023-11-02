#!/bin/python3 -B

import os
from argparse import ArgumentParser
from pprint import pprint

from tree_sitter import Language, Parser

from backend.schemdraw_backend import render
from blocks import Block
from traversing.traverser import *
from traversing.traverser_handler import StateMachineTraverser
from traversing.traverser_state import State, StateHolder

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
    arg_parser.add_argument("output")
    args = arg_parser.parse_args()

    main_method_query = CS_LANGUAGE.query(
        '((method_declaration name: (identifier) @name (#eq? @name "Main")) @method)'
    )

    blocks: list[Block] = []

    with open(args.input, "rb") as file:
        text = file.read()
        tree = parser.parse(text)
        cursor = main_method_query.captures(tree.root_node)[0][0].walk()
        traverse_handler = StateMachineTraverser(
            [StateHolder(State.LINEAR, cursor.node, blocks)]
        )
        blocks.append(Block("start", "Start"))
        traverse(cursor, traverse_handler)
        blocks.append(Block("end", "End"))
        for block in blocks:
            print(f"Processed top-level block with type {block.type} with captured text '{block.tooltip}'")
        print("Rendering.....")
        try:
            render(args.output, blocks)
            print("Rendering done. Saved to file", args.output)
        except Exception as e:
            print(e)

