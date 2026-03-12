import requests
from bs4 import BeautifulSoup
import re
import json
import time

BASE_URL = "https://www.atlasdasaude.pt/doencasAaZ"

def extrair_info_doenca(url_doenca):
    try:
        res = requests.get(url_doenca, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Selecionamos a div que contém o texto
        corpo = soup.find('div', class_='field-name-body')
        if not corpo:
            return None

        # Transformar o HTML em texto simples
        texto = corpo.get_text(separator="\n")
        
        # 1. Marcar as secções com @ 
        # Procurar as palavras-chave no início de uma linha
        texto = re.sub(r"\n(Causas|Sintomas|Tratamento)", r"\n@\1", texto)

        # 2. Dividir o texto pelo marcador @
        blocos = re.split(r"@", texto)

        res_dados = {
            "causas": "Não encontrado",
            "sintomas": "Não encontrado",
            "tratamento": "Não encontrado"
        }

        # 3. Processar cada bloco
        for bloco in blocos:
            if bloco.startswith("Causas"):
                # Remover a palavra "Causas" para ficar só o conteúdo
                res_dados["causas"] = bloco.replace("Causas", "").strip()
            
            elif bloco.startswith("Sintomas"):
                res_dados["sintomas"] = bloco.replace("Sintomas", "").strip()
            
            elif bloco.startswith("Tratamento"):
                res_dados["tratamento"] = bloco.replace("Tratamento", "").strip()

        return res_dados

    except Exception as e:
        print(f"Erro em {url_doenca}: {e}")
        return None

def scrap_total_atlas():
    entries = {} # O teu dicionário final
    letras = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    
    for letra in letras:
        print(f"Lendo letra: {letra.upper()}")
        url_letra = f"{BASE_URL}/{letra}"
        
        page = 0
        while True:
            response = requests.get(url_letra, params={'page': page})
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extrair links das doenças
            links = soup.select('.views-field-title a')
            if not links:
                break
                
            for link in links:
                nome_doenca = link.text.strip()
                link_final = "https://www.atlasdasaude.pt" + link['href']
                
                # Chamar a função de extração e guardamos no dicionário
                info = extrair_info_doenca(link_final)
                if info:
                    entries[nome_doenca] = info
                    print(f" -> {nome_doenca} processada.")
                
                time.sleep(0.1) # Pausa pequena
            
            # Se não houver botão "seguinte", para de procurar páginas desta letra
            if not soup.select('.pager-next'):
                break
            page += 1

    return entries

entries = scrap_total_atlas()

f_out = open("dicionario_atlas.json", "w", encoding="utf8")
json.dump(entries, f_out, indent=4, ensure_ascii=False)
f_out.close()

print(f"Concluído! {len(entries)} doenças guardadas.")