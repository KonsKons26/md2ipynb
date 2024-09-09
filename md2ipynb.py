#!/usr/bin/env python3

import json
import argparse


def md_parser(path):
    """
    This function reads an MD file and returns its lines in a list.
    """
    with open(path, "r") as reader:
        lines = reader.readlines()
    return lines


def find_blocks(lines, title_depth=5):
    """
    This function finds all lines that start with a `#` and are not inside a
    code block, then returns a list of lists where each inner list is a block
    that starts with a `#`. 
    """
    block_starts = []
    code_blocks = []
    code_block_opened = False
    for i, line in enumerate(lines):
        # Check if a line starts with a backtick or quotation marks then creates a
        # list of lists where each inner list is a pair of indexes that mark the
        # start and end of each code block
        if line.startswith("`") or line.startswith("'") or line.startswith('"'):
            if code_block_opened == False:
                code_blocks.append([i])
                code_block_opened = True
            else:
                code_blocks[-1].append(i)
                code_block_opened = False

        # Append the indexes of titles that also match the title_depth criterion
        if line.startswith("#") and line.split(" ")[0] in "#" * title_depth:
            block_starts.append(i)

    # Remove the indexes of `#` that are inside code blocks
    block_starts_remove = []
    for begin, end in code_blocks:
        for i in block_starts:
            if begin < i < end:
                block_starts_remove.append(i)
    block_starts = [start for start in block_starts if start not in block_starts_remove]

    # Place all the text before the first `#` in a block, if the MD file does not start
    # with a `#`
    if block_starts[0] == 0:
        blocks = []
    else:
        blocks = [[lines[i] for i in range(0, block_starts[0])]]
    # Iterate over the block_starts indexes
    for i in range(0, len(block_starts) - 1):
        block = []
        # Place the lines between the two block_starts indexes in the temporary list
        # and then in the final list with the rest of the blocks
        for j in range(block_starts[i], block_starts[i + 1]):
            block.append(lines[j])
        blocks.append(block)
    # Place the final block in the list
    blocks.append([lines[i] for i in range(block_starts[-1], len(lines))])

    return blocks


def create_nb_json(blocks):
    """
    This function takes all the blocks and creates the json structure of the notebook.
    """
    md_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": block
        }
        for block in blocks
    ]

    metadata_cell = {}
    nbformat = 4
    nbformat_minor = 2

    return {
        "cells": md_cells,
        "metadata_cell": metadata_cell,
        "nbormat": nbformat,
        nbformat_minor: nbformat_minor
    }


def save_ipynb(path, json_dict):
    """
    This function takes the json dictionary and saves it as an ipynb.
    """
    json_str = json.dumps(json_dict, indent=4)
    with open(path, "w") as writer:
        writer.write(json_str)


def main(i, o, d):
    raw_md = md_parser(i)
    blocks = find_blocks(raw_md, d)
    json_dict = create_nb_json(blocks)
    save_ipynb(o, json_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="desc")

    parser.add_argument("i", type=str, help="input, MD file path")
    parser.add_argument("o", type=str, help="output, ipynb file path")
    parser.add_argument("-d", type=int, default=5, help="title depth")
    args = parser.parse_args()

    main(args.i, args.o, args.d)
