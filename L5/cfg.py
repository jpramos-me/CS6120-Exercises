"""
The core logic for constructing a CFG was adapted in part from [bril's implementation](https://github.com/sampsyo/bril/blob/e72ab48ff45e2928c875a259d46409865cc2262e/bril-llvm/brilpy.py)
"""

TERMINATORS = ["jmp", "ret", "br"]


class Block(object):
    def __init__(self, block):
        self.instrs = block
        self.pred = []
        self.succ = []


class CFG(object):
    def __init__(self, blocks, reverse=False):
        self.labels = list()
        self.blocks = blocks
        self.cfg = dict()
        self.reverse = reverse
        self.build_cfg()

    def build_cfg(self):
        for block in self.blocks:
            bb = Block(block)
            label = "start"
            if "label" in block[0]:
                label = block[0]["label"]
            self.cfg[label] = bb
            self.labels.append(label)

        labels = list(self.cfg.keys())
        for idx, label in enumerate(labels):
            bb = self.cfg[label]
            op = bb.instrs[-1]["op"]
            if op not in TERMINATORS:
                if idx == len(labels) - 1:
                    continue
                else:
                    jmp_target = self.cfg[labels[idx + 1]].instrs[0]["label"]
                    if self.reverse:
                        self.cfg[label].pred.append(jmp_target)
                        self.cfg[jmp_target].succ.append(label)
                    else:
                        self.cfg[label].succ.append(jmp_target)
                        self.cfg[jmp_target].pred.append(label)
            elif op == "jmp":
                jmp_target = bb.instrs[-1]["labels"][0]
                if self.reverse:
                    self.cfg[label].pred.append(jmp_target)
                    self.cfg[jmp_target].succ.append(label)
                else:
                    self.cfg[label].succ.append(jmp_target)
                    self.cfg[jmp_target].pred.append(label)
            elif op == "br":
                br_targets = bb.instrs[-1]["labels"]
                for target in br_targets:
                    if self.reverse:
                        self.cfg[label].pred.append(target)
                        self.cfg[target].succ.append(label)
                    else:
                        self.cfg[label].succ.append(target)
                        self.cfg[target].pred.append(label)

    def gen_instrs(self):
        instrs = list()
        for label in self.labels:
            instrs.append({"label": label})
            instrs.extend(self.cfg[label].instrs)
        return instrs
