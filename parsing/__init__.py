import os
import logging

from tree_sitter import Language, Parser
from command import Command
from traverser.simple import ParserTraverser
from utils import resolve_dependency_path

if not os.path.exists(resolve_dependency_path("build")):
    os.mkdir(resolve_dependency_path("build"))

lang_lib = resolve_dependency_path("build/language")
parser_dir = resolve_dependency_path("parsers/tree-sitter-c-sharp")

if not os.path.exists(lang_lib):
    Language.build_library(lang_lib, [parser_dir])


CS_LANGUAGE: Language
try:
    CS_LANGUAGE = Language(lang_lib, "c_sharp")
except Exception as e:
    logging.critical(*e.args)
    exit()

METHOD_QUERY = CS_LANGUAGE.query(
    "((method_declaration name: (identifier) @name) @method)"
)


def parse_file(filename: str) -> dict[str, list[Command]]:
    parser = Parser()
    parser.set_language(CS_LANGUAGE)
    try:
        with open(filename, "rb") as file:
            root_node = parser.parse(file.read()).root_node
            captures = METHOD_QUERY.captures(root_node)
            methods = map(lambda x: tuple(map(lambda y: y[0], x)), filter(lambda x: x[0][1] == "method", zip(captures, captures[1:])))
            output = {}
            for method in methods:
                method_name = method[1].text.decode()
                logging.info(f"Parsing method {method_name}...")
                traverser = ParserTraverser()
                traverser.traverse(method[0].walk())
                #print(method[0].text, method[1].text.decode())
            return output
    except Exception as e:
        logging.error(*e.args)
        return {}
