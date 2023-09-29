import json
import sys
import fileinput
from brilpy import *

# Worklist for constant folding


def constant_prop(fnc, g):
    inp = [].append({})
    out = [].append({})

    if "args" in fnc:
        for arg in fnc["args"]:
            inp[0][arg["name"]] = None

    for x in range(g.n - 1):
        inp.append({})
        out.append({})

    return (inp, out)


def transfer(inp, block):
    out = {}

    for key, val in inp.items():
        out[key] = val

    # [Intra-procedural analysis](https://www.cs.cmu.edu/~aldrich/courses/15-819O-13sp/resources/interprocedural.pdf)
    for instr in block:
        if "op" in instr and "dest" in instr and instr["type"] == "int":
            if instr["op"] == "const":
                out[instr["dest"]] = instr["value"]
            elif instr["op"] == "call":
                out[instr["dest"]] = None
            else:
                if len(instr["args"]) == 1:
                    if instr["args"][0] in out and instr["args"][0] != None:
                        out[instr["dest"]] = out[instr["args"][0]]
                    else:
                        out[instr["dest"]] = None
                else:
                    if (
                        instr["args"][0] in out
                        and out[instr["args"][0]] != None
                        and instr["args"][1] in out
                        and out[instr["args"][1]] != None
                    ):
                        int_operations = {
                            "add": lambda x, y: x + y,
                            "sub": lambda x, y: x - y,
                            "mul": lambda x, y: x * y,
                            "div": lambda x, y: int(x / y),
                        }
                        out[instr["dest"]] = int_operations[instr["op"]](
                            out[instr["args"][0]], out[instr["args"][1]]
                        )
                    else:
                        out[instr["dest"]] = None
        elif "op" in instr and "dest" in instr and instr["type"] == "float":
            if instr["op"] == "const":
                out[instr["dest"]] = instr["value"]
            elif instr["op"] == "call":
                out[instr["dest"]] = None
            else:
                if len(instr["args"]) == 1:
                    if instr["args"][0] in out and instr["args"][0] != None:
                        out[instr["dest"]] = out[instr["args"][0]]
                    else:
                        out[instr["dest"]] = None
                else:
                    if (
                        instr["args"][0] in out
                        and out[instr["args"][0]] != None
                        and instr["args"][1] in out
                        and out[instr["args"][1]] != None
                    ):
                        float_operations = {
                            "fadd": lambda x, y: x + y,
                            "fsub": lambda x, y: x - y,
                            "fmul": lambda x, y: x * y,
                            "fdiv": lambda x, y: x / y,
                        }
                        out[instr["dest"]] = float_operations[instr["op"]](
                            out[instr["args"][0]], out[instr["args"][1]]
                        )
                    else:
                        out[instr["dest"]] = None
        elif "op" in instr and "dest" in instr and instr["type"] == "bool":
            if instr["op"] == "const":
                out[instr["dest"]] = instr["value"]
            elif instr["op"] == "call":
                out[instr["dest"]] = None
            else:
                if len(instr["args"]) == 1:
                    if instr["args"][0] in out and instr["args"][0] != None:
                        out[instr["dest"]] = out[instr["args"][0]]
                    else:
                        out[instr["dest"]] = None
                else:
                    if (
                        instr["args"][0] in out
                        and out[instr["args"][0]] != None
                        and instr["args"][1] in out
                        and out[instr["args"][1]] != None
                    ):
                        bool_operations = {
                            "flt": lambda x, y: x < y,
                            "fgt": lambda x, y: x > y,
                            "feq": lambda x, y: x == y,
                            "lt": lambda x, y: x < y,
                            "gt": lambda x, y: x > y,
                            "eq": lambda x, y: x == y,
                        }
                        out[instr["dest"]] = bool_operations[instr["op"]](
                            out[instr["args"][0]], out[instr["args"][1]]
                        )
                    else:
                        out[instr["dest"]] = None
    return out


def merge(map_lst):
    result = {}
    var = set()

    for m in map_lst:
        var = var | p.keys()

    for v in var:
        val = [p[v] for m in map_lst if v in m]

        if val.count(val[0]) == len(val) and None not in val:
            result[v] = val[0]
        else:
            result[v] = None
    return result


def main():
    file = ""
    for line in fileinput.input():
        file += line

    file = json.loads(file)

    for func in file["functions"]:
        print(f"{func['name']}")

        cfg = CFG(func)

        (inp, out) = run_worklist(func, rd_init, rd_xfer, rd_merge)

        for i, name in enumerate(cfg.names):
            print(f"{name}:\n {inp[i]} (in)\n {out[i]} (out)\n\n")


if __name__ == "__main__":
    main()
