#!/bin/python3

from tree_sitter import Language, Parser
from argparse import ArgumentParser
from traverser import traverse

from pprint import pprint
from traverser_state import State
import traverser_handler


if __name__ == "__main__":
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

    state_stack = [State.LINEAR]
    blocks = []
    route_stack = [blocks]

    with open(args.filename, "rb") as file:
        text = file.read()
        tree = parser.parse(text)
        cursor = query.captures(tree.root_node)[0][0].walk()
        traverse(cursor, lambda c, n, t, e, d: traverser_handler.handle_node(c, n, t, e, state_stack, route_stack, d))
        pprint(blocks)
