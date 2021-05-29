from Bio import Entrez
Entrez.email = "A.N.Other@example.com"     # Always tell NCBI who you are
handle = Entrez.esearch(db="pubmed", term="lung+cancer")
record = Entrez.read(handle)
count = record['Count']
handle = Entrez.esearch(db="pubmed", term="lung+cancer", retmax=count)
record = Entrez.read(handle)
print(len(record['IdList']))


