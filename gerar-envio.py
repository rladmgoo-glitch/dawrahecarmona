#!/usr/bin/env python3
"""Gera as versões "para enviar" (WhatsApp / e-mail) do material da Dawrah, Carmona & Associados.

    python3 gerar-envio.py             tudo
    python3 gerar-envio.py folder-a3   só os folders impressos
    python3 gerar-envio.py manual      só o manual da marca (usa os PDFs dos folders)

Saída em envio/:
  Dawrah-Carmona-site.html         o site num arquivo só: fotos embutidas como data: URI e os
                                   Termos de Uso dentro do rodapé (<details>), sem depender de img/
                                   nem de termos.html. Abre direto no celular.
  Dawrah-Carmona-apresentacao.pdf  folder.html impresso em A4 pelo Chrome headless (a versão digital).
  Dawrah-Carmona-folder-*A3-*.pdf  os folders impressos (folder-a3.html, institucional; folder-solucoes-a3.html,
                                   PPS/PEC/Michel): "espelhos" (aberto, A3 deitado, para aprovar) e "grafica"
                                   (8 páginas A4 soltas com 3 mm de sangria).
  Dawrah-Carmona-manual-da-marca.pdf  manual-da-marca.html (A4); as miniaturas vão para img/manual/.
  Dawrah-Carmona-artifact.html     o mesmo site no formato de Artifact do claude.ai (link compartilhável):
                                   sem <html>/<head> próprios, cabeçalho respeitando a área segura do
                                   celular e sem o formulário de e-mail (mailto não é confiável dentro do
                                   Artifact; e-mail, WhatsApp e Instagram seguem visíveis).

O site publicável continua sendo a pasta (index.html + termos.html + img/); este script não a altera.
"""
import base64
import html
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "envio")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def data_uri(nome):
    """JPEG re-encodado mais leve, para o arquivo único caber bem num anexo."""
    im = Image.open(os.path.join(AQUI, "img", nome)).convert("RGB")
    if im.width > 1300:
        im = im.resize((1300, round(im.height * 1300 / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=74, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def termos_embutidos():
    s = open(os.path.join(AQUI, "termos.html"), encoding="utf-8").read()
    intro = re.search(r'<p class="intro">(.*?)</p>', s, re.S).group(1)
    partes = [f"<p>{intro}</p>"]
    for n, corpo in re.findall(r'<section><span class="n">(\d+)</span><div>(.*?)</div></section>', s, re.S):
        titulo = re.search(r"<h2>(.*?)</h2>", corpo).group(1)
        paras = re.findall(r"<p>(.*?)</p>", corpo, re.S)
        partes.append(f"<h5>{n}. {titulo}</h5>" + "".join(f"<p>{p.strip()}</p>" for p in paras))
    data = re.search(r"Última atualização: ([^<]+)", s).group(1)
    return (
        '<details class="terms" id="termos"><summary>Termos de Uso</summary>'
        f'<div class="tx"><p class="upd">Última atualização: {html.escape(data, quote=False)}</p>'
        + "".join(partes)
        + "</div></details>"
    )


CSS_TERMOS = """
footer .terms{margin-top:22px;border-top:1px solid var(--navy-line);padding-top:16px}
footer .terms summary{cursor:pointer;list-style:none;font:600 10.5px/1.3 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--brass)}
footer .terms summary::-webkit-details-marker{display:none}
footer .terms summary::after{content:"  +"}
footer .terms[open] summary::after{content:"  –"}
footer .terms .tx{max-width:760px;margin-top:14px;font-size:13px;line-height:1.65;color:rgba(244,242,236,.72)}
footer .terms .tx .upd{color:rgba(244,242,236,.5)}
footer .terms .tx h5{margin:18px 0 6px;font:400 16px/1.3 var(--serif);color:var(--bone)}
footer .terms .tx p+p{margin-top:8px}
footer .terms .tx a{color:var(--bone)}
"""


def gerar_site():
    s = open(os.path.join(AQUI, "index.html"), encoding="utf-8").read()
    for nome in sorted(set(re.findall(r'img/([\w.-]+\.jpg)', s))):
        uri = data_uri(nome)
        s = s.replace(f'src="img/{nome}"', f'src="{uri}"').replace(f"url(img/{nome})", f"url({uri})")
    assert "img/" not in s, "sobrou referência a img/"
    link = '<a href="termos.html">Termos de Uso</a>'
    assert s.count(link) == 1
    s = s.replace(link, '<a href="#termos">Termos de Uso</a>')
    base = re.search(r'(<div class="foot-base">.*?</div>)', s).group(1)
    s = s.replace(base, base + "\n    " + termos_embutidos(), 1)
    s = s.replace("</style>", CSS_TERMOS + "</style>", 1)
    s = s.replace(
        "</body>",
        "<script>document.querySelector('a[href=\"#termos\"]').addEventListener('click',function(){"
        "document.getElementById('termos').open=true;});</script>\n</body>",
        1,
    )
    destino = os.path.join(SAIDA, "Dawrah-Carmona-site.html")
    open(destino, "w", encoding="utf-8").write(s)
    return destino, s


CSS_ARTIFACT = """
.top{top:env(safe-area-inset-top,0px)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:30;background:var(--navy)}
.hero{min-height:min(calc(100svh - 68px),720px)}
"""


def gerar_artifact(site):
    """Publicar com a ferramenta Artifact (mesmo caminho a cada atualização, para manter o link)."""
    estilo = re.search(r"<style>.*?</style>", site, re.S).group(0).replace("</style>", CSS_ARTIFACT + "</style>")
    corpo = re.search(r"<body>(.*)</body>", site, re.S).group(1)
    corpo = re.sub(r'\s*<form class="msg".*?</form>', "", corpo, count=1, flags=re.S)
    assert "<form" not in corpo
    s = "<title>Dawrah, Carmona &amp; Associados</title>\n" + estilo + "\n" + corpo.strip() + "\n"
    destino = os.path.join(SAIDA, "Dawrah-Carmona-artifact.html")
    open(destino, "w", encoding="utf-8").write(s)
    return destino


def gerar_pdf(origem="folder.html", nome="Dawrah-Carmona-apresentacao.pdf"):
    """O Chrome headless deste Mac não encerra sozinho depois do --print-to-pdf:
    espera o arquivo parar de crescer e encerra o processo."""
    destino = os.path.join(SAIDA, nome)
    if os.path.exists(destino):
        os.remove(destino)
    perfil = tempfile.mkdtemp()
    proc = subprocess.Popen(
        [CHROME, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={perfil}",
         "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={destino}",
         "file://" + os.path.join(AQUI, origem)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    ultimo, estavel = -1, 0
    for _ in range(120):
        time.sleep(0.5)
        if proc.poll() is not None:
            break
        if os.path.exists(destino):
            tam = os.path.getsize(destino)
            estavel = estavel + 1 if tam == ultimo and tam > 0 else 0
            ultimo = tam
            if estavel >= 4:
                break
    proc.kill()
    proc.wait()
    shutil.rmtree(perfil, ignore_errors=True)
    if not os.path.exists(destino) or os.path.getsize(destino) == 0:
        raise SystemExit("o Chrome não gerou o PDF")
    return destino


FOLDERS_A3 = {"folder-a3.html": "Dawrah-Carmona-folder-A3",                    # institucional
              "folder-solucoes-a3.html": "Dawrah-Carmona-folder-solucoes-A3"}     # PPS, PEC e Michel


def gerar_folder_a3():
    """Os folders impressos (8 páginas em 2 folhas A3 cada).
    Espelhos = o folder aberto, para aprovar; gráfica = as 8 páginas A4 soltas com 3 mm de sangria."""
    feitos = []
    for origem, nome in FOLDERS_A3.items():
        feitos += [gerar_pdf(origem, f"{nome}-espelhos.pdf"), gerar_pdf(origem + "#grafica", f"{nome}-grafica.pdf")]
    return feitos


def captura(url, destino, largura, altura):
    """Print de tela pelo Chrome headless (o mesmo truque do PDF: encerra quando o arquivo aparece)."""
    perfil = tempfile.mkdtemp()
    if os.path.exists(destino):
        os.remove(destino)
    proc = subprocess.Popen(
        [CHROME, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={perfil}", "--hide-scrollbars",
         f"--window-size={largura},{altura}", "--virtual-time-budget=3000", f"--screenshot={destino}", url],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(60):
        time.sleep(0.5)
        if proc.poll() is not None or (os.path.exists(destino) and os.path.getsize(destino) > 0):
            time.sleep(0.5)
            break
    proc.kill()
    proc.wait()
    shutil.rmtree(perfil, ignore_errors=True)


def miniaturas():
    """As imagens de aplicação do manual (img/manual/): páginas dos folders e o topo do site."""
    destino = os.path.join(AQUI, "img", "manual")
    os.makedirs(destino, exist_ok=True)
    tmp = tempfile.mkdtemp()

    def pagina(pdf, n):
        base = os.path.join(tmp, f"{pdf}-{n}")
        subprocess.run(["pdftocairo", "-png", "-r", "80", "-f", str(n), "-l", str(n), "-singlefile",
                        os.path.join(SAIDA, pdf), base], check=True)
        return Image.open(base + ".png").convert("RGB")

    capa = pagina("Dawrah-Carmona-folder-A3-espelhos.pdf", 1)
    capa = capa.crop((capa.width // 2, 0, capa.width, capa.height))
    site = os.path.join(tmp, "site.png")
    captura("file://" + os.path.join(AQUI, "index.html"), site, 1280, 800)
    for nome, im in (("folder-capa", capa),
                     ("folder-camadas", pagina("Dawrah-Carmona-folder-A3-espelhos.pdf", 2)),
                     ("solucoes", pagina("Dawrah-Carmona-folder-solucoes-A3-espelhos.pdf", 2)),
                     ("site", Image.open(site).convert("RGB"))):
        if im.width > 1100:
            im = im.resize((1100, round(im.height * 1100 / im.width)), Image.LANCZOS)
        im.save(os.path.join(destino, nome + ".jpg"), "JPEG", quality=82, optimize=True, progressive=True)
    shutil.rmtree(tmp, ignore_errors=True)


def gerar_manual():
    """Manual da marca (A4). As miniaturas saem dos PDFs dos folders, então vêm depois deles."""
    miniaturas()
    return gerar_pdf("manual-da-marca.html", "Dawrah-Carmona-manual-da-marca.pdf")


if __name__ == "__main__":
    os.makedirs(SAIDA, exist_ok=True)
    if sys.argv[1:] == ["folder-a3"]:
        feitos = gerar_folder_a3()
    elif sys.argv[1:] == ["manual"]:
        feitos = [gerar_manual()]
    else:
        site, html_site = gerar_site()
        feitos = [site, gerar_artifact(html_site), gerar_pdf()] + gerar_folder_a3() + [gerar_manual()]
    for f in feitos:
        print(f"{os.path.relpath(f, AQUI)}  {os.path.getsize(f) / 1024:.0f} KB")
