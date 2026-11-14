# Dawrah, Carmona & Associados — site, apresentação, folders e manual da marca

Material do **escritório** (não da AEVUM). Começou em 2026-10-26 a pedido dos sócios; revisão grande em 2026-10-31
(logo oficial em The Seasons, folders impressos A3 e manual da marca).

Repositório próprio desde 2026-11-10. Antes ficava em `marca/dawrahecarmona/` do repositório `aevum`, e o histórico veio junto.

**O site está no ar em https://dawrahecarmona.com.br desde 2026-11-13**, publicado pelo GitHub Pages a cada push na `main`. Ver [No ar](#no-ar).

| Arquivo | O que é |
|---|---|
| `index.html` | Home de `dawrahecarmona.com.br`: o escritório, os sócios e os cartões das três soluções. Publicável como está, junto com as páginas abaixo, `site-base.css`, `site.js`, `termos.html` e `img/`. |
| `360/` · `workshop/` · `aevum/` | Uma pasta por solução, cada uma com o seu `index.html`, para o endereço ficar `dawrahecarmona.com.br/workshop` sem extensão. Cada página abre com a trilha de volta para a home, fecha com a chamada para contato e lista as outras duas. O Workshop traz as duas vertentes, `#vendas` e `#empreendedorismo`, e segue a identidade do próprio produto — preto e dourado, Playfair Display e DM Sans, vindas de `DcaWorkshopApplication`; as fontes estão embutidas, reduzidas aos caracteres da página. **O texto do Workshop é o do site do produto, palavra por palavra: não acrescente formato, capacidade ou condição que não esteja lá.** |
| `conferir.py` | A cerca: logo presente, links e âncoras que resolvem, imagens que existem, cabeçalho e rodapé iguais, CSS sem uso. Rode antes de publicar ou de gerar o envio. |
| `site-base.css` | O que as quatro páginas têm em comum (as de pasta chamam `../site-base.css`): a fonte, as cores, tipografia, botões, cabeçalho, rodapé, os cartões da home (`.sols` / `.sol-card`) e os blocos reaproveitados (`.stats`, `.front`, `.fmt`, `.pillars`). O que é de uma página só fica no `<style>` dela. |
| `site.js` | O menu do celular, o ano do rodapé e o formulário da home. |
| `termos.html` | Termos de Uso, adaptados do texto da De Paula & Carmona. |
| `folder.html` | Apresentação A4, 10 páginas. Fonte do PDF (a versão digital). |
| `folder-a3.html` | Folder institucional impresso: 8 páginas A4 em 2 folhas A3 dobradas. Abre como o folder aberto; com `#grafica` no endereço, mostra as páginas soltas com sangria. |
| `folder-solucoes-a3.html` | Folder de soluções impresso, no mesmo formato: PPS, PEC e o trabalho do Michel como executivo e consultor. |
| `folder-a3-base.css` · `folder-a3-base.js` | A base comum dos dois folders: fonte, cores, espelhos e sangria, capa, contracapa, rede de pontos e o modo `#grafica`. |
| `manual-da-marca.html` | Manual da marca (A4, 6 páginas): logo, uso, cores, tipografia, elementos e aplicações. |
| `logo/` | **Logo oficial** (ver abaixo): SVG e PNG prontos, o contorno-mestre e o script que injeta o logo nos HTML. |
| `fontes/` | **Todo o material recebido do escritório**, guardado como chegou (PDFs do Canva, prints, logo oficial). Ver abaixo. |
| `img/` | Fotos: sócios (`michel.jpg`, `elton.jpg`), escritório, prédio, caneta, família, dossiê AEVUM. `img/workshop/` = os recortes da equipe do workshop, em WebP com fundo transparente, vindos do app (`DcaWorkshopApplication/frontend/src/assets/images`). `img/manual/` = miniaturas do manual (geradas). |
| `gerar-envio.py` | Gera as versões para enviar, em `envio/`. |
| `montar-site.py` | Monta em `_site/` exatamente o que vai ao ar: as cinco páginas, o CSS, o JS e só as imagens que elas pedem. Para na hora se aparecer arquivo não previsto — é o que mantém os folders, o manual, `fontes/` e `envio/` fora do site. `_site/` não é versionado. |
| `.github/workflows/pages.yml` | Publica: a cada push na `main` roda `conferir.py`, depois `montar-site.py`, e sobe `_site/` para o Pages. Só dispara nos caminhos listados nele — **uma página nova precisa entrar nessa lista**. |
| `CNAME` | O domínio, `dawrahecarmona.com.br`. Está no repositório porque `montar-site.py` o copia para `_site/`, mas quem configura o domínio é a API do Pages (ver abaixo). |

## Para enviar

```
python3 gerar-envio.py             # tudo
python3 gerar-envio.py folder-a3   # só os folders impressos
python3 gerar-envio.py manual      # só o manual (usa os PDFs dos folders)
```

- `envio/Dawrah-Carmona-apresentacao.pdf`: o PDF da apresentação. Segue como a opção digital.
- `envio/Dawrah-Carmona-folder-A3-espelhos.pdf` e `envio/Dawrah-Carmona-folder-solucoes-A3-espelhos.pdf`:
  - os folders impressos abertos, em 4 páginas A3 deitadas;
  - para aprovar.
- `envio/…-grafica.pdf`: o arquivo para a gráfica.
  - Traz as 8 páginas A4 em ordem de leitura, com 3 mm de sangria.
- `envio/Dawrah-Carmona-manual-da-marca.pdf`: o manual da marca.
- `envio/Dawrah-Carmona-site.html`: o site num arquivo só, para WhatsApp ou e-mail. Fotos e Termos vão dentro do arquivo.
- `envio/Dawrah-Carmona-artifact.html`: o site como link compartilhável, no Artifact https://claude.ai/artifact/K9ogxYsbUeipspKEXdhr7q.
  - Para atualizar o link, republique a partir deste mesmo arquivo.
  - O link é privado: quem libera o acesso é o dono, pelo menu Share.

Prévia local: `.claude/launch.json` → `site-dawrahecarmona`, este repositório na porta 8093.

**Toda vez que uma página for regerada, reinjete o logo e rode `python3 conferir.py`** — o bloco `<!--assinatura-->` se perde na regeração e a página fica sem o logo, sem erro nenhum.

## No ar

O site é publicado pelo **GitHub Pages** a partir da `main` deste repositório. Todo push na `main` que toque um dos
caminhos listados em `.github/workflows/pages.yml` roda `conferir.py`, monta `_site/` com `montar-site.py` e põe no
ar. Não há passo manual nem build local para commitar.

Vai ao ar **só** o que `montar-site.py` copia: as cinco páginas, o CSS, o JS e as imagens que elas pedem. Os folders
impressos, o manual da marca, `fontes/` e `envio/` ficam no repositório e não são publicados — se mexer no script,
confirme que continuam dando 404 no domínio. O repositório é público: os PDFs de `fontes/` não aparecem no site,
mas são visíveis no GitHub para quem tiver o endereço do repositório (o dono foi avisado em 13/11 e seguiu assim).

### Duas armadilhas do Pages

- **O arquivo `CNAME` não configura o domínio** quando a publicação é por Actions (`build_type=workflow`); isso só
  vale no modo antigo do Pages. O domínio se registra pela API:

  ```bash
  gh api -X PUT repos/rladmgoo-glitch/dawrahecarmona/pages -f cname=dawrahecarmona.com.br
  ```

  ```bash
  gh api -X PUT repos/rladmgoo-glitch/dawrahecarmona/pages -F https_enforced=true
  ```

  O booleano vai com `-F`; com `-f` o GitHub recusa com 422. O certificado sai alguns minutos depois.
- **O `CNAME` precisa estar na lista de `paths` do workflow.** Sem isso, ligar ou desligar o domínio não republica
  nada e parece que o site não reage.

### DNS e e-mail — o que não se toca

O DNS continua na **Locaweb**. Mudaram só:

- os quatro registros `A` do ápice, para `185.199.108.153`, `185.199.109.153`, `185.199.110.153` e `185.199.111.153`;
- o `www`, apontando para o ápice.

**Não mexer em `MX`, no TXT do SPF, nem em `webmail`, `pop`, `smtp`, `imap`, `mail` e `autodiscover`** — é por eles
que o e-mail do escritório funciona. O Pages não tem nada a ver com e-mail: responde só pelo site.

## Logo oficial (`logo/`)

O logo do escritório é o de `fontes/logo-oficial-dawrah-carmona.png`:
- “Dawrah, Carmona & Associados” em **The Seasons Bold**;
- embaixo, “Consultoria Empresarial” em **Antic Didone**;
- tudo em uma cor só.

A The Seasons é comercial e não está instalada. Por isso guardamos o **contorno** dos glifos (`logo/contornos.svg`), tirado da capa do PDF do Canva. Esse contorno é o desenho exato do logo, e nada depende da fonte.

| Comando | O que faz |
|---|---|
| `python3 logo/assinatura.py arquivos` | Gera os arquivos prontos: `dawrah-carmona-logo-{navy,branco}` (logo oficial) e `dawrah-carmona-nome-{navy,branco}` (só o nome), em `.svg` e `.png` de 3000 px, com fundo transparente. |
| `python3 logo/assinatura.py injetar A.html …` | Põe o logo dentro do HTML como símbolos SVG (`#dc-logo`, `#dc-nome`, `#dc-2l`, `#dc-2c`, `#dc-l1`, `#dc-l2`, `#dc-sub`). Entram só os que o arquivo usa. |
| `python3 logo/assinatura.py extrair` | Refaz o `contornos.svg` a partir do Canva. Só se o logo mudar. |

Para usar o logo num HTML:
- O arquivo precisa de um bloco `<!--assinatura--><!--/assinatura-->`.
- As cinco páginas do site recebem o logo pelo mesmo comando:
  `python3 logo/assinatura.py injetar index.html 360/index.html workshop/index.html aevum/index.html`.
- O uso é `<svg class="dc-nome"><use href="#dc-nome"/></svg>`.
- A cor vem do CSS (`color`), e a altura também.
- Referência de tamanho: 60 unidades do símbolo = 50 pt de The Seasons.

Arquivos que já usam o logo:
- `index.html`, `termos.html` e `folder.html`;
- os dois folders A3 e o manual;
- no repositório `aevum`, `marca/aevumlegacy-site.html` e `marca/og.html`.

Se o logo mudar, rode `injetar` em todos esses arquivos e gere os envios de novo.

## Material recebido (`fontes/`)

Regra do dono (31/10): **guardar sempre todo o material que o escritório manda**, com data no nome, mesmo o que já foi aproveitado.

| Arquivo | O que é |
|---|---|
| `2026-10-31-canva-consultoria-360-slides.pdf` | Slides do Canva “Consultoria 360º”. São o padrão visual e a origem do contorno do logo. |
| `2026-10-31-apresentacao-digital-revisada.pdf` | A apresentação digital, como voltou da revisão. |
| `2026-10-31-whatsapp-michel-revisao-folder.png` | O print do pedido do Michel para as páginas 2 e 3 do folder: só as bios, e o degradê da foto até o branco. |
| `2026-10-31-PEC-planejamento-estrategico-comercial.pdf` · `…-PPS-planejamento-patrimonial-sucessorio.pdf` | As lâminas do Canva das duas soluções. São a base do folder de soluções. |
| `2026-10-31-michel-apresentacao-profissional.pdf` | “Apresentação Profissional — Executivo e Consultor”, do Michel. Tem os números, a formação, o livro e a atuação. |
| `logo-oficial-dawrah-carmona.png` | O logo oficial, copiado de `design/clients/carmona-dawrah/04-design/brand/` (repositório `aevum`). |

## Decisões

- **Paleta:**
  - navy `#041e42` (Pantone 282 C), bone e latão `#c2a26a`;
  - **sem verde**, nem no escritório nem na AEVUM.
- **Logo:**
  - sempre o desenho oficial, em uma cor só;
  - o “&” não muda de cor;
  - o nome nunca é redigitado em outra fonte.
- **Site da AEVUM (`marca/aevumlegacy-site.html`, no repositório `aevum`):**
  - o conteúdo está aprovado; ali só mudam a cor e a fonte;
  - em 31/10 o verde virou latão e o nome do escritório passou para o logo.
- **Cartões das soluções (home), 14/11:** cada um é um cartão de verdade — borda, sombra, 22 px de respiro entre
  eles e uma barra de 3 px no topo na cor do produto (navy no 360º, dourado no Workshop, latão na AEVUM). Antes eram
  papel quase branco sobre bone, separados por um fio de 1 px, e se confundiam com o fundo. O Workshop vem em preto
  e dourado, a identidade do próprio produto.
  - As classes são `.sols` e `.sol-card`. **Não usar `.card` / `.cards`:** a página do Workshop usa esses nomes
    dentro de `.wk-dark` e as regras do `site-base.css` vazam para lá.
- **Rodapé e Termos:** CNPJ do escritório, 55.927.541/0001-51, com a razão social Dawrah Carmona e Associados Ltda.
- **Bios dos sócios:** texto enviado pelo escritório.
  - Michel: Sócio, administrador com MBA em Marketing (FGV). Números da trajetória e livro “Sr. Hochade” tirados da apresentação dele (31/10).
  - Elton: Diretor Jurídico, advogado.
- **"Colecionador de relógios vintage" (Elton):** está só nos PDFs, não no site.
- **Apresentação:** texto curto, e a estrutura fica nos diagramas. Os diagramas são:
  - o anel do 360º;
  - as cinco frentes;
  - o quadro "sem planejamento / com planejamento";
  - os passos do planejamento comercial (no folder de soluções, uma escada);
  - os formatos do Programa de Empreendedorismo.
- **Folder institucional (A3), revisão de 31/10:**
  - Estrutura:
    - 1: capa.
    - 2|3: três camadas.
      - 1ª: o escritório e os passos 01·02·03.
      - 2ª: Elton, com a foto à esquerda; o degradê sai da foto em azul e chega ao branco ainda no meio, e a bio fica no lado branco.
      - 3ª: Michel, a mesma coisa espelhada.
      - Só as bios: AEVUM e treinamento ficam nas páginas 4 e 5 (pedido do Michel, 31/10).
    - 4|5: AEVUM e Empreendedorismo. A frase “Transforme sua equipe em força de vendas.” está na faixa de contato da página 5.
    - 6|7: Consultoria 360º.
    - 8: contato.
  - Capa: a mesma imagem aprovada no PDF digital (foto do escritório sob o degradê azul `#041e42`), sem a frase, com o nome em The Seasons a 50 pt. Dentro do folder segue o padrão dos slides do Canva (“Consultoria 360º”): degradês e rede de pontos.
  - A foto da capa tem 1300 px e fica com ~72 ppi impressa. Ela fica quase toda coberta pelo azul, mas um original maior deixaria a impressão mais limpa.
  - Fotos dos sócios: 556 px de largura, ~165 ppi no tamanho impresso. Para a gráfica, o ideal são os originais em maior resolução.
- **Folder de soluções (A3), 31/10:**
  - Mesma capa, contracapa e base.
  - 2|3: PPS. Foto da família, o quadro “sem × com planejamento” e o **Elton** como quem conduz (é a área dele).
    Assim cada sócio aparece junto das soluções dele: o Elton no PPS e o Michel no comercial e no treinamento.
  - 4|5: PEC. Foto do prédio e a escada das sete etapas.
  - 6|7: Michel, executivo e consultor: os números, a formação, o livro, a atuação nacional e a evolução de negócios, os formatos in-company.
  - O conteúdo saiu dos anexos de 31/10 (`fontes/`). Não usamos a imagem com marca d’água Freepik da lâmina do PEC.
- **Domínio:** resolvido em 13/11 — o site foi para o GitHub Pages e o e-mail ficou onde estava, na Locaweb. Ver [No ar](#no-ar).
