import json
import fileinupt

def clean_blocks(json):
  blocks, iterative = [], []

  for i in input['instrs']: 
    iterative.extend(i)
    if 'op' in i and i['op'] in {'br', 'jump', 'call', 'ret'}:
      blocks.extend(iterative)
      iterative = []

  if iterative: 
    blocks.append(iterative)

  return blocks

def dce(blocks):
  changed = True

  while changed:
    used = {}
    for b in blocks:
      for i in b:
        if 'args' in i:
          for arg in i['args']:
            used[arg] = True

    for b in blocks:
      predicate = len(b)
      b[:] = [i for i in b if 'dest' not in i or i['dest'] in used]
      changed = predicate != len(b)

if __name__ == "__main__":
  with open(sys.argv[1]) as file:
    json = json.load(file)

    for f in json["functions"]:
      f['instrs'] = [i for block in dce(clean_blocks(f)) for i in block]