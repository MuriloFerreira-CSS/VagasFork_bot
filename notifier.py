"""
Envio de notificações para o Telegram via API HTTP (sem dependências extras).
"""
import requests

import config


def enviar_vaga(vaga: dict):
    texto = (
        f"🎯 *Nova vaga de estágio!*\n\n"
        f"*{_escapar(vaga.get('titulo', 'Sem título'))}*\n"
        f"🏢 {_escapar(vaga.get('empresa', 'Empresa não informada'))}\n"
        f"📍 {_escapar(vaga.get('local', 'Local não informado'))}\n"
        f"🌐 Fonte: {_escapar(vaga.get('fonte', ''))}\n\n"
        f"🔗 {vaga.get('url', '')}"
    )
    _enviar_mensagem(texto)


def enviar_mensagem_simples(texto: str):
    _enviar_mensagem(texto)


def _enviar_mensagem(texto: str):
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("[AVISO] TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não configurados.")
        print(texto)
        return

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    resp = requests.post(url, json=payload, timeout=15)
    if not resp.ok:
        print(f"[ERRO] Falha ao enviar mensagem no Telegram: {resp.text}")


def _escapar(texto: str) -> str:
    """Escapa caracteres especiais do modo Markdown legado do Telegram."""
    if not texto:
        return ""
    for ch in ["_", "*", "`", "["]:
        texto = texto.replace(ch, f"\\{ch}")
    return texto
