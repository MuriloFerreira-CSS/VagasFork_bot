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
    # Filtro de conteúdo: precisa parecer estágio de verdade, no título.
    titulo = vaga.get("titulo", "").lower()
    tem_keyword_incluida = any(kw.lower() in titulo for kw in config.INCLUDE_KEYWORDS)
    tem_keyword_excluida = any(kw.lower() in titulo for kw in config.EXCLUDE_KEYWORDS)
    if not tem_keyword_incluida or tem_keyword_excluida:
        return False

    # Filtro de localização:
    #   - São Paulo (capital/grande SP): passa em qualquer modalidade
    #   - Fora de SP: só passa se for 100% remota
    #   - País estrangeiro: nunca passa
    local = vaga.get("local", "").lower()
    texto_local = f"{local} {titulo}"

    if any(kw in local for kw in config.LOCATION_EXCLUDE_KEYWORDS):
        return False

    eh_sp = any(kw in local for kw in config.SP_KEYWORDS)
    eh_remoto = any(kw in texto_local for kw in config.REMOTO_KEYWORDS)

    if eh_sp:
        return True
    if eh_remoto:
        return True
    return False


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
