import json
import fileinput


def clean_blocks(file):
    blocks, iterative = [], []

    for i in file["instrs"]:
        iterative.append(i)
        if "op" in i and i["op"] in {"br", "jmp", "call", "ret"}:
            blocks.append(iterative)
            iterative = []

    if iterative:
        blocks.append(iterative)

    return blocks


def dce(blocks):
    state = True
    while state:
        optimize = {}
        for block in blocks:
            for instr in block:
                if "args" in instr:
                    for arg in instr["args"]:
                        optimize[arg] = True

        for block in blocks:
            predicate = len(block)
            block[:] = [
                instr
                for instr in block
                if "dest" not in instr or instr["dest"] in optimize
            ]
            state = predicate != len(block)

        return list(blocks)


if __name__ == "__main__":
    file = ""
    for line in fileinput.input():
        file += line

    file = json.loads(file)

    for func in file["functions"]:
        blocks = clean_blocks(func)
        clean = [inst for block in dce(blocks) for inst in block]
        func["instrs"] = clean

    print(json.dumps(file, indent=1))
