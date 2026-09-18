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

## 4. Candidatura automática por e-mail + link direto

Quando uma vaga tem e-mail de contato na descrição, o bot manda um e-mail automático com seu currículo em anexo, e sempre inclui na notificação do Telegram o link direto de aplicação (o oficial do site da empresa, quando a vaga tiver um, ou o link do LinkedIn).

**Configuração (secrets do GitHub, iguais aos do Telegram):**

| Secret | O que é |
|---|---|
| `CANDIDATO_NOME` | Seu nome, usado no corpo do e-mail |
| `RESUME_PATH` | Caminho do seu currículo dentro do repositório, ex: `curriculo.pdf` |
| `SMTP_USER` | Seu e-mail (ex: Gmail) |
| `SMTP_PASSWORD` | **Senha de app**, não a senha normal — no Gmail: Conta Google → Segurança → Verificação em duas etapas → Senhas de app |
| `SMTP_HOST` | `smtp.gmail.com` (ou o SMTP do seu provedor) |
| `SMTP_PORT` | `587` |
| `EMAIL_DRY_RUN` | `true` (recomendado no início) ou `false` |

**Passos:**
1. Suba seu currículo (PDF) pra raiz do repositório com o nome que você definir em `RESUME_PATH`
2. Crie os secrets acima
3. Deixe `EMAIL_DRY_RUN=true` no começo — o bot só vai *simular* o envio e mostrar no log o que mandaria, sem disparar de verdade. Confira o log de algumas execuções pra ver se o texto e o e-mail detectado fazem sentido
4. Quando estiver satisfeito, muda o secret `EMAIL_DRY_RUN` pra `false` — aí os e-mails passam a ser enviados de verdade (você recebe uma cópia oculta de cada um, via BCC)

⚠️ **Atenção**: com `EMAIL_DRY_RUN=false`, o bot manda e-mail de verdade pra empresas sem você revisar antes. Vale rodar em dry run por um tempo pra garantir que o texto e o currículo estão bons, e ficar de olho nos logs depois de ativar.

## 5. Notificação também no WhatsApp (opcional)

Usa o [CallMeBot](https://www.callmebot.com/blog/free-api-whatsapp-messages/), um serviço gratuito pra notificação pessoal (não precisa de conta de desenvolvedor Meta nem aprovação de negócio).

**Ativação (só uma vez, fora do código):**
1. Salva o número **+34 644 59 71 67** nos seus contatos do WhatsApp
2. Manda pra esse número, no WhatsApp, exatamente esta mensagem: `I allow callmebot to send me messages`
3. Em alguns minutos ele responde com sua **API key**

**Secrets do GitHub:**

| Secret | O que é |
|---|---|
| `WHATSAPP_PHONE` | Seu número com código do país, sem `+` nem espaços (ex: `5511999999999`) |
| `WHATSAPP_APIKEY` | A API key que o CallMeBot te mandou |

Com esses dois configurados, toda vaga nova é enviada tanto no Telegram quanto no WhatsApp automaticamente. Se deixar em branco, ele continua notificando só pelo Telegram, sem erro.

⚠️ É um serviço de terceiros com limite de uso — serve bem pra notificação pessoal de baixo volume, mas não é a API oficial do WhatsApp. Se quiser algo mais robusto (com SLA, sem depender de terceiro), a alternativa é a [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api) oficial da Meta, que exige criar um app de desenvolvedor.

## Avisos

- O scraper do LinkedIn usa um endpoint público não-oficial (usado pela paginação do site). Pode mudar sem aviso — se parar de retornar vagas, o `class_=` dos elementos em `scrapers/linkedin.py` é o primeiro lugar pra checar.
- Ajuste `INCLUDE_KEYWORDS`, `EXCLUDE_KEYWORDS`, `SP_KEYWORDS` e `REMOTO_KEYWORDS` em `config.py` conforme for vendo o que funciona.
- Automatizar o "Easy Apply" do LinkedIn (candidatura só dentro do site) não é feito por esse bot de propósito — viola os termos de uso do LinkedIn e pode banir a conta.
