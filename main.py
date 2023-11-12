#!/bin/python3

import logging
from argparse import ArgumentParser
from pprint import pprint

from parsing import parse_file, post_process_loops

logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s > %(message)s",
    datefmt="%H:%M:%S",
)


def process_file(filename: str):
    logging.info(f"Parsing AST of file {filename}")
    parsing_result = parse_file(filename)
    logging.info(f"Post processing rendering commands...")
    parsing_result = post_process_loops(parsing_result)
    logging.info(f"Rendering file {filename}")


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        prog="stumpblock", description="Converts C# code to block diagrams"
    )
    arg_parser.add_argument("input")
    args = arg_parser.parse_args()
    process_file(args.input)
