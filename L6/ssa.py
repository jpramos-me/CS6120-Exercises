import copy
import argparse
import copy
import sys
import json

from form_blocks import form_blocks
from dominators import find_dom, find_dom_frontier, find_dom_tree
from cfg import *


def out_ssa(cfg):
    for v, block in cfg.items():
        for i in block.instrs:
            if i.get("op") == "phi":
                dest = i["dest"]
                typ = i["type"]
                for d, label in enumerate(instr["labels"]):
                    var = instr["args"][d]
                    if var == "undef":
                        continue
                    copy_i = {"op": "id", "type": typ, "args": [var], "dest": dest}
                    cfg[label].i.insert(-1, copy_i)
        block.i = [i for i in copy.deepcopy(block.i) if i.get("op") != "phi"]

def into_ssa(cfg):
  