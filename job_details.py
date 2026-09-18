"""
Busca detalhes completos de uma vaga do LinkedIn (descrição e link externo
de aplicação, quando existir), usando o mesmo endpoint guest público que a
página de detalhes da vaga usa. Só funciona pra vagas vindas do scraper do
LinkedIn (depende do job_id).
"""
import re

import requests
from bs4 import BeautifulSoup

DETAIL_URL = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

# Pega o primeiro e-mail "de verdade" na descrição, ignorando endereços
# do próprio LinkedIn e domínios de rastreamento comuns.
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
DOMINIOS_IGNORADOS = ["linkedin.com", "sentry.io", "example.com"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def buscar_detalhes(job_id: str) -> dict:
    """Retorna {"email": str|None, "link_aplicacao": str|None}."""
    resultado = {"email": None, "link_aplicacao": None}

    try:
        resp = requests.get(DETAIL_URL.format(job_id=job_id), headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERRO] Falha ao buscar detalhes da vaga {job_id}: {e}")
        return resultado

    soup = BeautifulSoup(resp.text, "html.parser")

    descricao_tag = soup.find("div", class_="show-more-less-html__markup")
    if descricao_tag:
        texto = descricao_tag.get_text(" ", strip=True)
        for match in EMAIL_REGEX.finditer(texto):
            email = match.group(0)
            if not any(dominio in email.lower() for dominio in DOMINIOS_IGNORADOS):
                resultado["email"] = email
                break

    # Vagas com aplicação externa trazem a URL escondida num comentário
    # HTML dentro de <code id="applyUrl">. Vagas "Easy Apply" (só dentro do
    # LinkedIn) não têm essa tag.
    apply_tag = soup.find("code", id="applyUrl")
    if apply_tag:
        match = re.search(r'"(https?://[^"]+)"', apply_tag.get_text())
        if match:
            resultado["link_aplicacao"] = match.group(1)

    return resultado
