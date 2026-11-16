# -*- coding: utf-8 -*-
"""
Configuração do cliente — NOME DO CLIENTE.

Este é o ÚNICO arquivo que você precisa editar para colocar um cliente novo
no ar. Depois de editar, teste localmente:
    python build/build.py --google-file g.csv --google-shop-file gs.csv --geo-google-file geo.csv --ga4-file ga.csv --out dist/index.html

`build/config.example.py` é uma cópia intacta do modelo, para consulta
ou para restaurar `config.py` caso precise começar do zero de novo.
"""
from __future__ import annotations

# ==========================================================================
# 1) PLANILHA DO CLIENTE (Google Sheets)
# ==========================================================================
# Todas as abas ficam na MESMA planilha (mudam só os gids).
# A planilha precisa estar com o link público em modo "Qualquer pessoa com
# o link pode visualizar" (o build lê via export CSV, somente leitura).
SPREADSHEET_ID = ""   # Novamik · Made In Colors
GID_GA4 = ""    # OBRIGATÓRIO · aba GA4 (Date · Event name · Session source/medium · Event count · Sessions · Total users)
# Aba Compras: NÃO existe neste cliente. Sem GID_SALES, as compras da Visão Geral vêm do evento `purchase`
# do GA4 (sem valor => sem Faturamento/ROAS/Ticket). Se um dia houver aba Compras, preencha o gid aqui.
GID_SALES = ""
# Mídia paga: deixe "" no canal que ainda não tem planilha.
GID_META = ""             # Meta Ads: fora do escopo por enquanto (página oculta; o backend segue pronto — basta preencher o gid)
GID_GOOGLE = ""  # Google Ads · Campanhas > Grupos de anúncios > Palavras-chave (Day · Campaign Name · Ad Group Name · Ad Name · Cost · Impressions · Clicks · Conversions · Keyword)
# Google Shopping + PMax: a aba traz também campanhas de pesquisa — elas são EXCLUÍDAS: só entram campanhas cujo
# nome casa com GOOGLE_SHOP_PATTERN (e que não existam na aba geral do Google).
GID_GOOGLE_SHOP = ""
GOOGLE_SHOP_PATTERN = r"shop|pmax|p-max|performance[ _-]?max"
GID_TIKTOK = ""           # sem planilha (página oculta)
# Gasto por localização (País · Região · Cidade) — alimenta a seção "Gasto por localização" da Visão Geral.
GID_GEO_META = ""
GID_GEO_GOOGLE = ""   # aba "Local no Google"

# ==========================================================================
# 2) REGRAS DE NEGÓCIO
# ==========================================================================
# Fator de imposto aplicado sobre o gasto do Meta Ads quando o toggle
# "Imposto Meta" estiver ligado. Use 1.0 se o cliente não tiver imposto
# (com 1.0 o toggle some da interface).
TAX_FACTOR = 1.0       # sem imposto (com 1.0 o toggle "Imposto" some)
TAX_LABEL = "Imposto"
# Símbolo da moeda exibido nos valores (confirme a moeda da conta do Google Ads).
CURRENCY = "R$"

# A aba Compras é uma lista de pedidos concretizados (sem coluna de status
# utilizável)? True = toda linha é compra paga. False = filtra por is_paid()
# usando a coluna "Status".
COUNT_ALL_AS_PAID = True

# Páginas ocultas na sidebar (não apaga nada: o backend/dados seguem funcionando e #meta continua abrindo a página).
HIDDEN_PAGES = ()

# Canais (opcional — os padrões abaixo já cobrem o comum). Aplicados ao
# "Session source / medium" do GA4 e a utm_source / utm_medium das compras.
#   Google Ads = source google + medium cpc/ppc/paid...
#   Meta/TikTok = source da plataforma + medium que NÃO seja orgânico.
#   Tudo que não cair em nenhum canal pago vira "Outros" (só entra na Visão Geral).
# META_SOURCES = ("facebook", "fb", "instagram", "ig", "meta", "an")
# GOOGLE_SOURCES = ("google", "googleads", "google ads")
# GOOGLE_PAID_MEDIUMS = ("cpc", "ppc", "paid", "paidsearch", "paid search", "cpm", "display")
# TIKTOK_SOURCES = ("tiktok", "tik tok", "tt")
# ORGANIC_MEDIUMS = ("", "(none)", "(not set)", "none", "organic", "referral", "social", "bio",
#                    "link_in_bio", "story", "stories", "email", "direct", "sem utm")

# ==========================================================================
# 3) RÓTULOS EXIBIDOS NA INTERFACE
# ==========================================================================
CLIENT_NAME = "Nome do Cliente"   # nome exibido no topo do menu lateral (abaixo do logo)
CLIENT_SUB = "Ecommerce"                   # subtítulo abaixo do nome
MAIN_PRODUCT = "Todos os produtos"
LOGO_FILE = "logo.png"                     # imagem do logo (em build/), embutida na sidebar e no favicon

# ==========================================================================
# 4) METAS (aba Insights) — código de cor de CAC/ROAS
# ==========================================================================
#   • ROAS: quanto MAIOR, melhor  -> desempenho = roas / ROAS_TARGET
#   • CAC : quanto MENOR, melhor  -> desempenho = CAC_TARGET / cac
# 0.0 = sem meta (a Saúde do funil usa o histórico da conta como referência).
CAC_TARGET = 0.0
ROAS_TARGET = 0.0
REPORT_BAND_LOW = 0.70
REPORT_BAND_HIGH = 1.30

# ==========================================================================
# 5) IA INSIGHTS (Cloudflare Worker) — legado/opcional, ver SETUP-IA.md
# ==========================================================================
IA_WORKER_URL = ""   # ex.: "https://SEU-WORKER.SEU-SUBDOMINIO.workers.dev"
