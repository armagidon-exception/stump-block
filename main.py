#!/bin/python3

from argparse import ArgumentParser
import logging

from parsing import parse_file

logging.basicConfig(encoding="utf-8", level=logging.INFO)


def process_file(filename: str):
    parse_file(filename)
    pass


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        prog="stumpblock", description="Converts C# code to block diagrams"
    )
    arg_parser.add_argument("input")
    args = arg_parser.parse_args()
    process_file(args.input)
