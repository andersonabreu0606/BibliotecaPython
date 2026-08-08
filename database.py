from __future__ import annotations

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from models import Base


def normalizar_database_url(url: str) -> str:
    """Normaliza URLs PostgreSQL para o driver Psycopg 3 do SQLAlchemy."""
    url = url.strip()

    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]

    if url.startswith("postgresql://"):
        url = "postgresql+psycopg://" + url[len("postgresql://"):]

    return url


class Database:
    """Responsável por configurar a conexão e fornecer sessões de banco."""

    def __init__(self, url: str | None = None) -> None:
        raw_url = url or os.getenv("DATABASE_URL") or "sqlite:///biblioteca.db"
        self.url = normalizar_database_url(raw_url)

        connect_args = {}
        if self.url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}
        elif self.url.startswith("postgresql"):
            connect_args = {"connect_timeout": 10}

        self.engine = create_engine(
            self.url,
            future=True,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args=connect_args,
        )

        self._Session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            class_=Session,
        )

    def testar_conexao(self) -> bool:
        """Executa uma consulta simples para validar a conectividade."""
        with self.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True

    def criar_tabelas(self) -> None:
        Base.metadata.create_all(self.engine)

    def sessao(self) -> Session:
        return self._Session()
