"""
Envio automático de e-mail de candidatura, com currículo em anexo, para
vagas que divulgam e-mail de contato na descrição.

Por padrão fica em modo DRY RUN (config.EMAIL_DRY_RUN=True): só mostra no
log o que mandaria, sem enviar de verdade. Só desative depois de conferir
que o texto do e-mail e o currículo estão corretos — e-mail real mandado
errado pra empresa não tem como desfazer.
"""
import os
import smtplib
from email.message import EmailMessage

import config


def enviar_candidatura(vaga: dict, email_destino: str):
    assunto = config.EMAIL_ASSUNTO_TEMPLATE.format(titulo=vaga.get("titulo", ""))
    corpo = config.EMAIL_CORPO_TEMPLATE.format(
        nome=config.CANDIDATO_NOME,
        titulo=vaga.get("titulo", ""),
        empresa=vaga.get("empresa", ""),
    )

    if config.EMAIL_DRY_RUN:
        print(f"[DRY RUN] Mandaria e-mail de candidatura para {email_destino}")
        print(f"[DRY RUN] Assunto: {assunto}")
        return

    if not config.SMTP_USER or not config.SMTP_PASSWORD:
        print("[AVISO] SMTP_USER/SMTP_PASSWORD não configurados — e-mail não enviado.")
        return

    if not os.path.exists(config.RESUME_PATH):
        print(f"[AVISO] Currículo não encontrado em '{config.RESUME_PATH}' — e-mail não enviado.")
        return

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = config.SMTP_USER
    msg["To"] = email_destino
    msg["Bcc"] = config.SMTP_USER  # você recebe uma cópia de tudo que for enviado
    msg.set_content(corpo)

    with open(config.RESUME_PATH, "rb") as f:
        dados_curriculo = f.read()
    nome_arquivo = os.path.basename(config.RESUME_PATH)
    msg.add_attachment(
        dados_curriculo,
        maintype="application",
        subtype="octet-stream",
        filename=nome_arquivo,
    )

    try:
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(config.SMTP_USER, config.SMTP_PASSWORD)
            smtp.send_message(msg)
        print(f"[OK] E-mail de candidatura enviado para {email_destino}")
    except Exception as e:
        print(f"[ERRO] Falha ao enviar e-mail para {email_destino}: {e}")
