"""
Ponto de entrada do bot: busca vagas em todas as fontes configuradas,
filtra, remove duplicadas já enviadas e notifica no Telegram.

Uso:
    python main.py
"""
import config
import db
import notifier
from scrapers.linkedin import LinkedInScraper

# Adicione novos scrapers aqui conforme forem implementados
# (ex: GupyScraper, VagasComScraper, InfoJobsScraper...)
FONTES = [
    LinkedInScraper(palavra_chave="estágio dados", localizacao=config.LOCATION_QUERY),
    LinkedInScraper(palavra_chave="estágio programação", localizacao=config.LOCATION_QUERY),
]


def vaga_relevante(vaga: dict) -> bool:
    texto = f"{vaga.get('titulo', '')} {vaga.get('empresa', '')}".lower()

    tem_keyword_incluida = any(kw.lower() in texto for kw in config.INCLUDE_KEYWORDS)
    tem_keyword_excluida = any(kw.lower() in texto for kw in config.EXCLUDE_KEYWORDS)

    return tem_keyword_incluida and not tem_keyword_excluida


def main():
    db.init_db()

    total_encontradas = 0
    total_novas = 0

    for scraper in FONTES:
        print(f"Buscando vagas em: {scraper.nome_fonte}...")
        try:
            vagas = scraper.buscar_vagas()
        except Exception as e:
            print(f"[ERRO] Scraper {scraper.nome_fonte} falhou: {e}")
            continue

        total_encontradas += len(vagas)

        for vaga in vagas:
            if not vaga_relevante(vaga):
                continue
            if db.ja_enviada(vaga["id"]):
                continue

            print(f"Nova vaga: {vaga['titulo']} - {vaga['empresa']}")
            notifier.enviar_vaga(vaga)
            db.marcar_como_enviada(vaga)
            total_novas += 1

    print(f"\nFim da execução. {total_encontradas} vagas encontradas, {total_novas} novas enviadas.")


if __name__ == "__main__":
    main()
