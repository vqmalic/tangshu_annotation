import json
import pandas as pd

# load gold standard
df = pd.read_pickle("samples/expertsample.pkl")
gold = []
for x in df['annotation']:
	gold.extend(x)

# evaluate CoreNLP

j = json.load(open("samples/annotatedsample_corenlp.json", "r"))
out = []
nlpsen = []
for sentence in j['sentences']:
	for token in sentence['tokens']:
		l = len(token['originalText'])
		if token['ner'] == 'PERSON':
			out.extend(l * [1])
		else:
			out.extend(l * [0])
'''
for sentence in j['sentences']:
	this = []
	thissen = []
	for token in sentence['tokens']:
		thissen.append(token['originalText'])
		l = len(token['originalText'])
		if token['ner'] == 'PERSON':
			this.extend(l * [1])
		else:
			this.extend(l * [0])
	nlpsen.append(''.join(thissen))
	out.append(this)
'''

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
print("accuracy: {}".format(accuracy_score(gold, out)))
print("precision: {}".format(precision_score(gold, out)))
print("recall: {}".format(recall_score(gold, out)))
print("f1: {}".format(f1_score(gold, out)))
print(confusion_matrix(gold, out))