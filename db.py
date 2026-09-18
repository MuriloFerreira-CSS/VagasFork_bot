"""
Controle de vagas já enviadas, usando SQLite, pra não notificar duplicado.
"""
import sqlite3
from contextlib import contextmanager

import config


def init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS vagas_enviadas (
                id TEXT PRIMARY KEY,
                titulo TEXT,
                empresa TEXT,
                fonte TEXT,
                url TEXT,
                enviado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def ja_enviada(vaga_id: str) -> bool:
    with _connect() as conn:
        cur = conn.execute(
            "SELECT 1 FROM vagas_enviadas WHERE id = ?", (vaga_id,)
        )
        return cur.fetchone() is not None


def marcar_como_enviada(vaga: dict):
    with _connect() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO vagas_enviadas (id, titulo, empresa, fonte, url)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                vaga["id"],
                vaga.get("titulo", ""),
                vaga.get("empresa", ""),
                vaga.get("fonte", ""),
                vaga.get("url", ""),
            ),
        )
        conn.commit()


@contextmanager
def _connect():
    conn = sqlite3.connect(config.DB_PATH)
    try:
        yield conn
    finally:
        conn.close()
