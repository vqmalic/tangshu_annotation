import pandas as pd

out = []

with open("samples/expertsample.txt", "r") as f:
	lines = f.readlines()
	for line in lines:
		line = line.replace("\n", "")
		ne = False
		orig = []
		anno = []
		for char in line:
			if char == "{":
				ne = True
			elif char == "}":
				ne = False
			else:
				if ne:
					anno.append(1)
				else:
					anno.append(0)
				orig.append(char)
		out.append([''.join(orig), anno])

df = pd.DataFrame(out, columns=['text', 'annotation'])
df.to_pickle("samples/expertsample.pkl")
