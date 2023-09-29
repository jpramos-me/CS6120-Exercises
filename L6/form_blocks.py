"""
The core logic for forming basic blocks was adapted in part from [bril's example](https://github.com/sampsyo/bril/blob/main/examples/form_blocks.py)
"""

import json
import sys

TERMINATORS = ["jmp", "ret", "br"]


def form_blocks(instrs):
    curr_block = []
    for i in instrs:
        if "op" in i:
            curr_block.append(i)
            if i["op"] in TERMINATORS:
                yield curr_block
                curr_block = []
        else:
            yield curr_block
            curr_block = [i]
    yield curr_block


def main():
    file = ""
    for line in fileinput.input():
        file += line

    file = json.loads(file)

    for func in file["functions"]:
        blocks = form_blocks(func["instrs"])
        for block in blocks:
            print(block)


if __name__ == "__main__":
    main()
