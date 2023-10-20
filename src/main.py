#!/bin/python3

from tree_sitter import Language, Parser
from argparse import ArgumentParser
from traverser import Traverser

Language.build_library("../build/languages.so", ["../parsers/tree-sitter-c-sharp"])
CS_LANGUAGE = Language("../build/languages.so", "c_sharp")
parser = Parser()
parser.set_language(CS_LANGUAGE)

traverser = Traverser(CS_LANGUAGE)

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        prog="stumpblock", description="Converts C# code to block diagrams"
    )
    arg_parser.add_argument("filename")
    args = arg_parser.parse_args()

    query = CS_LANGUAGE.query(
        """
        ((method_declaration name: (identifier) @name (#eq? @name "Main")) @method)
    """
    )

    with open(args.filename, "rb") as file:
        text = file.read()
        tree = parser.parse(text)
        c = query.captures(tree.root_node)[0][0].walk()
        blocks = []
        traverser.traverse(c, blocks)
        print(blocks)
