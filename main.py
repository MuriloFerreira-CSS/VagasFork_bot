"""
Ponto de entrada do bot: busca vagas em todas as fontes configuradas,
filtra, remove duplicadas já enviadas e notifica no Telegram.

Uso:
    python main.py
"""
import config
import db
import email_sender
import job_details
import notifier
import whatsapp_notifier
from scrapers.linkedin import GEO_ID_BRASIL, LinkedInScraper

# Adicione novos scrapers aqui conforme forem implementados
# (ex: GupyScraper, VagasComScraper, InfoJobsScraper...)
#
# Duas buscas por palavra-chave:
#   - "sp": localização = São Paulo, qualquer modalidade (presencial/híbrido/remoto)
#   - "remoto": geoId = Brasil inteiro, só vagas marcadas como remotas (f_WT=2)
# Marcar isso na própria busca é mais confiável que tentar adivinhar pelo
# texto da localização depois, porque o LinkedIn às vezes só mostra
# "Brazil" em vagas remotas, sem escrever "remoto" em lugar nenhum.
PALAVRAS_CHAVE = ["estágio dados", "estágio programação"]

FONTES = []
for palavra in PALAVRAS_CHAVE:
    FONTES.append(
        LinkedInScraper(
            palavra_chave=palavra,
            localizacao="São Paulo, Brazil",
            apenas_remoto=False,
            modo="sp",
        )
    )
    FONTES.append(
        LinkedInScraper(
            palavra_chave=palavra,
            localizacao="Brasil",
            geo_id=GEO_ID_BRASIL,
            apenas_remoto=True,
            modo="remoto",
        )
    )


def vaga_relevante(vaga: dict) -> bool:
    # Filtro de conteúdo: precisa parecer estágio de verdade, no título.
    titulo = vaga.get("titulo", "").lower()
    tem_keyword_incluida = any(kw.lower() in titulo for kw in config.INCLUDE_KEYWORDS)
    tem_keyword_excluida = any(kw.lower() in titulo for kw in config.EXCLUDE_KEYWORDS)
    if not tem_keyword_incluida or tem_keyword_excluida:
        return False

    # Filtro de país: mesmo vindo de uma busca escopada pro Brasil, o
    # LinkedIn ocasionalmente mistura resultado de fora — descarta se o
    # texto do local mencionar outro país conhecido.
    local = vaga.get("local", "").lower()
    if any(kw in local for kw in config.LOCATION_EXCLUDE_KEYWORDS):
        return False

    # A localização/modalidade já foi garantida na hora da busca (ver
    # FONTES acima): "sp" veio filtrado por localização São Paulo, e
    # "remoto" veio filtrado por f_WT=2 (só remoto) no Brasil inteiro.
    return vaga.get("modo") in ("sp", "remoto")


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

            # Busca a descrição completa da vaga pra achar e-mail de contato
            # e/ou link externo de aplicação (só funciona pra vagas do
            # LinkedIn, que têm job_id).
            if vaga.get("job_id"):
                detalhes = job_details.buscar_detalhes(vaga["job_id"])
                if detalhes.get("link_aplicacao"):
                    vaga["link_aplicacao"] = detalhes["link_aplicacao"]
                if detalhes.get("email"):
                    vaga["email_contato"] = detalhes["email"]
                    email_sender.enviar_candidatura(vaga, detalhes["email"])
                    vaga["email_candidatura_enviada"] = not config.EMAIL_DRY_RUN

            notifier.enviar_vaga(vaga)
            whatsapp_notifier.enviar_vaga(vaga)
            db.marcar_como_enviada(vaga)
            total_novas += 1

    print(f"\nFim da execução. {total_encontradas} vagas encontradas, {total_novas} novas enviadas.")


if __name__ == "__main__":
    main()
