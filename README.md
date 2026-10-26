# Dawrah, Carmona & Associados — site e apresentação

Material do **escritório** (não da AEVUM), feito em 2026-10-26 a pedido dos sócios.

| Arquivo | O que é |
|---|---|
| `index.html` | Novo site de `dawrahecarmona.com.br`. Publicável como está, junto com `termos.html` e `img/`. |
| `termos.html` | Termos de Uso, adaptados do texto da De Paula & Carmona. |
| `folder.html` | Apresentação A4, 10 páginas. Fonte do PDF. |
| `img/` | Fotos: sócios (`michel.jpg`, `elton.jpg`), escritório, prédio, caneta, família, dossiê AEVUM. |
| `gerar-envio.py` | Gera as versões para enviar, em `envio/`. |

## Para enviar

```
python3 marca/dawrahecarmona/gerar-envio.py
```

- `envio/Dawrah-Carmona-apresentacao.pdf`: o PDF da apresentação.
- `envio/Dawrah-Carmona-site.html`: o site num arquivo só, para WhatsApp ou e-mail. Fotos e Termos vão dentro do arquivo.
- `envio/Dawrah-Carmona-artifact.html`: o site como link compartilhável, no Artifact https://claude.ai/artifact/K9ogxYsbUeipspKEXdhr7q.
  - Para atualizar o link, republique a partir deste mesmo arquivo.
  - O link é privado: quem libera o acesso é o dono, pelo menu Share.

Prévia local: configuração `site-dawrahecarmona` em `.claude/launch.json`, porta 8093.

## Decisões

- **Paleta:** navy `#041e42`, bone e latão `#c2a26a`. A AEVUM usa o mesmo navy, **sem verde**.
- **Rodapé e Termos:** CNPJ do escritório, 55.927.541/0001-51, com a razão social Dawrah Carmona e Associados Ltda.
- **Bios dos sócios:** texto enviado pelo escritório.
  - Michel: Sócio, administrador com especialização em marketing.
  - Elton: Diretor Jurídico, advogado.
- **"Colecionador de relógios vintage" (Elton):** está só no PDF, não no site.
- **Apresentação:** texto curto, e a estrutura fica nos diagramas. Os diagramas são:
  - o anel do 360º;
  - as cinco frentes;
  - o quadro "sem planejamento / com planejamento";
  - os passos do planejamento comercial;
  - os formatos do Programa de Empreendedorismo.
- **Pendente:** o site ainda não está no domínio. O DNS e, provavelmente, o e-mail `contato@` estão na Locaweb; não mexer sem combinar.
