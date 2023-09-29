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


OPERATORS = ["add", "mul", "eq", "and", "or", "fadd", "fmul", "feq", "ceq"]


def lvn(blocks):
    for block in blocks:
        instructions = dict(zip(range(0, len(block)), block))

        expr_to_id = {}
        var_to_id = {}
        state = {}

        id = 1

        for pair in instructions.items():
            idx = pair[0]
            instr = pair[1]

            if "dest" in instr:
                var_name = instr["dest"]

                if "value" in instr:
                    expr = (instr["op"], instr["value"])

                elif "args" in instr:
                    args = instr["args"]
                    op = instr["op"]

                    if op in OPERATORS:
                        args = sorted(args)

                    args = list(
                        map(lambda x: var_to_id[x] if x in var_to_id else x, args)
                    )
                    instr["args"] = list(
                        map(lambda x: state[x]["var"] if x in state else x, args)
                    )
                    expr = (op, *args)

                if str(expr) in expr_to_id:
                    var_to_id[var_name] = expr_to_id[str(expr)]

                else:
                    state[id] = {"expr": expr, "var": instr["dest"]}
                    expr_to_id[str(expr)] = id
                    var_to_id[var_name] = id

                    id += 1
    return blocks


if __name__ == "__main__":
    file = ""
    for line in fileinput.input():
        file += line

    file = json.loads(file)

    for func in file["functions"]:
        blocks = clean_blocks(func)
        clean = [inst for block in lvn(blocks) for inst in block]
        func["instrs"] = clean

    print(json.dumps(file, indent=1))
