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

# Regra de localização (aplicada na hora da BUSCA, em main.py — ver FONTES):
#   - Vaga em São Paulo (localização = "São Paulo, Brazil" na busca): passa
#     em QUALQUER modalidade (presencial, híbrido ou remoto).
#   - Vaga fora de São Paulo: só passa se for 100% remota (f_WT=2 na busca).
# Se a localização contiver qualquer um desses termos, a vaga é descartada
# de cara — serve de trava de segurança pro caso do LinkedIn misturar
# resultado de fora do Brasil numa busca escopada pro país.
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

# --- Envio automático de e-mail para vagas com candidatura por e-mail ---
CANDIDATO_NOME = os.environ.get("CANDIDATO_NOME", "Seu Nome")
RESUME_PATH = os.environ.get("RESUME_PATH", "curriculo.pdf")

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")  # senha de app, nunca a senha normal da conta

EMAIL_ASSUNTO_TEMPLATE = "Candidatura para a vaga de {titulo}"
EMAIL_CORPO_TEMPLATE = (
    "Olá,\n\n"
    "Me chamo {nome} e tenho interesse na vaga de {titulo} na {empresa}, "
    "encontrada no LinkedIn.\n"
    "Segue meu currículo em anexo. Fico à disposição para conversar.\n\n"
    "Atenciosamente,\n{nome}"
)

# Enquanto True, o bot só MOSTRA no log o e-mail que mandaria, sem enviar
# de verdade. Deixe True até conferir que texto e currículo estão certos,
# e só troque pra False (via secret no GitHub) quando tiver certeza.
EMAIL_DRY_RUN = os.environ.get("EMAIL_DRY_RUN", "true").lower() == "true"
