import json
import sys

def argAmount(file):

	for f in file['functions']:
		for i in f['instrs']:
			if "args" in i:
				if (len(i['args']) == 0):
				  print("No arguments given")
				else:
					for a in i['args']:
						print(a)

if __name__ == '__main__':
	file = open(sys.argv[1])
	argAmount(json.load(file))