from __future__ import annotations

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Base


class Database:
    """Responsável por configurar a conexão e fornecer sessões de banco."""

    def __init__(self, url: str | None = None) -> None:
        self.url = url or os.getenv("DATABASE_URL", "sqlite:///biblioteca.db")

        connect_args = {}
        if self.url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}

        self.engine = create_engine(
            self.url,
            future=True,
            pool_pre_ping=True,
            connect_args=connect_args,
        )
        self._Session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            class_=Session,
        )

    def criar_tabelas(self) -> None:
        Base.metadata.create_all(self.engine)

    def sessao(self) -> Session:
        return self._Session()
