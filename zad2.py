from urllib.request import urlopen
from urllib.parse import urlencode
from lxml import etree
import re


PMID = []

author_name = "Krzysztof Murzyn"
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
url = base_url+ urlencode({"db": "pubmed", "term": author_name+"[author]", "retmax": 30})

response = urlopen(url)
resultxml = response.read()
xml = etree.XML(resultxml)

Id = xml.xpath("//Id")
for elem in Id:
    PMID.append(elem.text)


Titles = []

for ID in PMID:
    baseurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    query = "db=pubmed&id="+ID+"&format=xml"
    new_url = baseurl+query
    f = urlopen(new_url)
    result_xml = f.read()
    new_xml = etree.XML(result_xml)

    wynik = new_xml.xpath("//ArticleTitle")
    if wynik:
        Titles.append(wynik[0].text)
    else:
        Titles.append("Title not found")

Abstracts = []

for ID in PMID:
    baseurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    query = "db=pubmed&id="+ID+"&format=xml"
    new_url = baseurl+query
    f = urlopen(new_url)
    result_xml = f.read()
    new_xml = etree.XML(result_xml)

    wynik = new_xml.xpath("//AbstractText")
    if wynik:
        Abstracts.append(wynik[0].text)


for abstract in Abstracts:
    molecule = len(re.findall(r"\bmolecule\b", abstract))
    print(molecule)