from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utc_now() -> datetime:
    """Retorna o instante atual em UTC, sem timezone, para compatibilidade ampla."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Base(DeclarativeBase):
    """Classe base para os modelos ORM do sistema."""
    pass


class Livro(Base):
    __tablename__ = "livros"
    __table_args__ = (
        CheckConstraint("copias_total >= 0", name="ck_livros_total_nao_negativo"),
        CheckConstraint("copias_disponiveis >= 0", name="ck_livros_disp_nao_negativo"),
        CheckConstraint(
            "copias_disponiveis <= copias_total",
            name="ck_livros_disp_menor_total",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    autor: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    ano_publicacao: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    copias_total: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    copias_disponiveis: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    emprestimos: Mapped[list["Emprestimo"]] = relationship(back_populates="livro")

    @property
    def disponivel(self) -> bool:
        return self.copias_disponiveis > 0

    def __repr__(self) -> str:
        return f"<Livro(id={self.id}, titulo={self.titulo!r})>"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    identificacao: Mapped[str] = mapped_column(
        String(80), nullable=False, unique=True, index=True
    )
    contato: Mapped[str] = mapped_column(String(150), nullable=False)

    emprestimos: Mapped[list["Emprestimo"]] = relationship(back_populates="usuario")

    def __repr__(self) -> str:
        return f"<Usuario(id={self.id}, identificacao={self.identificacao!r})>"


class SistemaUsuario(Base):
    __tablename__ = "usuarios_sistema"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    perfil: Mapped[str] = mapped_column(String(30), nullable=False, default="operador")
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<SistemaUsuario(id={self.id}, username={self.username!r}, perfil={self.perfil!r})>"


class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    livro_id: Mapped[int] = mapped_column(
        ForeignKey("livros.id"), nullable=False, index=True
    )
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), nullable=False, index=True
    )
    data_emprestimo: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utc_now
    )
    data_devolucao: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="EMPRESTADO"
    )

    livro: Mapped[Livro] = relationship(back_populates="emprestimos")
    usuario: Mapped[Usuario] = relationship(back_populates="emprestimos")

    @property
    def ativo(self) -> bool:
        return self.status == "EMPRESTADO" and self.data_devolucao is None

    def __repr__(self) -> str:
        return f"<Emprestimo(id={self.id}, status={self.status!r})>"
