import pandas as pd

s1 = pd.read_csv("samples/sample1.csv", index_col=0)
s2 = pd.read_csv("samples/sample2.csv", index_col=0)

overlap = set(s1.index).intersection(s2.index)

so = s1.loc[list(overlap)]
so = so.sort_values(by=['book', 'juan', 'juansuffix', 'paraIdx'])

np.random.seed(3057)
o1 = np.random.choice(range(20), 10, replace=False)
o2 = np.random.choice(range(20, 40), 10, replace=False)
o = list(o1) + list(o2)

newso = so.iloc[o]

s1sub = s1.loc[list(set(s1.index) - overlap)]
s1suba = s1sub[s1sub['book'] == "New_Book_of_Tang"]
s1subb = s1sub[s1sub['book'] == "Old_Book_of_Tang"]
news1 = pd.concat([newso, s1suba.sample(10), s1subb.sample(10)])

s2sub = s2.loc[list(set(s2.index) - overlap)]
s2suba = s2sub[s2sub['book'] == "New_Book_of_Tang"]
s2subb = s2sub[s2sub['book'] == "Old_Book_of_Tang"]
news2 = pd.concat([newso, s2suba.sample(10), s2subb.sample(10)])

news1 = news1.sort_values(by=['book', 'juan', 'juansuffix', 'paraIdx'])
news2 = news2.sort_values(by=['book', 'juan', 'juansuffix', 'paraIdx'])

news1.to_csv("samples/minisample1.csv")
news2.to_csv("samples/minisample2.csv")