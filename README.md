# Dawrah, Carmona & Associados — site, apresentação, folders e manual da marca

Material do **escritório** (não da AEVUM). Começou em 2026-10-26 a pedido dos sócios; revisão grande em 2026-10-31
(logo oficial em The Seasons, folders impressos A3 e manual da marca).

| Arquivo | O que é |
|---|---|
| `index.html` | Novo site de `dawrahecarmona.com.br`. Publicável como está, junto com `termos.html` e `img/`. |
| `termos.html` | Termos de Uso, adaptados do texto da De Paula & Carmona. |
| `folder.html` | Apresentação A4, 10 páginas. Fonte do PDF (a versão digital). |
| `folder-a3.html` | Folder institucional impresso: 8 páginas A4 em 2 folhas A3 dobradas. Abre como o folder aberto; com `#grafica` no endereço, mostra as páginas soltas com sangria. |
| `folder-solucoes-a3.html` | Folder de soluções impresso, no mesmo formato: PPS, PEC e o trabalho do Michel como executivo e consultor. |
| `folder-a3-base.css` · `folder-a3-base.js` | A base comum dos dois folders: fonte, cores, espelhos e sangria, capa, contracapa, rede de pontos e o modo `#grafica`. |
| `manual-da-marca.html` | Manual da marca (A4, 6 páginas): logo, uso, cores, tipografia, elementos e aplicações. |
| `logo/` | **Logo oficial** (ver abaixo): SVG e PNG prontos, o contorno-mestre e o script que injeta o logo nos HTML. |
| `fontes/` | **Todo o material recebido do escritório**, guardado como chegou (PDFs do Canva, prints, logo oficial). Ver abaixo. |
| `img/` | Fotos: sócios (`michel.jpg`, `elton.jpg`), escritório, prédio, caneta, família, dossiê AEVUM. `img/manual/` = miniaturas do manual (geradas). |
| `gerar-envio.py` | Gera as versões para enviar, em `envio/`. |

## Para enviar

```
python3 marca/dawrahecarmona/gerar-envio.py             # tudo
python3 marca/dawrahecarmona/gerar-envio.py folder-a3   # só os folders impressos
python3 marca/dawrahecarmona/gerar-envio.py manual      # só o manual (usa os PDFs dos folders)
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

Prévia local (`.claude/launch.json`):
- `site-dawrahecarmona`: esta pasta, na porta 8093.
- `marca`: a pasta `marca/` inteira, na porta 8094.

## Logo oficial (`logo/`)

O logo do escritório é o de `fontes/logo-oficial-dawrah-carmona.png`:
- “Dawrah, Carmona & Associados” em **The Seasons Bold**;
- embaixo, “Consultoria Empresarial” em **Antic Didone**;
- tudo em uma cor só.

A The Seasons é comercial e não está instalada. Por isso guardamos o **contorno** dos glifos (`logo/contornos.svg`), tirado da capa do PDF do Canva. Esse contorno é o desenho exato do logo, e nada depende da fonte.

| Comando | O que faz |
|---|---|
| `python3 marca/dawrahecarmona/logo/assinatura.py arquivos` | Gera os arquivos prontos: `dawrah-carmona-logo-{navy,branco}` (logo oficial) e `dawrah-carmona-nome-{navy,branco}` (só o nome), em `.svg` e `.png` de 3000 px, com fundo transparente. |
| `python3 marca/dawrahecarmona/logo/assinatura.py injetar A.html …` | Põe o logo dentro do HTML como símbolos SVG (`#dc-logo`, `#dc-nome`, `#dc-2l`, `#dc-2c`, `#dc-l1`, `#dc-l2`, `#dc-sub`). Entram só os que o arquivo usa. |
| `python3 marca/dawrahecarmona/logo/assinatura.py extrair` | Refaz o `contornos.svg` a partir do Canva. Só se o logo mudar. |

Para usar o logo num HTML:
- O arquivo precisa de um bloco `<!--assinatura--><!--/assinatura-->`.
- O uso é `<svg class="dc-nome"><use href="#dc-nome"/></svg>`.
- A cor vem do CSS (`color`), e a altura também.
- Referência de tamanho: 60 unidades do símbolo = 50 pt de The Seasons.

Arquivos que já usam o logo:
- `index.html`, `termos.html` e `folder.html`;
- os dois folders A3 e o manual;
- fora desta pasta, `../aevumlegacy-site.html` e `../og.html`.

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
| `logo-oficial-dawrah-carmona.png` | O logo oficial, copiado de `design/clients/carmona-dawrah/04-design/brand/`. |

## Decisões

- **Paleta:**
  - navy `#041e42` (Pantone 282 C), bone e latão `#c2a26a`;
  - **sem verde**, nem no escritório nem na AEVUM.
- **Logo:**
  - sempre o desenho oficial, em uma cor só;
  - o “&” não muda de cor;
  - o nome nunca é redigitado em outra fonte.
- **Site da AEVUM (`../aevumlegacy-site.html`):**
  - o conteúdo está aprovado; ali só mudam a cor e a fonte;
  - em 31/10 o verde virou latão e o nome do escritório passou para o logo.
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
  - 2|3: PPS. Foto da família e o quadro “sem × com planejamento”.
  - 4|5: PEC. Foto do prédio e a escada das sete etapas.
  - 6|7: Michel, executivo e consultor: os números, a formação, o livro, a atuação nacional e a evolução de negócios, os formatos in-company.
  - O conteúdo saiu dos anexos de 31/10 (`fontes/`). Não usamos a imagem com marca d’água Freepik da lâmina do PEC.
- **Pendente:** o site ainda não está no domínio. O DNS e, provavelmente, o e-mail `contato@` estão na Locaweb; não mexer sem combinar.
