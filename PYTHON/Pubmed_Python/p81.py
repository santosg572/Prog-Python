from Bio import Entrez
import time

Entrez.email = "A.N.Other@example.com" 

TERMINO = "anova"

handle = Entrez.esearch(db="pubmed", term=TERMINO)
record = Entrez.read(handle)

count = int(record['Count'])
print(count)

handle = Entrez.esearch(db="pubmed", term=TERMINO, retmax=count, datetype='pdat', mindate='2019', maxdate='2020')
record = Entrez.read(handle)

count = int(record['Count'])
print(count)

id_list = record['IdList']
post_xml = Entrez.epost("pubmed", id=",".join(id_list))
search_results = Entrez.read(post_xml)

webenv = search_results["WebEnv"]
query_key = search_results["QueryKey"] 

try:
    from urllib.error import HTTPError  # for Python 3
except ImportError:
    from urllib2 import HTTPError  # for Python 2

batch_size = 200

out_handle = open("segmentation.txt", "w")
for start in range(0, count, batch_size):
    end = min(count, start+batch_size)
    print("Going to download record %i to %i" % (start+1, end))
    attempt = 0
    while attempt < 3:
        attempt += 1
        try:
            fetch_handle = Entrez.efetch(db="pubmed",
                                         retstart=start, retmax=batch_size,
                                         webenv=webenv, query_key=query_key)
        except HTTPError as err:
            if 500 <= err.code <= 599:
                print("Received error from server %s" % err)
                print("Attempt %i of 3" % attempt)
                time.sleep(15)
            else:
                raise
    data = fetch_handle.read()
    fetch_handle.close()
    out_handle.write(data)
out_handle.close()


