import logging
import os
from typing import cast

from tree_sitter import Language, Parser

from command import BreakStatement, CloseChunk, Command, ContinueStatement, OpenChunk, PlaceBlock, ReturnStatement
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
    with open(filename, "rb") as file:
        root_node = parser.parse(file.read()).root_node
        captures = METHOD_QUERY.captures(root_node)
        methods = map(
            lambda x: tuple(map(lambda y: y[0], x)),
            filter(lambda x: x[0][1] == "method", zip(captures, captures[1:])),
        )
        output = {}
        for method in methods:
            method_name = method[1].text.decode()
            logging.info(f"Parsing method {method_name}...")
            body = method[0].child_by_field_name('body')
            assert body
            cursor = body.walk()
            traverser = ParserTraverser(cursor)
            traverser.traverse()
            output[method_name] = traverser.commands
        return output


def post_process_loops(input: dict[str, list[Command]]) -> dict[str, list[Command]]:
    loops = ['preloop', 'postloop', 'iterator', 'parameter_loop']

    def id_generator():
        i = 0

        def next_id():
            nonlocal i
            i += 1
            return i
        return next_id

    output = {}
    for method, commands in input.items():
        next_id = id_generator()
        chunk_stack = []
        tranformed = []
        return_id = None
        for i in range(len(commands)):
            command = commands[i]
            prev_command = commands[i - 1] if i > 0 else None
            if isinstance(command, OpenChunk):
                tranformed.append(command)
                is_loop = False
                if isinstance(prev_command, PlaceBlock) and cast(PlaceBlock, prev_command).block_type in loops:
                    is_loop = True
                chunk_stack.append([command, len(tranformed) - 1, is_loop, None, None, command.chunk_name])
            elif isinstance(command, CloseChunk):
                tranformed.append(command)
                c = chunk_stack.pop()
                if c[2] and c[4] is not None:
                    tranformed.append(PlaceBlock('break', tooltip=str(c[4])))
            elif isinstance(command, ReturnStatement):
                if not return_id:
                    return_id = next_id()
                tranformed.append(PlaceBlock('return', tooltip=return_id))
            elif isinstance(command, BreakStatement):
                matches = list(filter(lambda x: x[2], chunk_stack))
                assert matches, "Syntax error: break statements cannot be outside of loops"
                c = matches[-1]
                if not c[4]:
                    c[4] = next_id()
                tranformed.append(PlaceBlock('break', tooltip=str(c[4])))
            elif isinstance(command, ContinueStatement):
                matches = list(filter(lambda x: x[2], chunk_stack))
                assert matches, "Syntax error: continue statements cannot be outside of loops"
                c = matches[-1]
                if not c[3]:
                    c[3] = next_id()
                    tranformed.insert(c[1] - 1, PlaceBlock('continue', tooltip=str(c[3])))
                tranformed.append(PlaceBlock('continue', tooltip=str(c[3])))
            else:
                tranformed.append(command)

        if return_id:
            tranformed.append(PlaceBlock('return', tooltip=return_id))
        output[method] = tranformed

    return output
