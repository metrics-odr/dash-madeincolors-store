# CLAUDE.md — Dashboard de Resultados · Novamik - Made In Colors (Ecommerce)

> Lido automaticamente pelo Claude Code. Repositório `metrics-odr/dash-madeincolors-store`
> (engine copiada de `metrics-odr/dash-maya-shopp`, adaptada à identidade do cliente).
> URL pública: **https://metrics-odr.github.io/dash-madeincolors-store/**

## ⭐ REGRA DE PUBLICAÇÃO (sempre que houver alteração)

Ao terminar **qualquer** alteração neste repositório, o Claude deve **abrir um botão "Publicar"**
(use `AskUserQuestion` com uma opção chamada exatamente **Publicar** e outra "Agora não").
Ao clicar em **Publicar**, o Claude faz tudo de uma vez, sem pedir mais confirmações:

1. commit na branch de trabalho e `git push`;
2. **abrir Pull Request** para `main`;
3. **mesclar o PR** na `main` (squash) — a `main` dispara o GitHub Actions;
4. acompanhar o Actions e devolver: status (verde?) e a URL pública já atualizada.

Objetivo: o usuário ver a alteração publicada no navegador o quanto antes. Nunca publicar sem o clique.

## Fontes de dados (Google Sheets `1G4j0KJ7Uv3oo_Mvpdqhk7XIL9OecZLtgB2f0syyCndk`, leitura via CSV público)

| Aba | gid | Uso |
|-----|-----|-----|
| Google Ads — Campanhas · Grupos · Palavras-chave | 888044421 | página **Google Ads** (Day · Campaign · Ad Group · Ad Name · Cost · Impressions · Clicks · Conversions · Keyword) |
| Google Ads — Shopping e PMax | 1783811121 | soma na **mesma página Google Ads** (grupo "(Shopping/PMax)"). A aba traz também campanhas de pesquisa: **são excluídas** (só entram nomes que casam `GOOGLE_SHOP_PATTERN` e que não estejam na aba geral) |
| Google Ads — Gasto por localização | 1126389235 | seção **Gasto por localização** (País · Região · Cidade) na Visão Geral |
| GA4 | 1669456740 | funil por sessões (page_view → view_item → add_to_cart → begin_checkout) e **compras** (evento `purchase`) |

Não há aba de Compras/valor: **Faturamento, ROAS e Ticket aparecem "-"** (`has_revenue=false`). Compras da Visão Geral =
evento `purchase` do GA4; compras por campanha/grupo/palavra-chave = coluna Conversions do Google Ads. Se surgir uma
aba Compras ou uma coluna de valor de conversão, preencha `GID_SALES` em `build/config.py` (o resto se ativa sozinho).

## Escopo / páginas
- Sidebar: Visão Geral · **Google Ads (visão única, inclui Shopping/PMax)** · Insights de IA.
- **Meta Ads e TikTok ficam ocultos** (`HIDDEN_PAGES` em `build/config.py`); **nada do backend foi apagado** —
  basta preencher `GID_META` e remover `"meta"` de `HIDDEN_PAGES` para reativar.

## Arquitetura
```
build/build.py             # ENGINE: lê CSVs (read-only), emite media[]/ga[]/sales[]/geo[] e costura os arquivos abaixo
build/config.py            # ⭐ CONFIG DO CLIENTE (gids, moeda, nome, páginas ocultas, metas)
build/template.html        # esqueleto HTML
build/identidade-visual.css# ⭐ TODAS as cores (claro/escuro, paleta dos gráficos) — paleta Made In Colors
build/estilos.css          # layout/componentes
build/app.js               # lógica + renderização (tudo roda no navegador)
build/logo.png             # logo (embutido na sidebar e no favicon via LOGO_FILE)
build/gerar_relatorios.py  # métricas p/ Insights (workflow 23:50 BRT)
.github/workflows/deploy.yml  # build + GitHub Pages (push em build/**, cron */30 e workflow_dispatch)
ia-worker/                 # legado/opcional (workflow de deploy do Worker removido — não usar)
```
Teste local: `python build/build.py --google-file g.csv --google-shop-file gs.csv --geo-google-file geo.csv --ga4-file ga.csv --out dist/index.html`

## Pontos a confirmar com o cliente
1. Moeda: **Euro (€)** — `CURRENCY` em `build/config.py`.
2. **Faturamento/ROAS**: o cliente vai inserir na planilha; até lá ficam "-" (ajustar depois: `GID_SALES` ou coluna de valor de conversão).
3. Campanhas PMax/Shopping hoje têm gasto zero; a aba Shopping não tem coluna Conversions.

## Problemas conhecidos de publicação
- `workflow_dispatch`/cron-job.org só funcionam com o workflow na `main`.
- O sandbox do agente não alcança a API de Settings do Actions/Pages; o Pages liga sozinho via `configure-pages` (`enablement: true`).
- Token do cron-job.org: nunca commitar (ver `SETUP-CRON.md`).
