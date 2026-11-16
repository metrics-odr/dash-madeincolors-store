# Dashboard de Resultados — Novamik · Made In Colors (Ecommerce)

Publicado em **https://metrics-odr.github.io/dash-madeincolors-store/** (GitHub Pages), gerado por uma
engine de BI estática (HTML/CSS/JS + Chart.js) a partir de uma planilha Google (somente leitura):
Google Ads (campanhas › grupos › palavras-chave), Google Shopping/PMax, gasto por localização e GA4.
Atualiza a cada ~30 min (GitHub Actions disparado pelo cron-job.org — ver `SETUP-CRON.md`).

Páginas: **Visão Geral** · **Google Ads** · **Shopping & PMax** · **Insights de IA**
(Meta Ads/TikTok existem no backend, ocultos na sidebar).

Configuração do cliente: `build/config.py` · cores: `build/identidade-visual.css` · detalhes: `CLAUDE.md`.

Teste local:
```bash
python build/build.py --out dist/index.html
```
