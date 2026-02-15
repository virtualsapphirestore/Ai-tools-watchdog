# Manual de Operação: AI Tools Watchdog

Este guia ensina como colocar seu sistema de renda passiva automátizada no ar usando apenas ferramentas gratuitas (GitHub).

## 1. Pré-requisitos
*   Uma conta no GitHub.
*   Uma chave de API do Google Gemini (Gratuita). [Pegue aqui](https://aistudio.google.com/).

## 2. Instalação (Setup Inicial)

### Passo A: Preparar os arquivos
Você já tem todos os arquivos necessários na pasta `ai_tools_watchdog`. O que precisamos fazer é enviá-los para o GitHub.

1.  Crie um novo repositório no GitHub (ex: `ai-tools-watchdog`). Deixe-o **Público**.
2.  Abra um terminal na pasta `ai_tools_watchdog` e rode:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/ai-tools-watchdog.git
git push -u origin main
```

## 3. Configuração da Automação
Para que o robô funcione, ele precisa da sua senha (API Key) para escrever os reviews.

1.  No seu repositório do GitHub, vá em **Settings > Secrets and variables > Actions**.
2.  Clique em **New repository secret**.
3.  **Name:** `GOOGLE_API_KEY`
4.  **Value:** (Cole sua chave da API do Gemini aqui).
5.  Clique em **Add secret**.

## 4. Publicação do Site
Para que o site fique visível para o mundo:

1.  Vá em **Settings > Pages**.
2.  Em **Build and deployment > Source**, mantenha "Deploy from a branch".
3.  **Importante:** A branch `gh-pages` só será criada após a primeira execução do robô.
4.  **Dica:** Vá na aba **Actions**, selecione o workflow "Daily AI Tools Update" e clique em **Run workflow** manualmente para testar.
5.  Espere terminar (deve levar uns 2-3 minutos).
6.  Volte em **Settings > Pages**.
7.  Agora em **Branch**, selecione `main` (ou `gh-pages` se preferir gerar HTML estático, mas este script atualiza o README/index da branch principal) e salve. 
    *   *Nota: O script atual edita o `index.md` na branch principal. Se você usar o GitHub Pages para servir o `index.md` da branch `main` (root), ele funcionará.*

Em instantes, seu site estará no ar em `https://SEU_USUARIO.github.io/ai-tools-watchdog/`.

## 5. Como Monetizar (Fase 2)
Agora que o sistema roda sozinho:

1.  **Cadastre-se em Programas de Afiliados:** Procure por ferramentas SaaS populares (Jasper, Copy.ai, etc) e cadastre-se no PartnerStack ou Impact.
2.  **Injete seus Links:**
    *   Edite o arquivo `src/scraper.py` futuramente para substituir links diretos pelos seus links de afiliado quando encontrar matches.
    *   Ou manualmente adicione "Ferramentas em Destaque" no `index.md` com seus links.

## 6. Manutenção
O sistema roda todo dia às 12:00 UTC (09:00 BRT).
Se quiser mudar o horário, edite o arquivo `.github/workflows/daily_update.yml` na linha `cron`.

Parabéns! Você tem um ativo digital trabalhando por você. 🚀
