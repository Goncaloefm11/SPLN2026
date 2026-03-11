import json

f= open("../aula3-3Mar/dicionario_medicina.json", "r", encoding="utf-8")

dados = json.load(f)
markdown = """---
title: Dicionário Médico PT
author:
    - Gonçalo M.
    - SPLN
    - Universidade do Minho
classoption: twocolumn
---\n\n"""

for conceito in dados:
    markdown += f"## {conceito} {dados[conceito]['pt']}\n"
    markdown += dados[conceito]['dom'] + "\n"
    if "dom" in dados[conceito]:
        markdown += f"Domínios: {dados[conceito]['dom']}\n"
    if "sin" in dados[conceito]:
        markdown += f"Síntomas: {dados[conceito]['sin']}\n"
    if "var" in dados[conceito]:
        markdown += f"Variantes: {dados[conceito]['var']}\n"
    if "es" in dados[conceito]:    
        markdown += f"Espanhol: {dados[conceito]['es']}\n"
    if "en" in dados[conceito]:    
        markdown += f"Inglês: {dados[conceito]['en']}\n"
    if "la" in dados[conceito]:    
        markdown += f"Latim: {dados[conceito]['la']}\n"
    if "ga" in dados[conceito]:    
        markdown += f"Galego: {dados[conceito]['ga']}\n"
    if "notas" in dados[conceito]:
        markdown += f"Notas: {dados[conceito]['notas']}\n"
    markdown += "\n\n"

f.out= open("dicionario.md", "w", encoding="utf-8")
f.out.write(markdown)
f.out.close()
