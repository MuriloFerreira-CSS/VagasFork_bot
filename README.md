# Bot de Vagas de Estágio → Telegram

Busca vagas de estágio (foco em dados/programação) e manda pra você no Telegram assim que encontra algo novo, sem repetir vaga já enviada.

## Como funciona

```
scrapers/  → cada arquivo busca vagas em uma fonte (LinkedIn, Gupy, etc.)
config.py  → palavras-chave, credenciais do Telegram
db.py      → guarda em SQLite quais vagas já foram enviadas (evita duplicata)
notifier.py→ manda a mensagem formatada pro Telegram
main.py    → junta tudo: busca, filtra, dedup, envia
```

## 1. Criar o bot no Telegram

1. Fale com o [@BotFather](https://t.me/BotFather) no Telegram
2. `/newbot` → escolha um nome → ele te dá um **token**
3. Mande qualquer mensagem pro seu bot novo
4. Acesse `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates` e pegue o `chat.id` (é o seu `TELEGRAM_CHAT_ID`)

## 2. Rodar localmente

```bash
pip install -r requirements.txt

export TELEGRAM_BOT_TOKEN="seu_token_aqui"
export TELEGRAM_CHAT_ID="seu_chat_id_aqui"

python main.py
```

## 3. Rodar automaticamente de graça (GitHub Actions)

1. Suba esse projeto pra um repositório no seu GitHub
2. Vá em **Settings → Secrets and variables → Actions** e crie:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. Pronto — o workflow em `.github/workflows/scrape.yml` já roda a cada 3h sozinho. Você também pode disparar manualmente na aba **Actions**.

## Adicionando novas fontes

Crie um arquivo em `scrapers/`, herde de `ScraperBase` (veja `scrapers/base.py`) e implemente `buscar_vagas()` retornando uma lista de dicts com `id`, `titulo`, `empresa`, `local`, `url`, `fonte`. Depois é só importar e adicionar na lista `FONTES` em `main.py`.

Boas fontes pra tentar em seguida:
- **Gupy**: muitas empresas usam o mesmo template — vale investigar a API interna do board de vagas de empresas específicas (ex: `https://<empresa>.gupy.io`)
- **Vagas.com** / **InfoJobs**: scraping de HTML com BeautifulSoup, parecido com o do LinkedIn

## Avisos

- O scraper do LinkedIn usa um endpoint público não-oficial (usado pela paginação do site). Pode mudar sem aviso — se parar de retornar vagas, o `class_=` dos elementos em `scrapers/linkedin.py` é o primeiro lugar pra checar.
- Ajuste `INCLUDE_KEYWORDS` e `EXCLUDE_KEYWORDS` em `config.py` conforme for vendo o que funciona.
