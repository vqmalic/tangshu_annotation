import pandas as pd
import numpy as np

np.random.seed(3057)

ms1_v1 = pd.read_csv("annotated/minisample1.csv", index_col=0)
ms2_v1 = pd.read_csv("annotated/minisample2.csv", index_col=0, encoding='utf-16')

s1 = pd.read_csv("samples/sample1.csv", index_col=0)
s2 = pd.read_csv("samples/sample2.csv", index_col=0)

done = set(ms1_v1.index).union(set(ms2_v1.index))
done_overlap = set(ms1_v1.index).intersection(set(ms2_v1.index))

overlap = set(s1.index).intersection(set(s2.index))
overlap_cands = overlap - done_overlap

s1nt = set(s1[s1['book'] == 'New_Book_of_Tang'].index)
s1nt = s1nt - done
s1nt = s1nt - overlap
s1ot = set(s1[s1['book'] == 'Old_Book_of_Tang'].index)
s1ot = s1ot - done
s1ot = s1ot - overlap

news1 = list(np.random.choice(list(s1nt), 27, replace=False)) + list(np.random.choice(list(s1ot), 27, replace=False))

s2nt = set(s2[s2['book'] == 'New_Book_of_Tang'].index)
s2nt = s2nt - done
s2nt = s2nt - overlap
s2ot = set(s2[s2['book'] == 'Old_Book_of_Tang'].index)
s2ot = s2ot - done
s2ot = s2ot - overlap

news2 = list(np.random.choice(list(s2nt), 27, replace=False)) + list(np.random.choice(list(s2ot), 27, replace=False))
newo = list(np.random.choice(list(overlap_cands), 6))

news1 = news1 + newo
news2 = news2 + newo

sub1 = s1.loc[news1].copy()
sub2 = s2.loc[news2].copy()

sub1['comments'] = [""] * sub1.shape[0]
sub2['comments'] = [""] * sub2.shape[0]

sub1.to_csv("samples/minisample1_p2.csv", encoding='utf-8')
sub2.to_csv("samples/minisample2_p2.csv", encoding='utf-8')