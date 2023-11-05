from urllib.request import urlopen
from urllib.parse import urlencode
from lxml import etree
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity 
import matplotlib.pyplot as plt
import time
import binf2 as b

with open('prace.txt','r') as f:
    baza = f.read().splitlines()
    f.close()

lista_mesh = []

for PMID in baza:
    baseurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    query = "db=pubmed&id="+PMID+"&format=xml"
    new_url = baseurl+query
    f = urlopen(new_url)
    result_xml = f.read()
    new_xml = etree.XML(result_xml)

    wynik = new_xml.xpath("//DescriptorName")
    time.sleep(1)
    wart_mesh = []
    for x in wynik:
        wart_mesh.append(x.text)
    lista_mesh.append(wart_mesh)

unique_words = set(sum(lista_mesh, []))
num_of_words = []

for i in range(len(lista_mesh)):
    nw = dict.fromkeys(unique_words,0)
    for word in lista_mesh[i]:
        nw[word]+=1
    
    num_of_words+=[nw]

           
def computeTF(wordDict):
    tfDict = {}
    M = wordDict.values()
    for word, count in wordDict.items():
        tfDict[word] = count/max(M)
    return tfDict
                   
tf = [computeTF(num_of_words[i]) for i in range(len(lista_mesh))]

                   
def computeIDF(documents):
    import math
    N = len(documents)
    
    idfDict = dict.fromkeys(documents[0].keys(),0)
    for document in documents:
        for word, val in document.items():
            if val>0:
                idfDict[word]+=1
    for word, val in idfDict.items():
        idfDict[word] = math.log2(N/float(val))
    return idfDict
                   
idfs = computeIDF(num_of_words)

def computeTFIDF(tfBag, idfs):
    tfidf = {}
    for word, val in tfBag.items():
        tfidf[word] = val*idfs[word]
    return tfidf           


df = pd.DataFrame([computeTFIDF(tf[i], idfs) for i in range(len(lista_mesh))])

def miara_cos(x, y):
    return np.sum(x*y)/(np.sqrt(sum(x**2))*np.sqrt(sum(y**2)))

similarity_matrix = cosine_similarity(b.TFIDF(lista_mesh)) 
similarity_df = pd.DataFrame(similarity_matrix)

plt.matshow(similarity_df)
plt.show()