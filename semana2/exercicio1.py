# ler um ficheiro 
import re
f = open("medicina.txt", encoding="utf8")
texto = f.read()

#marcar conceitos 
texto = re.sub(r"\n(\d+) ", r"\n@\1 ", texto)

#extrair conceitos
conceitos = re.split("@", texto)

def processar_conceitos(c):
    c = re.sub(r"SIN\.-", r"@SIN.-", c)
    c = re.sub(r"VAR\.-", r"@VAR.-", c)
    c = re.sub(r"Nota\.-", r"@Nota.-", c)
    c = re.sub(r"\n(en|pt|la|es) ", r"\n#\1 ", c)

    #extrair 
    id = re.search(r"^(\d+) ", c)
    sin = re.search(r"@SIN\.-([^#@]+)", c)
    var = re.search(r"@VAR\.-([^#@]+)", c)
    nota = re.search(r"@Nota\.-([^@#]+)", c)
    lingua = re.findall(r"#(la|en|pt|es) ([^#@]+)", c)
    #print(lingua)

    galego_dominio = re.search(r"\d+ (.*)\n(.*)", c)
    galego = galego_dominio.group(1)
    dominio = galego_dominio.group(2)

    res = {}
    
    if nota:
        res["nota"] = nota.group(1)
    if var:
        res["var"] = var.group(1)
    if sin:
        res["sin"] = sin.group(1)
    res["galego"] = galego
    res["dominio"] = dominio

    for l, t in lingua:
        res[l] = t

    return res, id.group(1)


entries = {}

for c in conceitos [1:] :
    res, id = processar_conceitos(c)
    entries[id] = res


import json

f_out = open("dicionario_medicina.json", "w", encoding="utf8")
json.dump(entries, f_out,indent=4, ensure_ascii=False)


'''
CONCEITO
    id 
        - num
    traduçoes
        -galego
        -espanhol
        -ingles
        -portugues
    dominio*
    sinonimo
    nota
'''
