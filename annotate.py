import pandas as pd
import sqlite3
import re
import numpy as np
from clint.textui import progress

# load juans

juans = pd.read_pickle("zhengshi.pkl")
juans = juans[juans['sourcebook'].isin(["Old_Book_of_Tang", "New_Book_of_Tang"])]

# load CBDB

conn = sqlite3.connect("cbdb_sqlite.db")
c = conn.cursor()
c.execute('''
	SELECT BIOG_MAIN.c_personid, c_name_chn, c_index_year, c_birthyear, c_death_age, c_death_age_approx, c_surname_chn, c_mingzi_chn, c_alt_name_chn
	FROM BIOG_MAIN LEFT JOIN ALTNAME_DATA
	ON BIOG_MAIN.c_personid == ALTNAME_DATA.c_personid''')
all_rows = c.fetchall()
conn.close()

# bio data frame
# people in Tang period
# OR, people with no date information

people = pd.DataFrame(all_rows, columns=['id', 'name', 'index', 'birth', 'death', 'death_age', 'surname', 'mingzi', 'alt_name'])
print("{} people in the CBDB.".format(len(list(set(people['id'])))))
print("Filtering by date.")
keep = []
ymin = 618 - 80
ymax = 907 + 80

for _, row in people.iterrows():
	k = False
	if pd.isnull(row['birth']) and pd.isnull(row['death']):
		k = True
	else:
		if pd.notnull(row['birth']):
			if ymin < row['birth'] < ymax:
				k = True
		if pd.notnull(row['death']):
			if ymin < row['death'] < ymax:
				k = True
	keep.append(k)
people = people[keep]
print("{} people remaining in the CBDB.".format(len(list(set(people['id'])))))

# gather remaining people's names into set
names = []
for _, row in people.iterrows():
	if pd.notnull(row['name']):
		names.append(row['name'])
	if pd.notnull(row['alt_name']):
		names.append(row['alt_name'])
names = list(set(names))
print("{} unique names found.".format(len(names)))
print("Filtering problematic names.")
print("Removing names with reserved regular expression characters in them.")
names = [x for x in names if '[' not in x]
names = [x for x in names if '?' not in x]
names = [x.split("(")[0] if "(" in x else x for x in names]
names = [x.split("（")[0] if "（" in x else x for x in names]
print("Removing names that are only numerical characters.")
nums = set("一二三四五六七八九十百千萬")
names = [x for x in names if not set(x).issubset(nums)]
print("Removing names with only one character.")
names = [x for x in names if len(x) > 1]
print("{} unique names remain.".format(len(names)))


#############ALT
merged = 'б'.join(juans['raw'])
matches = []
i = 0
print("Identifying matches...")
with progress.Bar(expected_size=len(names)) as bar:
	for entry in names:
		try:
			p = re.compile(entry)
			for m in p.finditer(merged):
				s = m.span()
				if s[1] - s[0] == 1:
					print(entry)
				if s[0] != s[1]:
					matches.append(m.span())
		except:
			pass
		i += 1
		bar.show(i)

def is_subset(a, b):
    if a[0] >= b[0] and a[1] <= b[1]:
        return True
    else:
        return False

m = matches
j = merged

m = list(set(m))
m = sorted(m, key=lambda x:x[0])

print("Filtering matches...")
filtered = []
i = 0
with progress.Bar(expected_size=len(names)) as bar:
	for k, x in enumerate(m):
		add = True
		for y in m[np.max([k-50, 0]):np.min([k+50, len(m)])]:
			if x == y:
				pass
			else:
				if is_subset(x, y):
					add = False
		if add:
			filtered.append(x)
		i += 1
		bar.show(i)

print("Segmenting...")
segmented = []
with progress.Bar(expected_size=len(filtered)) as bar:
	for i, (a, b) in enumerate(filtered):
		if i == 0:
			segmented.append(j[0:a])
			segmented.append("  {{" + j[a:b] + "}}  ")
		elif i == len(filtered):
			segmented.append(j[filtered[i-1][1]:a])
			segmented.append("  {{" + j[a:b] + "}}  ")
			segmented.append(j[b:len(j)-1])
		else:
			segmented.append(j[filtered[i-1][1]:a])
			segmented.append("  {{" + j[a:b] + "}}  ")
		i += 1
		bar.show(i)

new = ''.join(segmented)
new = new.split('б')

juans['raw_ner_tagged'] = new
print("Done. Saving to tangannotated.pkl")
juans.to_pickle("tangannotated.pkl")

'''
# go through each juan and get indices of any matches
print("Now finding name matches in text.")

ji_matches = []
i = 0
with progress.Bar(expected_size=juans.shape[0]) as bar:
	for ji, row in juans.iterrows():
		these_matches = []
		for entry in names:
			try:
				p = re.compile(entry)
				for m in p.finditer(row['raw']):
					s = m.span()
					if s[1] - s[0] == 1:
						print(entry)
					if s[0] != s[1]:
						these_matches.append(m.span())
			except:
				pass
		ji_matches.append(these_matches)
		i += 1
		bar.show(i)

juans['matches'] = ji_matches

# annotate the raw text
# if a match is inside another match, remove it

def is_subset(a, b):
    if a[0] >= b[0] and a[1] <= b[1]:
        return True
    else:
        return False

segmented_col = []

for _, row in juans.iterrows():
	j = row['raw']
	m = row['matches']
	# if a match is inside another match, remove it
	m = list(set(m))
	m = sorted(m, key=lambda x:x[0])
	filtered = []
	for x in m:
		add = True
		for y in m:
			if x == y:
				pass
			else:
				if is_subset(x, y):
					add = False
		if add:
			filtered.append(x)
	segmented = []
	for i, (a, b) in enumerate(filtered):
		if i == 0:
			segmented.append(j[0:a])
			segmented.append("  [" + j[a:b] + "]  ")
		elif i == len(filtered):
			segmented.append(j[filtered[i-1][1]:a])
			segmented.append("  [" + j[a:b] + "]  ")
			segmented.append(j[b:len(j)-1])
		else:
			segmented.append(j[filtered[i-1][1]:a])
			segmented.append("  [" + j[a:b] + "]  ")
	segmented_col.append(''.join(segmented))

juans['raw_ner_tagged'] = segmented_col
juans.to_pickle("zhengshi.pkl")
'''