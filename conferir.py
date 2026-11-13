#!/usr/bin/env python3
"""Confere o site antes de publicar ou de gerar o envio.

    python3 conferir.py

Olha o que quebra em silêncio:
  - o logo: toda página usa <use href="#dc-*">, e o símbolo precisa estar dentro dela
    (o bloco <!--assinatura--> some a cada vez que a página é regerada à mão);
  - links e âncoras: todo href aponta para arquivo que existe e âncora que existe;
  - imagens: todo src existe em img/;
  - cabeçalho e rodapé: iguais em todas as páginas, fora o item marcado como atual;
  - CSS sem uso: regra no <style> da página cuja classe não aparece no HTML dela.

Sai com código 1 se achar problema, para dar para usar em gancho ou CI.
"""
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PAGINAS = ["index.html", "360/index.html", "workshop/index.html", "aevum/index.html"]


def resolve(pagina, alvo):
    """O caminho que um href/src de `pagina` aponta, visto da raiz do site.
    Uma pasta ("../workshop/", "360/") responde pelo index.html dela."""
    caminho = os.path.normpath(os.path.join(os.path.dirname(pagina), alvo))
    if caminho in (".", ""):
        caminho = "index.html"
    elif alvo.endswith("/") or os.path.isdir(os.path.join(AQUI, caminho)):
        caminho = os.path.join(caminho, "index.html")
    return caminho


def texto(p):
    return open(os.path.join(AQUI, p), encoding="utf-8").read()


def normaliza(s):
    """Para comparar cabeçalhos e rodapés: espaços, o item atual e o prefixo da home."""
    s = re.sub(r"\s+", " ", s)
    return s.replace(' aria-current="page"', "").replace("../", "").replace('href="#', 'href="')


def confere():
    erros = []
    ids = {p: set(re.findall(r'id="([\w-]+)"', texto(p))) for p in PAGINAS}

    for p in PAGINAS:
        h = texto(p)

        # 1. o logo
        for simbolo in set(re.findall(r'<use href="#(dc-[\w-]+)"', h)):
            if f'<symbol id="{simbolo}"' not in h:
                erros.append(f"{p}: usa #{simbolo} mas não tem o símbolo "
                             f"(rode: python3 logo/assinatura.py injetar {p})")

        # 2. links e âncoras
        for href in re.findall(r'href="([^"]+)"', h):
            if href.startswith(("http", "mailto:", "#dc-")) or href.endswith(".css"):
                continue
            arquivo, _, ancora = href.partition("#")
            arquivo = resolve(p, arquivo) if arquivo else p
            if not os.path.exists(os.path.join(AQUI, arquivo)):
                erros.append(f"{p}: href={href} — arquivo não existe")
            elif ancora and arquivo in ids and ancora not in ids[arquivo]:
                erros.append(f"{p}: href={href} — âncora não existe")

        # 3. imagens
        for src in re.findall(r'src="([^"]+)"', h):
            if src.startswith(("data:", "http")):
                continue
            if not os.path.exists(os.path.join(AQUI, resolve(p, src))):
                erros.append(f"{p}: src={src} — não existe")

        # 4. CSS da página sem uso na página
        estilo = re.search(r"<style>(.*?)</style>", h, re.S)
        if estilo:
            usadas = {c for g in re.findall(r'class="([^"]+)"', h) for c in g.split()}
            for classe in sorted({s for s in re.findall(r"(?m)^\.([a-z][\w-]*)", estilo.group(1))}):
                if classe not in usadas:
                    erros.append(f"{p}: .{classe} está no <style> e não é usada")

    # 5. cabeçalho e rodapé iguais
    for nome, padrao in (("nav", r'<nav class="nav".*?</nav>'),
                         ("rodapé", r'<div class="foot-grid">.*?</div>\s*</div>')):
        vistos = {}
        for p in PAGINAS:
            m = re.search(padrao, texto(p), re.S)
            if not m:
                erros.append(f"{p}: não achei o {nome}")
                continue
            vistos.setdefault(normaliza(m.group(0)), []).append(p)
        if len(vistos) > 1:
            grupos = " | ".join(", ".join(v) for v in vistos.values())
            erros.append(f"{nome} diferente entre as páginas: {grupos}")

    return erros


if __name__ == "__main__":
    problemas = confere()
    for x in problemas:
        print(x)
    print(f"{len(PAGINAS)} páginas conferidas — " + (f"{len(problemas)} problema(s)" if problemas else "tudo certo"))
    sys.exit(1 if problemas else 0)
