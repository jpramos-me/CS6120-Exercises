import json
import copy
import fileinput
import argparse
import sys

from collections import OrderedDict
from form_blocks import form_blocks
from cfg import *


"""
Pretty printer helpers
"""


def dom_tree_printer(dt):
    s = OrderedDict()
    sort = list(dt.keys())
    sort.sort()
    for v in sort:
        l = list(dt[v].succs)
        l.sort()
        s[v] = l
    print(json.dumps(s, indent=1))


def printer(dom):
    s = OrderedDict()
    sort = list(dom.keys())
    sort.sort()
    for v in sort:
        l = list(dom[v])
        l.sort()
        s[v] = l
    print(json.dumps(s, indent=1))


"""
Dominator algorithm
"""


def worklist(cfg, merge, transfer):
    ins = dict()
    out = dict()
    for label, _ in cfg.items():
        ins[label] = set()
        out[label] = set()

    wl = copy.deepcopy(cfg)

    while len(wl) > 0:
        label = list(wl.keys())[0]
        bb = wl.pop(label)
        bb_in = [out[label] for label in bb.pred]
        bb_in_merge = merge(bb_in)
        bb_out = transfer(bb, bb_in_merge)
        if len(bb_out) != len(out[label]):
            out[label] == bb_out

    return out


def merg(ins):
    s = set()
    if len(ins) > 0:
        s.update(ins[0])

    for i in ins:
        if len(i) == 0:
            continue
            s = s.intersection(i)
    return s


def trans(bb, ins):
    label = bb.instrs[0]["label"]
    ins.add(label)
    return ins


def find_dom_work(cfg):
    return worklist(cfg, merg, trans)


def find_dom(cfg):
    dom = dict()
    while True:
        changed = False
        for v, bb in cfg.items():
            if v not in dom:
                dom[v] = list()
            pred_dom = [dom[p] for p in bb.pred if p in dom]
            common_dom = set.intersection(*pred_dom) if len(pred_dom) > 0 else set()
            common_dom.add(v)
            if common_dom != dom[v]:
                dom[v] = common_dom
                changed = True
        if not changed:
            break
    return dom


class Node:
    def __init__(self, name) -> None:
        self.name = name
        self.preds = []
        self.succs = []


def find_dom_tree(dom, cfg):
    dom_tree = dict()
    for v in cfg.keys():
        dominators = copy.deepcopy(dom[v])
        dominators.remove(v)
        ldom = list()
        for d in dominators:
            domed = list()
            for ve, doms in dom.items():
                if d in doms:
                    domed.append(ve)
            immediate_dom = True
            for dd in dominators:
                if dd == d:
                    continue
                if dd in domed:
                    immediate_dom = False
                    break
            if immediate_dom:
                ldom.append(d)
        for parent in ldom:
            if v not in dom_tree:
                dom_tree[v] = Node(v)
            if parent not in dom_tree:
                dom_tree[parent] = Node(parent)
            dom_tree[parent].succs.append(v)
            dom_tree[v].preds.append(parent)
    return dom_tree


def find_dom_frontier(dom, cfg):
    dom_frontier = dict()
    for v in cfg.keys():
        dom_frontier[v] = set()
        domed = list()
        for ve, dominators in dom.items():
            if v in dominators:
                domed.append(ve)
        for d in domed:
            for suc in cfg[d].succ:
                if suc not in domed or suc == v:
                    dom_frontier[v].add(suc)
    return dom_frontier


def main(args):
    dom_print = args.dom
    dom_tree = args.dom_tree
    dom_frontier = args.dom_frontier
    dom_worklist = args.dom_worklist
    directory = args.dir

    if directory is not None:
        with open(directory, "r") as d:
            file = json.load(d)
    else:
        file = json.load(sys.stdin)

    for func in file["functions"]:
        blocks = form_blocks(func["instrs"])
        blocks = [b for b in blocks if len(b) > 0]
        cfg = CFG(blocks).cfg

        if dom_worklist:
            dom = find_dom_work(cfg)
            printer(dom)
        else:
            dom = find_dom(cfg)
            printer(dom)

        if dom_print:
            printer(dom)

        if dom_tree:
            tree = find_dom_tree(dom, cfg)
            dom_tree_printer(tree)

        if dom_frontier:
            frontier = find_dom_frontier(dom, cfg)
            printer(frontier)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-dom", dest="dom", default=False, action="store_true", help="print dominator"
    )
    parser.add_argument(
        "-tree",
        dest="dom_tree",
        default=False,
        action="store_true",
        help="print dominance tree",
    )
    parser.add_argument(
        "-frontier",
        dest="dom_frontier",
        default=False,
        action="store_true",
        help="print dominance frontier",
    )
    parser.add_argument(
        "-worklist",
        dest="dom_worklist",
        default=False,
        action="store_true",
        help="use worklist algorithm to find dominator",
    )
    parser.add_argument("-d", dest="dir", action="store", type=str, help="json file")
    args = parser.parse_args()
    main(args)
