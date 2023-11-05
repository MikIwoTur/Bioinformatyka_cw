from urllib.request import urlretrieve
from IPython.display import Image
from urllib.request import urlopen
from lxml import etree


query = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/lopinavir/XML"
response = urlopen(query)
resultxml = response.read()
tree = etree.XML(resultxml)

sek = []
for element in tree.iter():
    if element.tag == "{http://www.ncbi.nlm.nih.gov}PC-InfoData_value_sval":
        sek.append(element.text)
        ########## masa tego związku wynosi: 628,8

smiles = sek[-2]
urlretrieve('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+smiles+'/PNG', 'smi_pic.png')
p = Image(filename='smi_pic.png')
print(p)