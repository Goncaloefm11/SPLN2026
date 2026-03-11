import requests
from bs4 import BeautifulSoup
import json
import string

def extrai_pagina(url):
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    
    res = {}
    doencas_div = soup.find_all('div', class_='views-row')

    for div in doencas_div:
        try:
            designacao = div.div.h3.a.text
            descricao = div.find('div', class_='views-field-body').div.text
            res[designacao] = descricao.strip()
        except:
            continue
    
    return res

url_base = 'https://www.atlasdasaude.pt/doencasaaz'
res = {}

for l in string.ascii_lowercase:
    res = res | extrai_pagina(url_base + '/' + l)

f_out = open("doencas.json", "w", encoding="utf-8")
json.dump(res, f_out, indent=4, ensure_ascii=False)
f_out.close()
