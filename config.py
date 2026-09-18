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
# A vaga precisa conter pelo menos UMA palavra de INCLUDE_KEYWORDS no título.
# Tirei "internship" daqui de propósito: em inglês essa palavra pega vaga
# de estágio nos EUA/Europa também, e a gente só quer vaga aqui no Brasil.
INCLUDE_KEYWORDS = [
    "estágio",
    "estagio",
    "estagiário",
    "estagiaria",
]

# E NÃO pode conter nenhuma palavra de EXCLUDE_KEYWORDS
EXCLUDE_KEYWORDS = [
    "sênior",
    "senior",
    "pleno",
    "especialista",
]

# Regra de localização:
#   - Vaga em São Paulo (cidade ou grande SP): passa em QUALQUER modalidade
#     (presencial, híbrido ou remoto).
#   - Vaga fora de São Paulo: só passa se for 100% remota/home office.
#   - País estrangeiro: nunca passa, mesmo que esteja marcada como remota.
SP_KEYWORDS = [
    "são paulo", "sao paulo", "s. paulo",
    " sp,", " sp -", " sp)", ", sp", "(sp)",
    "guarulhos", "osasco", "santo andré", "santo andre", "são bernardo",
    "sao bernardo", "diadema", "barueri", "carapicuíba", "carapicuiba",
    "mogi das cruzes", "suzano", "taboão da serra", "taboao da serra",
]

REMOTO_KEYWORDS = [
    "remoto", "remote", "home office", "trabalho remoto", "100% remoto",
]

# Se a localização contiver qualquer um desses termos, a vaga é descartada
# de cara, mesmo que pareça remota.
LOCATION_EXCLUDE_KEYWORDS = [
    "united states", "usa", "estados unidos", "canada", "canadá",
    "united kingdom", "portugal", "mexico", "méxico", "india", "índia",
    "germany", "alemanha", "france", "frança", "spain", "espanha",
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
