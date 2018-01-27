import requests
import os
from clint.textui import progress

if not os.path.isfile("zhengshi.pkl"):
	print("Getting book text.")
	r = requests.get("http://www.qalaymiqan.com/data/tangshu/zhengshi.pkl", stream=True)
	with open("zhengshi.pkl", "wb") as f:
		total_length = int(r.headers.get('content-length'))
		for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024)+1):
			if chunk:
				f.write(chunk)
				f.flush()
else:
	print("Book text already present.")

if not os.path.isfile("cbdb_sqlite.db"):
	print("Getting CBDB.")
	r = requests.get("http://www.qalaymiqan.com/data/tangshu/cbdb_sqlite.db", stream=True)
	with open("cbdb_sqlite.db", "wb") as f:
		total_length = int(r.headers.get('content-length'))
		for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024)+1):
			if chunk:
				f.write(chunk)
				f.flush()
else:
	print("CBDB already present.")