"""
Envio de notificações pro WhatsApp usando o CallMeBot — um serviço
gratuito feito pra notificação pessoal (não é a API oficial da Meta, mas
não exige conta de desenvolvedor nem processo de aprovação de negócio).

Ativação (só precisa fazer uma vez, fora do código):
  1. Salva o número +34 644 59 71 67 nos seus contatos do WhatsApp
  2. Manda pra esse número, no WhatsApp, exatamente esta mensagem:
     "I allow callmebot to send me messages"
  3. Em alguns minutos ele responde com sua API key
  4. Usa seu número (com código do país, ex: 5511999999999) e essa
     API key nas variáveis WHATSAPP_PHONE e WHATSAPP_APIKEY

Limitações: é um serviço de terceiros, não da Meta — ideal pra notificação
pessoal de baixo volume. Não use pra mandar mensagem em massa ou pra
outras pessoas; ele pode bloquear o número em caso de abuso.
"""
import requests

import config

CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


def enviar_vaga(vaga: dict):
    link = vaga.get("link_aplicacao") or vaga.get("url", "")
    texto = (
        f"🎯 Nova vaga de estágio!\n\n"
        f"{vaga.get('titulo', 'Sem título')}\n"
        f"🏢 {vaga.get('empresa', 'Empresa não informada')}\n"
        f"📍 {vaga.get('local', 'Local não informado')}\n\n"
        f"🔗 {link}"
    )
    _enviar_mensagem(texto)


def _enviar_mensagem(texto: str):
    if not config.WHATSAPP_PHONE or not config.WHATSAPP_APIKEY:
        print("[AVISO] WHATSAPP_PHONE ou WHATSAPP_APIKEY não configurados — notificação de WhatsApp pulada.")
        return

    params = {
        "phone": config.WHATSAPP_PHONE,
        "text": texto,
        "apikey": config.WHATSAPP_APIKEY,
    }
    try:
        resp = requests.get(CALLMEBOT_URL, params=params, timeout=15)
        if not resp.ok:
            print(f"[ERRO] Falha ao enviar mensagem no WhatsApp: {resp.text}")
    except requests.RequestException as e:
        print(f"[ERRO] Falha ao enviar mensagem no WhatsApp: {e}")
