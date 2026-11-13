#!/usr/bin/env python3
"""Monta em _site/ exatamente o que vai para o ar, e nada mais.

    python3 montar-site.py

O repositório guarda muito além do site — os folders impressos, o manual da marca,
os PDFs de `fontes/` e `envio/`. Nada disso é publicado: este script copia as páginas,
o CSS, o JS, os Termos e só as imagens que as páginas realmente pedem, e escreve o
CNAME do domínio. O GitHub Pages publica essa pasta.
"""
import os
import re
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "_site")
DOMINIO = "dawrahecarmona.com.br"
PAGINAS = ["index.html", "360/index.html", "workshop/index.html", "aevum/index.html", "termos.html"]
SOLTOS = ["site-base.css", "site.js"]


def recursos():
    """As imagens que as páginas pedem, pelo caminho a partir da raiz do site."""
    usados = set()
    for p in PAGINAS:
        h = open(os.path.join(AQUI, p), encoding="utf-8").read()
        pasta = os.path.dirname(p)
        for ref in re.findall(r'(?:src|href)="([^"]+)"', h) + re.findall(r"url\(([^)]+)\)", h):
            ref = ref.strip("'\"")
            if ref.startswith(("#", "data:", "http", "mailto:")):
                continue
            if not re.search(r"\.(jpg|jpeg|png|webp|svg|ico)$", ref, re.I):
                continue
            usados.add(os.path.normpath(os.path.join(pasta, ref)))
    return sorted(usados)


def monta():
    if os.path.exists(SAIDA):
        shutil.rmtree(SAIDA)
    os.makedirs(SAIDA)
    for p in PAGINAS + SOLTOS:
        destino = os.path.join(SAIDA, p)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        shutil.copy2(os.path.join(AQUI, p), destino)
    imagens = recursos()
    for r in imagens:
        origem = os.path.join(AQUI, r)
        if not os.path.exists(origem):
            raise SystemExit(f"a página pede {r} e o arquivo não existe")
        destino = os.path.join(SAIDA, r)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        shutil.copy2(origem, destino)
    # O CNAME só entra quando o domínio já apontar para o GitHub. Enquanto não
    # existir o arquivo na raiz, o site responde em <usuario>.github.io/<repo> e dá
    # para conferir sem mexer no DNS — com o CNAME, o Pages passa a redirecionar
    # para o domínio e o endereço de teste deixa de abrir.
    tem_cname = os.path.exists(os.path.join(AQUI, "CNAME"))
    if tem_cname:
        shutil.copy2(os.path.join(AQUI, "CNAME"), os.path.join(SAIDA, "CNAME"))

    # nada além do previsto pode ter entrado
    publicados = {os.path.relpath(os.path.join(raiz, f), SAIDA)
                  for raiz, _, arqs in os.walk(SAIDA) for f in arqs}
    esperados = set(PAGINAS) | set(SOLTOS) | set(imagens) | ({"CNAME"} if tem_cname else set())
    sobrando = publicados - esperados
    if sobrando:
        raise SystemExit("entrou arquivo não previsto: " + ", ".join(sorted(sobrando)))
    return publicados, imagens


if __name__ == "__main__":
    publicados, imagens = monta()
    peso = sum(os.path.getsize(os.path.join(SAIDA, f)) for f in publicados)
    dominio = "com domínio próprio" if "CNAME" in publicados else "sem CNAME (endereço do github.io)"
    print(f"_site/ pronto: {len(publicados)} arquivos ({len(imagens)} imagens), {peso/1024/1024:.1f} MB, {dominio}")
    for f in sorted(publicados):
        print("  " + f)
