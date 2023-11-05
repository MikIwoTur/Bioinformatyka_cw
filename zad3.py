from urllib.request import urlopen
from urllib.parse import urlencode
from lxml import etree
import re

NUCLEOTIDES = []

ID = 'NM_001012006.1', 'MK560199.1', 'AB046569.1' 
for sequence in ID:
    baseurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    query = "db=nucleotide&id="+sequence+"&format=xml" 
    url = baseurl+query
    f = urlopen(url) 
    resultxml = f.read() 
    xml = etree.XML(resultxml)
    resultelements = xml.xpath("//GBSeq_sequence")
    if resultelements:
        seq = resultelements[0].text
        NUCLEOTIDES.append(seq)
        with open(sequence + '.fasta', 'w') as f:
            f.write(f'>{sequence}\n{seq}')
    else:
        print("nie znaleziono sekwencji")

for nucleotide in NUCLEOTIDES:
    print(nucleotide)

