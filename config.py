"""
Configurações do bot de busca de vagas de estágio.
"""
import os

# --- Telegram ---
# Crie um bot com o @BotFather no Telegram e pegue o token.
# Para pegar o CHAT_ID: mande uma mensagem pro seu bot e acesse
# https://api.telegram.org/bot<SEU_TOKEN>/getUpdates
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# --- Palavras-chave para filtrar vagas ---
# A vaga precisa conter pelo menos UMA palavra de INCLUDE_KEYWORDS
INCLUDE_KEYWORDS = [
    "estágio",
    "estagio",
    "estagiário",
    "internship",
]

# E NÃO pode conter nenhuma palavra de EXCLUDE_KEYWORDS
EXCLUDE_KEYWORDS = [
    "sênior",
    "senior",
    "pleno",
    "especialista",
]

# Áreas de interesse (usado pra dar prioridade/score, não é filtro obrigatório)
AREA_KEYWORDS = [
    "dados",
    "data",
    "python",
    "sql",
    "power bi",
    "powerbi",
    "análise",
    "analytics",
    "programação",
    "desenvolvedor",
    "developer",
    "software",
    "ti",
    "tecnologia da informação",
]

# --- Banco de dados local (evita reenviar vaga repetida) ---
DB_PATH = os.environ.get("DB_PATH", "vagas.db")

# --- Localização (opcional, usado como filtro em algumas fontes) ---
LOCATION_QUERY = os.environ.get("LOCATION_QUERY", "Brasil")
