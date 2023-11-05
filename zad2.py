from urllib.request import urlopen
from urllib.parse import urlencode
from lxml import etree
import re


PMID = []

autor = "Krzysztof Murzyn"
bazowy_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
url = bazowy_url + urlencode({"db": "pubmed", "term": autor+"{author}"})

otwarcie = urlopen(url)
otwarcie_lxml = otwarcie.read()
xml = etree.XML(otwarcie_lxml)

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
    else:
        Abstracts.append("Title not found")

for abstract in Abstracts:
    muscle = re.findall("molecule", abstract)
    print(len(muscle))


