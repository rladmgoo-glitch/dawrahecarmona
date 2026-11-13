#!/usr/bin/env python3
"""Gera as versões "para enviar" (WhatsApp / e-mail) do material da Dawrah, Carmona & Associados.

    python3 gerar-envio.py             tudo
    python3 gerar-envio.py folder-a3   só os folders impressos
    python3 gerar-envio.py manual      só o manual da marca (usa os PDFs dos folders)

Saída em envio/:
  Dawrah-Carmona-site.html         o site num arquivo só, e ainda navegando por páginas: a home e
                                   as três soluções continuam páginas separadas, e o menu e os cartões
                                   trocam de uma para outra em vez de rolar tudo num scroll só. Fotos
                                   embutidas como data: URI e os Termos de Uso dentro do rodapé
                                   (<details>). Não depende de site-base.css, site.js, img/ nem
                                   termos.html; abre direto no celular, sem internet.
  Dawrah-Carmona-apresentacao.pdf  folder.html impresso em A4 pelo Chrome headless (a versão digital).
  Dawrah-Carmona-folder-*A3-*.pdf  os folders impressos (folder-a3.html, institucional; folder-solucoes-a3.html,
                                   PPS/PEC/Michel): "espelhos" (aberto, A3 deitado, para aprovar) e "grafica"
                                   (8 páginas A4 soltas com 3 mm de sangria).
  Dawrah-Carmona-manual-da-marca.pdf  manual-da-marca.html (A4); as miniaturas vão para img/manual/.
  Dawrah-Carmona-artifact.html     o mesmo site no formato de Artifact do claude.ai (link compartilhável):
                                   sem <html>/<head> próprios, cabeçalho respeitando a área segura do
                                   celular e sem o formulário de e-mail (mailto não é confiável dentro do
                                   Artifact; e-mail, WhatsApp e Instagram seguem visíveis).

O site publicável continua sendo a pasta (index.html, 360/, workshop/, aevum/, termos.html,
site-base.css, site.js e img/); este script não a altera.
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
    """A foto re-encodada mais leve, para o arquivo único caber bem num anexo.
    As fotos comuns viram JPEG; os recortes com fundo transparente (os retratos
    do workshop) seguem em WebP, que guarda o canal alfa."""
    im = Image.open(os.path.join(AQUI, "img", nome))
    alfa = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    buf = io.BytesIO()
    if alfa:
        im = im.convert("RGBA")
        if im.height > 1100:
            im = im.resize((round(im.width * 1100 / im.height), 1100), Image.LANCZOS)
        im.save(buf, "WEBP", quality=80, method=6)
        return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    im = im.convert("RGB")
    if im.width > 1300:
        im = im.resize((1300, round(im.height * 1300 / im.width)), Image.LANCZOS)
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


PAGINAS = [("360", "Consultoria Empresarial 360º"),
           ("workshop", "Workshop"),
           ("aevum", "AEVUM · Private Legacy Office")]
"""As soluções, cada uma na sua pasta, na ordem em que entram no arquivo único."""

CSS_PAGINAS = """
/* No arquivo único cada página do site continua sendo uma página: o menu e os
   cartões trocam de página em vez de rolar tudo num scroll só. */
.pagina{display:none}
.pagina.ativa{display:block}
"""

JS_PAGINAS = """
(function(){
  var paginas=document.querySelectorAll('.pagina');
  function mostra(id,ancora){
    var achou=false;
    paginas.forEach(function(p){
      var e=(p.id===id); p.classList.toggle('ativa',e); achou=achou||e;
    });
    if(!achou)return false;
    var alvo=ancora&&document.getElementById(ancora);
    if(alvo){alvo.scrollIntoView();}else{window.scrollTo(0,0);}
    return true;
  }
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href^="#pg-"]');
    if(!a)return;
    e.preventDefault();
    mostra(a.getAttribute('href').slice(1),a.getAttribute('data-ancora'));
    var nav=document.getElementById('nav');
    if(nav)nav.classList.remove('open');
  });
  if(location.hash.indexOf('#pg-')===0)mostra(location.hash.slice(1));
})();
"""


def miolo(pasta):
    """O <main> de uma página de solução, com a trilha e sem o rodapé de navegação."""
    s = open(os.path.join(AQUI, pasta, "index.html"), encoding="utf-8").read()
    m = re.search(r"<main([^>]*)>(.*?)</main>", s, re.S)
    atributos, corpo = m.group(1), m.group(2)
    corpo = re.sub(r'\s*<section class="outras">.*?</section>', "", corpo, count=1, flags=re.S)
    assert "outras-grid" not in corpo
    # a página pode trazer a própria identidade numa classe do <main> (o workshop traz)
    if atributos.strip():
        corpo = f"<div{atributos}>{corpo}\n</div>"
    trilha = re.search(r'<nav class="crumb".*?</nav>', s, re.S)
    estilo = re.search(r"<style>(.*?)</style>", s, re.S)
    return (trilha.group(0) if trilha else "") + "\n" + corpo, (estilo.group(1).strip() if estilo else "")


def so_ancoras(s):
    """Os links entre páginas viram #pg-<pasta>; o que vem depois do # vira data-ancora.
    Serve para o corpo das páginas, onde uma âncora solta (#proposta) é da própria página."""
    def troca(m):
        destino = (m.group(1) or "").replace("../", "").rstrip("/")
        if destino in ("", "index.html"):
            destino = "home"
        extra = ' data-ancora="%s"' % m.group(2) if m.group(2) else ""
        return 'href="#pg-%s"%s' % (destino, extra)

    return re.sub(r'href="((?:\.\./)?(?:360|workshop|aevum)/|\.\./|index\.html)(?:#([\w-]+))?"', troca, s)


def cabecalho_so_ancoras(s):
    """No cabeçalho (que vem da home) toda âncora é da home: #contato vira a home
    mais a âncora. #nav é do menu e #dc-… é o logo — esses ficam."""
    def troca(m):
        alvo = m.group(1)
        if alvo == "nav" or alvo.startswith("dc-"):
            return m.group(0)
        if alvo == "inicio":
            return 'href="#pg-home"'
        return 'href="#pg-home" data-ancora="%s"' % alvo

    return re.sub(r'href="#([\w-]+)"', troca, s)


def gerar_site():
    """O site inteiro num arquivo: a home e as páginas de solução continuam páginas,
    e o menu troca entre elas. As fotos entram como data: URI e os Termos de Uso
    vão para dentro do rodapé."""
    home = open(os.path.join(AQUI, "index.html"), encoding="utf-8").read()
    estilos = [open(os.path.join(AQUI, "site-base.css"), encoding="utf-8").read()]
    m = re.search(r"<style>(.*?)</style>", home, re.S)
    estilos.append(m.group(1).strip())
    home = home.replace(m.group(0), "", 1)

    cabeca = home[:home.index("<body>") + len("<body>")]
    assinatura = re.search(r"<!--assinatura-->.*?<!--/assinatura-->", home, re.S).group(0)
    cabecalho = cabecalho_so_ancoras(re.search(r'<header class="top">.*?</header>', home, re.S).group(0))
    rodape = re.search(r"<footer>.*?</footer>", home, re.S).group(0)
    corpo_home = re.search(r"<main>(.*?)</main>", home, re.S).group(1)

    partes = ['<div class="pagina ativa" id="pg-home">%s</div>' % corpo_home]
    for pasta, _ in PAGINAS:
        corpo, estilo = miolo(pasta)
        partes.append('<div class="pagina" id="pg-%s">\n%s\n</div>' % (pasta, corpo))
        if estilo:
            estilos.append(estilo)

    s = (cabeca + "\n" + assinatura + "\n\n" + cabecalho + "\n\n"
         + "\n\n".join(partes) + "\n\n" + rodape
         + '\n<script src="site.js"></script>\n</body></html>\n')
    s = s.replace('<link rel="stylesheet" href="site-base.css">',
                  "<style>\n" + "\n".join(estilos) + CSS_PAGINAS + "\n</style>")
    s = s.replace('<script src="site.js"></script>',
                  "<script>\n" + open(os.path.join(AQUI, "site.js"), encoding="utf-8").read().strip()
                  + "\n" + JS_PAGINAS.strip() + "\n</script>")
    s = so_ancoras(s)
    sobrou = re.findall(r'href="(?!#|mailto:|https?:|termos\.html)([^"]+)"', s)
    assert not sobrou, sobrou

    for nome in sorted(set(re.findall(r"img/([\w./-]+\.(?:jpg|png|webp))", s))):
        uri = data_uri(nome)
        s = s.replace(f'src="img/{nome}"', f'src="{uri}"').replace(f"url(img/{nome})", f"url({uri})")
        s = s.replace(f'src="../img/{nome}"', f'src="{uri}"').replace(f"url(../img/{nome})", f"url({uri})")
    assert "img/" not in s, "sobrou referência a img/"
    link = '<a href="termos.html">Termos de Uso</a>'
    assert s.count(link) == 1, s.count(link)
    s = s.replace(link, '<a href="#termos">Termos de Uso</a>')
    base = re.search(r'(<div class="foot-base">.*?</div>)', s).group(1)
    s = s.replace(base, base + "\n    " + termos_embutidos(), 1)
    s = s.replace("</style>", CSS_TERMOS + "</style>", 1)
    s = s.replace(
        "</body>",
        "<script>document.querySelector(\'a[href=\"#termos\"]\').addEventListener(\'click\',function(){"
        "document.getElementById(\'termos\').open=true;});</script>\n</body>",
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
