"""
Interface base que todo scraper de fonte de vagas deve seguir.
Cada scraper retorna uma lista de dicts no formato:

{
    "id": "identificador único (ex: url ou id da vaga)",
    "titulo": "Estágio em Dados",
    "empresa": "Empresa X",
    "local": "São Paulo, SP",
    "url": "https://...",
    "fonte": "LinkedIn",
}
"""
from abc import ABC, abstractmethod


class ScraperBase(ABC):
    nome_fonte = "desconhecida"

    @abstractmethod
    def buscar_vagas(self) -> list[dict]:
        """Retorna a lista de vagas encontradas nessa fonte."""
        raise NotImplementedError
