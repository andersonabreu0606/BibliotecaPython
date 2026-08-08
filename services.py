from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import select, or_, func
from sqlalchemy.exc import IntegrityError

from database import Database
from models import Livro, Usuario, Emprestimo


class BibliotecaErro(Exception):
    """Erro de negócio conhecido e apresentável ao utilizador."""
    pass


class BibliotecaService:
    """Reúne as regras de negócio da biblioteca."""

    def __init__(self, db: Database) -> None:
        self.db = db

    # ----------------------------
    # Livros
    # ----------------------------
    def cadastrar_livro(
        self,
        titulo: str,
        autor: str,
        ano_publicacao: int,
        copias: int,
    ) -> Livro:
        titulo = titulo.strip()
        autor = autor.strip()

        if not titulo or not autor:
            raise BibliotecaErro("Título e autor são obrigatórios.")
        if ano_publicacao < 0 or ano_publicacao > datetime.now().year + 1:
            raise BibliotecaErro("Ano de publicação inválido.")
        if copias < 1:
            raise BibliotecaErro("O livro deve possuir pelo menos 1 cópia.")

        livro = Livro(
            titulo=titulo,
            autor=autor,
            ano_publicacao=ano_publicacao,
            copias_total=copias,
            copias_disponiveis=copias,
        )

        with self.db.sessao() as s:
            s.add(livro)
            s.commit()
            s.refresh(livro)
            return livro

    def listar_livros(self, somente_disponiveis: bool = False) -> list[Livro]:
        with self.db.sessao() as s:
            stmt = select(Livro).order_by(Livro.titulo)
            if somente_disponiveis:
                stmt = stmt.where(Livro.copias_disponiveis > 0)
            return list(s.scalars(stmt).all())

    def buscar_livros(
        self,
        titulo: str | None = None,
        autor: str | None = None,
        ano: int | None = None,
    ) -> list[Livro]:
        with self.db.sessao() as s:
            stmt = select(Livro)

            if titulo:
                stmt = stmt.where(func.lower(Livro.titulo).contains(titulo.strip().lower()))
            if autor:
                stmt = stmt.where(func.lower(Livro.autor).contains(autor.strip().lower()))
            if ano is not None:
                stmt = stmt.where(Livro.ano_publicacao == ano)

            stmt = stmt.order_by(Livro.titulo)
            return list(s.scalars(stmt).all())

    # ----------------------------
    # Usuários
    # ----------------------------
    def cadastrar_usuario(
        self,
        nome: str,
        identificacao: str,
        contato: str,
    ) -> Usuario:
        nome = nome.strip()
        identificacao = identificacao.strip()
        contato = contato.strip()

        if not nome or not identificacao or not contato:
            raise BibliotecaErro("Nome, identificação e contato são obrigatórios.")

        usuario = Usuario(
            nome=nome,
            identificacao=identificacao,
            contato=contato,
        )

        try:
            with self.db.sessao() as s:
                s.add(usuario)
                s.commit()
                s.refresh(usuario)
                return usuario
        except IntegrityError as exc:
            raise BibliotecaErro(
                "Já existe um usuário com esse número de identificação."
            ) from exc

    def listar_usuarios(self) -> list[Usuario]:
        with self.db.sessao() as s:
            return list(s.scalars(select(Usuario).order_by(Usuario.nome)).all())

    # ----------------------------
    # Empréstimos e devoluções
    # ----------------------------
    def emprestar_livro(self, livro_id: int, usuario_id: int) -> Emprestimo:
        with self.db.sessao() as s:
            try:
                livro = s.get(Livro, livro_id)
                usuario = s.get(Usuario, usuario_id)

                if livro is None:
                    raise BibliotecaErro("Livro não encontrado.")
                if usuario is None:
                    raise BibliotecaErro("Usuário não encontrado.")
                if livro.copias_disponiveis <= 0:
                    raise BibliotecaErro("Não há cópias disponíveis deste livro.")

                # Evita empréstimo duplicado do mesmo título ao mesmo utilizador.
                duplicado = s.scalar(
                    select(Emprestimo).where(
                        Emprestimo.livro_id == livro_id,
                        Emprestimo.usuario_id == usuario_id,
                        Emprestimo.status == "EMPRESTADO",
                        Emprestimo.data_devolucao.is_(None),
                    )
                )
                if duplicado:
                    raise BibliotecaErro(
                        "Este usuário já possui um empréstimo ativo deste livro."
                    )

                livro.copias_disponiveis -= 1
                emprestimo = Emprestimo(
                    livro_id=livro_id,
                    usuario_id=usuario_id,
                    status="EMPRESTADO",
                )
                s.add(emprestimo)
                s.commit()
                s.refresh(emprestimo)
                return emprestimo

            except BibliotecaErro:
                s.rollback()
                raise
            except Exception:
                s.rollback()
                raise

    def devolver_livro(self, emprestimo_id: int) -> Emprestimo:
        with self.db.sessao() as s:
            try:
                emprestimo = s.get(Emprestimo, emprestimo_id)

                if emprestimo is None:
                    raise BibliotecaErro("Empréstimo não encontrado.")
                if not emprestimo.ativo:
                    raise BibliotecaErro("Este empréstimo já foi devolvido.")

                livro = s.get(Livro, emprestimo.livro_id)
                if livro is None:
                    raise BibliotecaErro("Livro associado ao empréstimo não encontrado.")

                emprestimo.status = "DEVOLVIDO"
                emprestimo.data_devolucao = datetime.now(timezone.utc).replace(tzinfo=None)
                livro.copias_disponiveis += 1

                # Proteção contra inconsistência.
                if livro.copias_disponiveis > livro.copias_total:
                    raise BibliotecaErro(
                        "Inconsistência de estoque detectada. A devolução foi cancelada."
                    )

                s.commit()
                s.refresh(emprestimo)
                return emprestimo

            except BibliotecaErro:
                s.rollback()
                raise
            except Exception:
                s.rollback()
                raise

    def listar_emprestimos(self, somente_ativos: bool = False) -> list[Emprestimo]:
        with self.db.sessao() as s:
            stmt = select(Emprestimo).order_by(Emprestimo.data_emprestimo.desc())
            if somente_ativos:
                stmt = stmt.where(
                    Emprestimo.status == "EMPRESTADO",
                    Emprestimo.data_devolucao.is_(None),
                )
            emprestimos = list(s.scalars(stmt).all())

            # Carrega as relações enquanto a sessão está aberta.
            for e in emprestimos:
                _ = e.livro.titulo
                _ = e.usuario.nome

            return emprestimos

    # ----------------------------
    # Relatórios
    # ----------------------------
    def resumo(self) -> dict[str, int]:
        with self.db.sessao() as s:
            total_livros = s.scalar(select(func.count(Livro.id))) or 0
            total_usuarios = s.scalar(select(func.count(Usuario.id))) or 0
            emprestimos_ativos = s.scalar(
                select(func.count(Emprestimo.id)).where(
                    Emprestimo.status == "EMPRESTADO",
                    Emprestimo.data_devolucao.is_(None),
                )
            ) or 0
            copias_disponiveis = s.scalar(
                select(func.coalesce(func.sum(Livro.copias_disponiveis), 0))
            ) or 0

            return {
                "livros_catalogados": int(total_livros),
                "usuarios_cadastrados": int(total_usuarios),
                "emprestimos_ativos": int(emprestimos_ativos),
                "copias_disponiveis": int(copias_disponiveis),
            }
