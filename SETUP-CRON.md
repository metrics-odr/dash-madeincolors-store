# Ativação + configuração do cron-job.org (dash-madeincolors-store)

> owner/repo: `metrics-odr/dash-madeincolors-store` · URL do Pages:
> `https://metrics-odr.github.io/dash-madeincolors-store/`. O **token nunca é comitado**:
> ele vai apenas no cron-job.org (substitua `TOKEN_AQUI`).

`workflow_dispatch` só existe na branch padrão (`main`). Na 1ª execução o workflow habilita o
GitHub Pages sozinho (`actions/configure-pages` com `enablement: true`).

## Token (fine-grained)
GitHub → Settings → Developer settings → Fine-grained tokens → Generate:
- Repository access: **Only select repositories → `dash-madeincolors-store`**
- Permissions → **Actions: Read and write**

## cron-job.org — cada bloco abaixo é copiado separadamente

**URL**
```
https://api.github.com/repos/metrics-odr/dash-madeincolors-store/actions/workflows/deploy.yml/dispatches
```
**Método**
```
POST
```
**Schedule**
```
A cada 30 minutos (Every 30 minutes)
```

**Header 1 — nome**
```
Accept
```
**Header 1 — valor**
```
application/vnd.github+json
```
**Header 2 — nome**
```
Authorization
```
**Header 2 — valor**
```
Bearer TOKEN_AQUI
```
**Header 3 — nome**
```
X-GitHub-Api-Version
```
**Header 3 — valor**
```
2022-11-28
```
**Header 4 — nome**
```
Content-Type
```
**Header 4 — valor**
```
application/json
```
**Request body**
```
{"ref":"main"}
```

## Como saber se funcionou
- Resposta esperada: **HTTP 204 No Content**; em Actions aparece uma execução nova a cada disparo.
- 401/403 = token errado/sem Actions: write · 404 = owner/repo/arquivo errado ou fora da `main` · 422 = workflow ainda não está na `main`.
