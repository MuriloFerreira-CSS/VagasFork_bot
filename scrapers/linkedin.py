"""
Scraper para o LinkedIn usando o endpoint público de "guest" (sem precisar
de login/API key). Esse endpoint é o mesmo usado pela paginação da busca
de vagas normal do site, então pode mudar sem aviso — se parar de
funcionar, é o primeiro lugar a checar.
"""
import re

import requests
from bs4 import BeautifulSoup

from scrapers.base import ScraperBase

BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"


class LinkedInScraper(ScraperBase):
    nome_fonte = "LinkedIn"

    def __init__(self, palavra_chave="estágio dados", localizacao="Brasil", paginas=2):
        self.palavra_chave = palavra_chave
        self.localizacao = localizacao
        self.paginas = paginas

    def buscar_vagas(self) -> list[dict]:
        vagas = []
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            )
        }

        for pagina in range(self.paginas):
            params = {
                "keywords": self.palavra_chave,
                "location": self.localizacao,
                "start": pagina * 25,
            }
            try:
                resp = requests.get(BASE_URL, params=params, headers=headers, timeout=15)
                resp.raise_for_status()
            except requests.RequestException as e:
                print(f"[ERRO] LinkedIn scraper falhou na página {pagina}: {e}")
                break

            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.find_all("div", class_="base-card")
            if not cards:
                break

            for card in cards:
                vaga = self._parsear_card(card)
                if vaga:
                    vagas.append(vaga)

        return vagas

    def _parsear_card(self, card) -> dict | None:
        try:
            titulo_tag = card.find("h3", class_="base-search-card__title")
            empresa_tag = card.find("h4", class_="base-search-card__subtitle")
            local_tag = card.find("span", class_="job-search-card__location")
            link_tag = card.find("a", class_="base-card__full-link")

            if not (titulo_tag and link_tag):
                return None

            url = link_tag["href"].split("?")[0]
            # O id da vaga costuma vir no final da URL, ex: .../view/1234567890
            match = re.search(r"(\d+)$", url)
            vaga_id = match.group(1) if match else url

            return {
                "id": f"linkedin_{vaga_id}",
                "titulo": titulo_tag.get_text(strip=True),
                "empresa": empresa_tag.get_text(strip=True) if empresa_tag else "",
                "local": local_tag.get_text(strip=True) if local_tag else "",
                "url": url,
                "fonte": self.nome_fonte,
            }
        except Exception as e:
            print(f"[ERRO] Falha ao parsear card do LinkedIn: {e}")
            return None
