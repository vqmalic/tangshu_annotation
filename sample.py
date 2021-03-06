import pandas as pd
import sqlite3
import re
import numpy as np
from clint.textui import progress
import pickle

# load juans
juans = pd.read_pickle("samples/zhengshi.pkl")
# trim
boo = []
for x in juans['text']:
	if "《" in x and "卷" in x:
		boo.append(False)
	else:
		boo.append(True)
juans = juans[boo]

old = juans[juans['book'].isin(['Old_Book_of_Tang'])]
new = juans[juans['book'].isin(['New_Book_of_Tang'])]
n = 75

os = old.sample(n=n, random_state=3057)
ns = new.sample(n=n, random_state=3057)

out = pd.concat([os, ns])
out = out.drop(['compileIdx', 'chronIdx'], axis=1)
out = out.sort_values(by=['book', 'juan', 'juansuffix', 'paraIdx'])
out.to_csv("samples/sample1.csv")

# Generate second sample, with overlap

irr_size = 40

irr_0 = os.sample(n=int(irr_size/2), random_state=3057)
irr_1 = ns.sample(n=int(irr_size/2), random_state=3057)
irr = pd.concat([irr_0, irr_1])

os = old.sample(n=n-int(irr_size/2), random_state=7503)
ns = new.sample(n=n-int(irr_size/2), random_state=7503)

out = pd.concat([irr, os, ns])
out = out.drop(['compileIdx', 'chronIdx'], axis=1)
out = out.sort_values(by=['book', 'juan', 'juansuffix', 'paraIdx'])
out.to_csv("samples/sample2.csv")

s1 = pd.read_csv("samples/sample1.csv", index_col=0)
s2 = pd.read_csv("samples/sample2.csv", index_col=0)
idx = set(s1.index).intersection(s2.index)
print(len(idx))


#oldsents = '''師凡十餘萬，至大非川，為欽陵所拒，#王師#敗績，遂滅吐谷渾而盡有其地б睿宗時、#薛稷#、賈膺福、#崔湜#，又代其任б《汝洛集》一卷#裴度#、#劉禹錫#唱和б以禦史中丞#裴冕#為中書侍郎、同中書門下平章事б《劉白唱和集》三卷#劉禹錫#、#白居易#б正月乙酉，宣武軍節度使#韓弘#守#司徒#б景福二年，陰令左右告敬瑄、令孜養死士，約#楊晟#等反，於是斬敬瑄於家б」鵬卒，後石至宰相，福歷七鎮，諸#孫通#顯雲б禦史中丞#裴度#以禹錫母老，請移近處，乃改授連州刺史б二人者，本契丹李盡忠部將，盡忠入寇，楷固等數挫#王師#，後降，有司請論如法б初，#張柬之#代為荊州，共乘艫江中，私語外家革命，元琰悲涕慷慨，誌在王室б甲辰，以禮部尚書、東京留守#韋陟#為吏部尚書，太子賓客#房琯#為禮部尚書б悅與淄青兵三萬餘人陣於洹水，#馬燧#等三帥與神策將#李晟#等來攻，悅之衆復敗，死傷二萬計б後為#郭子儀#朔方節度留後，大將孫守亮擁重兵，驕蹇不受制，嗣恭因稱疾，守亮至，即殺之，一軍皆震б」有詔#李元#諒、韓全義率師一萬，會遊瑰收鹽州б先是遣右率府長史#王玄#策使天竺，其四天竺國王鹹遣使朝貢б時都統王鐸前鋒都將#李系#守潭州，有眾五萬，並諸團結軍號十萬б與#楊炎#善，薦為補闕，歷都官員外郎б公往不遺於#李密#，今豈負於朕哉б琇稱疾罷，而滉為度支、諸道鹽鐵、轉運使，於是#崔造#亦罷б在漢州，##張嘉#貞#為益州長史、判都督事，性簡貴，待管內刺史禮隔，而引擇言同榻，坐談政理，時人榮之б服除，#李逢吉#辟置宣武府б馮朝隱註《老子》白履忠註《老子》#李播#註《老子》尹知章註《老子》#傅弈#《老子音義》並卷亡б」明年九月，#郭子儀#收復兩京б#鄭畋#，字臺文，滎陽人也б順宗即位，風疾不能視朝政，而宦官#李忠#言與牛美人侍病б申，嗣虢#王則#之從父甥也б#李懷#光亂河中，輒解去б八月丙寅，#王縉#為侍中，都統河南、淮南、山南東道節度行營事б是時程休、邢宇、宇弟宙、#張茂#之、李、族子丹叔、惟嶽、喬潭、楊拯、房垂、柳識皆號門弟子б己卯，以河南尹王璠為右丞，以左散騎常侍#馮宿#為河南尹б內侍#高力士#曰：「陛下新即位，宜與大臣裁可否б府屬#孔戡#等屢以直語爭刺，初唯唯，後益不從，皆引去б而##楊嗣#復#、李玨相次輔政，夷行介特，雅不與合，每議論天子前，往往語相侵短б#元振#自恃功勛，怏怏不得誌，道病卒б#呂諲#政事出揆遠甚，以故宰相鎮荊南，治聲尤高б時高宗將廢皇後王氏而立武昭儀，行儉以為國家憂患必從此始，與太尉長孫無忌、尚書左僕射#褚遂良#私議其事，大理#袁公瑜#於昭儀母榮國夫人譖之，由是左授西州都督府長史б」玄宗東巡狩，詔州縣敦勸見行在，時九十餘，帝令#張說#訪以政事，宦官扶入宮中，與語甚悅，拜國子博士，聽還山б乙酉，周#王顯#為洮河道行軍元帥，領左衛大將軍劉審禮等十二總管，相王輪為涼州道行軍元帥，領契苾何力等軍，以伐吐蕃б」#薛元超#贊帝曰：「漢欲廢嫡立庶，故四人者為出，豈如陛下親降岩穴邪'''

'''
# split by sentence

sentout = []
sb = set(list("。．？！!.﹒﹖﹗．?"))

for juan in list(juans['raw_ner_tagged']):
    for x in sb:
        juan = juan.replace(x, "б")
    sents = juan.split("б")
    for x in sents:
        if "{{" in x:
            sentout.append(x)


oldsents = oldsents.split("б")
newsents = []

for catch in oldsents:
	caught = False
	for x in sentout:
		a = catch.replace("#", "")
		a = a.replace(" ", "")
		a = a.replace("\n", "")
		b = x.replace("{{", "")
		b = b.replace("}}", "")
		b = b.replace(" ", "")
		b = b.replace("\n", "")
		a = set(a)
		b = set(b)
		if len(a.intersection(b)) == len(a):
			newsents.append(x)
			caught = True
	if caught == False:
		print(catch)

with open("samples/annotatedsample.pkl", "wb") as f:
	pickle.dump(newsents, f)

with open("samples/annotatedsample.txt", "w") as f:
	for sent in newsents:
		f.write(sent + "\n\n")
'''