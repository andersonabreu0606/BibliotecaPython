from __future__ import annotations

import os
import pandas as pd
import streamlit as st

# Em produção no Streamlit Community Cloud, DATABASE_URL pode ser definido em Secrets.
try:
    if "DATABASE_URL" in st.secrets:
        os.environ["DATABASE_URL"] = st.secrets["DATABASE_URL"]
except Exception:
    pass

from database import Database
from services import BibliotecaService, BibliotecaErro


st.set_page_config(
    page_title="Biblioteca Digital",
    page_icon="📚",
    layout="wide",
)

db = Database()
db.criar_tabelas()
service = BibliotecaService(db)


def livros_df(livros):
    return pd.DataFrame([
        {
            "ID": l.id,
            "Título": l.titulo,
            "Autor": l.autor,
            "Ano": l.ano_publicacao,
            "Cópias totais": l.copias_total,
            "Disponíveis": l.copias_disponiveis,
        }
        for l in livros
    ])


def usuarios_df(usuarios):
    return pd.DataFrame([
        {
            "ID": u.id,
            "Nome": u.nome,
            "Identificação": u.identificacao,
            "Contato": u.contato,
        }
        for u in usuarios
    ])


def emprestimos_df(emprestimos):
    return pd.DataFrame([
        {
            "ID empréstimo": e.id,
            "Livro": e.livro.titulo,
            "Usuário": e.usuario.nome,
            "Data empréstimo": e.data_emprestimo.strftime("%d/%m/%Y %H:%M"),
            "Data devolução": (
                e.data_devolucao.strftime("%d/%m/%Y %H:%M")
                if e.data_devolucao else ""
            ),
            "Status": e.status,
        }
        for e in emprestimos
    ])


st.title("📚 Sistema de Gerenciamento de Biblioteca")
st.caption(
    "Projeto acadêmico em Python com POO, persistência de dados, tratamento de erros, "
    "empréstimos, devoluções, consultas e relatórios."
)

menu = st.sidebar.radio(
    "Menu",
    [
        "Início",
        "Cadastrar livro",
        "Cadastrar usuário",
        "Empréstimo",
        "Devolução",
        "Consultar livros",
        "Relatórios",
    ],
)


if menu == "Início":
    resumo = service.resumo()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Livros catalogados", resumo["livros_catalogados"])
    c2.metric("Usuários cadastrados", resumo["usuarios_cadastrados"])
    c3.metric("Empréstimos ativos", resumo["emprestimos_ativos"])
    c4.metric("Cópias disponíveis", resumo["copias_disponiveis"])

    st.subheader("Livros disponíveis")
    df = livros_df(service.listar_livros(somente_disponiveis=True))
    if df.empty:
        st.info("Nenhum livro disponível no momento.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)


elif menu == "Cadastrar livro":
    st.header("Cadastro de livros")

    with st.form("form_livro", clear_on_submit=True):
        titulo = st.text_input("Título")
        autor = st.text_input("Autor")
        ano = st.number_input(
            "Ano de publicação",
            min_value=0,
            max_value=2100,
            value=2020,
            step=1,
        )
        copias = st.number_input(
            "Número de cópias",
            min_value=1,
            max_value=10000,
            value=1,
            step=1,
        )
        enviado = st.form_submit_button("Cadastrar")

    if enviado:
        try:
            livro = service.cadastrar_livro(
                titulo=titulo,
                autor=autor,
                ano_publicacao=int(ano),
                copias=int(copias),
            )
            st.success(f'Livro "{livro.titulo}" cadastrado com sucesso.')
        except BibliotecaErro as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Erro inesperado: {exc}")


elif menu == "Cadastrar usuário":
    st.header("Cadastro de usuários")

    with st.form("form_usuario", clear_on_submit=True):
        nome = st.text_input("Nome")
        identificacao = st.text_input("Número de identificação")
        contato = st.text_input("Contato")
        enviado = st.form_submit_button("Cadastrar")

    if enviado:
        try:
            usuario = service.cadastrar_usuario(nome, identificacao, contato)
            st.success(f'Usuário "{usuario.nome}" cadastrado com sucesso.')
        except BibliotecaErro as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Erro inesperado: {exc}")


elif menu == "Empréstimo":
    st.header("Empréstimo de livros")

    livros = service.listar_livros(somente_disponiveis=True)
    usuarios = service.listar_usuarios()

    if not livros:
        st.warning("Não há livros disponíveis para empréstimo.")
    elif not usuarios:
        st.warning("Cadastre ao menos um usuário antes de realizar empréstimos.")
    else:
        livro_map = {
            f"{l.id} — {l.titulo} ({l.copias_disponiveis} disponível/eis)": l.id
            for l in livros
        }
        usuario_map = {
            f"{u.id} — {u.nome} [{u.identificacao}]": u.id
            for u in usuarios
        }

        with st.form("form_emprestimo"):
            livro_sel = st.selectbox("Livro", list(livro_map))
            usuario_sel = st.selectbox("Usuário", list(usuario_map))
            enviado = st.form_submit_button("Confirmar empréstimo")

        if enviado:
            try:
                emp = service.emprestar_livro(
                    livro_map[livro_sel],
                    usuario_map[usuario_sel],
                )
                st.success(f"Empréstimo #{emp.id} realizado com sucesso.")
                st.rerun()
            except BibliotecaErro as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Erro inesperado: {exc}")


elif menu == "Devolução":
    st.header("Devolução de livros")
    ativos = service.listar_emprestimos(somente_ativos=True)

    if not ativos:
        st.info("Não há empréstimos ativos.")
    else:
        emp_map = {
            f"#{e.id} — {e.livro.titulo} — {e.usuario.nome}": e.id
            for e in ativos
        }

        with st.form("form_devolucao"):
            emp_sel = st.selectbox("Empréstimo", list(emp_map))
            enviado = st.form_submit_button("Confirmar devolução")

        if enviado:
            try:
                emp = service.devolver_livro(emp_map[emp_sel])
                st.success(f"Empréstimo #{emp.id} devolvido com sucesso.")
                st.rerun()
            except BibliotecaErro as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Erro inesperado: {exc}")


elif menu == "Consultar livros":
    st.header("Consulta de livros")
    col1, col2, col3 = st.columns(3)
    titulo = col1.text_input("Título contém")
    autor = col2.text_input("Autor contém")
    ano_txt = col3.text_input("Ano exato")

    ano = None
    if ano_txt.strip():
        if ano_txt.isdigit():
            ano = int(ano_txt)
        else:
            st.warning("O ano deve ser numérico.")

    livros = service.buscar_livros(
        titulo=titulo or None,
        autor=autor or None,
        ano=ano,
    )
    df = livros_df(livros)

    if df.empty:
        st.info("Nenhum livro encontrado.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)


elif menu == "Relatórios":
    st.header("Relatórios")

    aba1, aba2, aba3, aba4 = st.tabs(
        ["Livros disponíveis", "Livros emprestados", "Usuários", "Histórico"]
    )

    with aba1:
        df = livros_df(service.listar_livros(somente_disponiveis=True))
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Baixar CSV",
            df.to_csv(index=False).encode("utf-8-sig"),
            "livros_disponiveis.csv",
            "text/csv",
        )

    with aba2:
        df = emprestimos_df(service.listar_emprestimos(somente_ativos=True))
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Baixar CSV",
            df.to_csv(index=False).encode("utf-8-sig"),
            "livros_emprestados.csv",
            "text/csv",
        )

    with aba3:
        df = usuarios_df(service.listar_usuarios())
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Baixar CSV",
            df.to_csv(index=False).encode("utf-8-sig"),
            "usuarios.csv",
            "text/csv",
        )

    with aba4:
        df = emprestimos_df(service.listar_emprestimos(somente_ativos=False))
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Baixar CSV",
            df.to_csv(index=False).encode("utf-8-sig"),
            "historico_emprestimos.csv",
            "text/csv",
        )
