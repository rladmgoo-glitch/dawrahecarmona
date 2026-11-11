#!/usr/bin/env python3
"""Assinatura oficial de Dawrah, Carmona & Associados: o nome em The Seasons Bold e
"Consultoria Empresarial" em Antic Didone, como no logo do escritório (fontes/logo-oficial-dawrah-carmona.png).

A fonte The Seasons é comercial e não está instalada. Por isso guardamos o CONTORNO dos glifos,
tirado da capa do PDF do Canva que o escritório mandou. Esse contorno é o desenho exato do logo.

    python3 logo/assinatura.py extrair     # Canva → contornos.svg (só se o logo mudar)
    python3 logo/assinatura.py arquivos    # SVG e PNG do logo nesta pasta
    python3 logo/assinatura.py injetar A.html B.html ...

"injetar" troca o bloco entre <!--assinatura--> e <!--/assinatura--> por um <svg> oculto com os símbolos
(#dc-logo = o logo oficial; #dc-nome = o nome numa linha; #dc-2l / #dc-2c = em duas linhas, à esquerda ou
centralizado; #dc-l1, #dc-l2 = cada linha solta; #dc-sub = "Consultoria Empresarial") e as proporções deles.
Para usar no HTML:

    <svg class="dc-nome" role="img" aria-label="Dawrah, Carmona &amp; Associados"><use href="#dc-nome"/></svg>

A cor vem do CSS (`color`); a altura também. 60 unidades de altura do símbolo = 50 pt de The Seasons,
então `height:59.6pt` dá o nome em 50 pt.
"""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
CANVA = os.path.join(AQUI, "..", "fontes", "2026-10-31-canva-consultoria-360-slides.pdf")
CONTORNOS = os.path.join(AQUI, "contornos.svg")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
NOME, SUB = "Dawrah, Carmona & Associados", "Consultoria Empresarial"
NAVY, BRANCO = "#041e42", "#ffffff"
ALTURA = {"nome": (0, 60), "sub": (8, 59)}     # faixa vertical fixa: as linhas alinham pela linha de base


def extrair():
    """Capa do Canva (pág. 1) → contornos.svg. Os glifos e as posições saem do SVG do pdftocairo."""
    tmp = tempfile.mkdtemp()
    svg = os.path.join(tmp, "capa.svg")
    subprocess.run(["pdftocairo", "-svg", "-f", "1", "-l", "1", CANVA, svg], check=True)
    s = open(svg, encoding="utf-8").read()
    shutil.rmtree(tmp)
    glifo = dict(re.findall(r'<g id="(glyph-\d+-\d+)">\s*(?:<path[^>]*d="([^"]*)")?', s))

    def corrida(fonte, texto):
        bloco = re.search(r'<g id="%s".*?</g>\s*</g>' % fonte, s, re.S).group(0)
        usos = re.findall(r'xlink:href="#(glyph-\d+-\d+)" x="([\d.]+)" y="([\d.]+)"', bloco)
        assert len(usos) == len(texto), (fonte, len(usos), len(texto))
        return [(c, float(x), float(y), (glifo.get(g) or "").strip()) for c, (g, x, y) in zip(texto, usos)]

    out = ['<svg xmlns="http://www.w3.org/2000/svg" data-origem="fontes/2026-10-31-canva-consultoria-360-slides.pdf, pág. 1">']
    for nome, fonte, texto in (("nome", "source-42", NOME), ("sub", "source-39", SUB)):
        out.append(f'<g id="{nome}" data-texto="{html.escape(texto)}">')
        for c, x, y, d in corrida(fonte, texto):
            out.append(f'<path data-c="{html.escape(c)}" data-x="{x:.3f}" data-y="{y:.3f}" d="{d}"/>')
        out.append("</g>")
    open(CONTORNOS, "w", encoding="utf-8").write("\n".join(out + ["</svg>"]) + "\n")
    print(os.path.relpath(CONTORNOS))


def glifos(grupo):
    s = open(CONTORNOS, encoding="utf-8").read()
    bloco = re.search(r'<g id="%s"[^>]*>(.*?)</g>' % grupo, s, re.S).group(1)
    return [(html.unescape(c), float(x), float(y), d) for c, x, y, d in
            re.findall(r'<path data-c="([^"]*)" data-x="([^"]*)" data-y="([^"]*)" d="([^"]*)"/>', bloco)]


def caixa(gs):
    xs = []
    for _, x, _, d in gs:
        n = [float(v) for v in re.findall(r"-?[\d.]+", d)]
        xs += [x + v for v in n[0::2]]
    return min(xs), max(xs)


def trecho(grupo, ini, fim):
    """Glifos de texto[ini:fim], sem espaços nas pontas, deslocados para começar em x = .5."""
    gs = [g for g in glifos(grupo)[ini:fim] if g[3]]
    x0, x1 = caixa(gs)
    paths = "".join(f'<path transform="translate({x - x0 + .5:.3f} {y:.3f})" d="{d}"/>' for _, x, y, d in gs)
    return paths, x1 - x0 + 1


PASSO = 55             # distância entre as linhas de base do nome em duas linhas (o corpo é 50,34 u)


def duas_linhas(l1, l2, centro):
    (p1, w1), (p2, w2) = l1, l2
    w = max(w1, w2)
    d1, d2 = ((w - w1) / 2, (w - w2) / 2) if centro else (0, 0)
    return (f'<g transform="translate({d1:.3f} 0)">{p1}</g><g transform="translate({d2:.3f} {PASSO})">{p2}</g>',
            w, ALTURA["nome"][0], ALTURA["nome"][1] + PASSO)


def pecas():
    i = NOME.index(" &")
    l1, l2 = trecho("nome", 0, i), trecho("nome", i + 1, len(NOME))
    return {
        "nome": trecho("nome", 0, len(NOME)) + ALTURA["nome"],
        "l1": l1 + ALTURA["nome"],
        "l2": l2 + ALTURA["nome"],
        "2l": duas_linhas(l1, l2, centro=False),
        "2c": duas_linhas(l1, l2, centro=True),
        "sub": trecho("sub", 0, len(SUB)) + ALTURA["sub"],
    }


def svg_solto(paths, w, y0, y1, cor):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {y0} {w:.3f} {y1 - y0}" width="{w:.3f}" '
            f'height="{y1 - y0}"><g fill="{cor}">{paths}</g></svg>\n')


SUB_EM = (174, 84)     # onde o Canva põe "Consultoria Empresarial" em relação ao nome (é o logo oficial)


def logo_paths():
    """O logo oficial: o nome numa linha e "Consultoria Empresarial" embaixo, nas posições exatas do Canva."""
    n = [g for g in glifos("nome") if g[3]]
    s = [(c, x + SUB_EM[0], y + SUB_EM[1], d) for c, x, y, d in glifos("sub") if d]
    x0 = caixa(n)[0]
    x1 = max(caixa(n)[1], caixa(s)[1])
    paths = "".join(f'<path transform="translate({x - x0 + .5:.3f} {y:.3f})" d="{d}"/>' for _, x, y, d in n + s)
    return paths, x1 - x0 + 1, 0, SUB_EM[1] + ALTURA["sub"][1]


def lockup(cor):
    paths, w, y0, y1 = logo_paths()
    return svg_solto(paths, w, y0, y1, cor)


def png(svg_arquivo, largura):
    """SVG → PNG transparente pelo Chrome headless (o mesmo Chrome que imprime os PDFs)."""
    s = open(svg_arquivo, encoding="utf-8").read()
    w, h = (float(v) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', s).groups())
    alt = round(largura * h / w)
    tmp = tempfile.mkdtemp()
    pag = os.path.join(tmp, "p.html")
    open(pag, "w").write(f'<html><body style="margin:0;background:transparent">'
                         f'<img src="file://{svg_arquivo}" style="display:block;width:{largura}px;height:{alt}px"></body></html>')
    destino = svg_arquivo[:-4] + ".png"
    proc = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={tmp}/perfil",
                             "--hide-scrollbars", "--default-background-color=00000000",
                             f"--window-size={largura},{alt}", f"--screenshot={destino}", "file://" + pag],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        time.sleep(.5)
        if proc.poll() is not None or (os.path.exists(destino) and os.path.getsize(destino) > 0):
            time.sleep(.5)
            break
    proc.kill()
    proc.wait()
    shutil.rmtree(tmp, ignore_errors=True)
    return destino


def arquivos():
    p = pecas()
    feitos = []
    for cor, sufixo in ((NAVY, "navy"), (BRANCO, "branco")):
        pn, wn, a0, a1 = p["nome"]
        for nome, conteudo in ((f"dawrah-carmona-nome-{sufixo}.svg", svg_solto(pn, wn, a0, a1, cor)),
                               (f"dawrah-carmona-logo-{sufixo}.svg", lockup(cor))):
            caminho = os.path.join(AQUI, nome)
            open(caminho, "w", encoding="utf-8").write(conteudo)
            feitos += [caminho, png(caminho, 3000)]
    for f in feitos:
        print(f"{os.path.relpath(f)}  {os.path.getsize(f) / 1024:.0f} KB")


def bloco(usados):
    p = dict(pecas(), logo=logo_paths())
    simbolos, regras = [], []
    for nome, (paths, w, y0, y1) in p.items():
        if nome not in usados:
            continue
        simbolos.append(f'<symbol id="dc-{nome}" viewBox="0 {y0} {w:.3f} {y1 - y0}"><g fill="currentColor">{paths}</g></symbol>')
        regras.append(f".dc-{nome}{{display:block;aspect-ratio:{w:.3f}/{y1 - y0};width:auto;overflow:visible}}")
    return ("<!--assinatura-->\n<!-- gerado por dawrahecarmona/logo/assinatura.py — não editar à mão -->\n"
            "<style>" + "".join(regras) + "</style>\n"
            '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(simbolos) + "</svg>\n"
            "<!--/assinatura-->")


def injetar(arquivos_html):
    """Só entram os símbolos que o arquivo usa (href="#dc-…"), para a página não carregar contorno à toa."""
    padrao = r"<!--assinatura-->.*?<!--/assinatura-->"
    for f in arquivos_html:
        s = open(f, encoding="utf-8").read()
        n = len(re.findall(padrao, s, re.S))
        if n != 1:
            raise SystemExit(f"{f}: precisa de exatamente um bloco <!--assinatura--><!--/assinatura--> (achei {n})")
        usados = set(re.findall(r'href="#dc-([a-z0-9]+)"', re.sub(padrao, "", s, flags=re.S)))
        s = re.sub(padrao, lambda m: bloco(usados), s, flags=re.S)
        open(f, "w", encoding="utf-8").write(s)
        print(f"{f}  ok  ({', '.join(sorted(usados))})")


if __name__ == "__main__":
    cmd, args = (sys.argv[1:2] or ["?"])[0], sys.argv[2:]
    if cmd == "extrair":
        extrair()
    elif cmd == "arquivos":
        arquivos()
    elif cmd == "injetar" and args:
        injetar(args)
    else:
        raise SystemExit(__doc__)
