from Bio import Entrez
import json

# https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/

def search(query):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',
#                            sort='relevance',
                            retmax='20',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'your.email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

if __name__ == '__main__':
    results = search('magnetic resonance')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']):
         print("{}) {}".format(i+1, paper['MedlineCitation']['Article']['ArticleTitle']))


#print(json.dumps(papers['PubmedArticle'][0], indent=2))

