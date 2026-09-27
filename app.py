from __future__ import annotations

import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy.exc import OperationalError

from database import Database
from services import BibliotecaService, BibliotecaErro, obter_credenciais_acesso, validar_credenciais


def obter_database_url():
    try:
        if "DATABASE_URL" in st.secrets:
            return str(st.secrets["DATABASE_URL"]).strip()
    except Exception:
        pass
    return os.getenv("DATABASE_URL")


st.set_page_config(
    page_title="Biblioteca Digital",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


if "biblioteca_autenticado" not in st.session_state:
    st.session_state.biblioteca_autenticado = False
if "biblioteca_usuario" not in st.session_state:
    st.session_state.biblioteca_usuario = None
if "biblioteca_perfil" not in st.session_state:
    st.session_state.biblioteca_perfil = "operador"

try:
    db = Database(obter_database_url())
    db.testar_conexao()
    db.criar_tabelas()
    service = BibliotecaService(db)
    service.garantir_usuario_padrao()
except OperationalError:
    st.error(
        "Não foi possível conectar ao PostgreSQL. "
        "Revise a DATABASE_URL configurada nos Secrets do Streamlit."
    )
    st.info(
        "No Neon, copie novamente a Connection string. Para a primeira "
        "inicialização, prefira Direct connection e mantenha sslmode=require."
    )
    raise

if not st.session_state.biblioteca_autenticado:
    st.title("🔐 Acesso restrito")
    st.caption("Informe as credenciais para entrar no painel da biblioteca.")

    login_default, senha_default = obter_credenciais_acesso()
    with st.form("login_biblioteca"):
        usuario = st.text_input("Usuário", value=login_default, placeholder="admin")
        senha = st.text_input("Senha", type="password", value=senha_default, placeholder="Digite a senha")
        enviado = st.form_submit_button("Entrar", use_container_width=True)

    if enviado:
        try:
            usuario_logado = service.autenticar_usuario(usuario, senha)
            st.session_state.biblioteca_autenticado = True
            st.session_state.biblioteca_usuario = usuario_logado.username
            st.session_state.biblioteca_perfil = usuario_logado.perfil
            st.rerun()
        except BibliotecaErro as exc:
            st.error(str(exc))
    st.stop()

# -----------------------------------------------------------------------------
# Identidade visual
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        :root {
            --primary: #4f46e5;
            --primary-soft: #eef2ff;
            --ink: #111827;
            --muted: #6b7280;
            --border: #e5e7eb;
            --success: #059669;
            --warning: #d97706;
            --danger: #dc2626;
        }

        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid var(--border);
        }

        .tree-nav {
            margin-top: 0.5rem;
        }

        .tree-group {
            margin: 0.7rem 0 0.75rem 0;
            padding-left: 0.2rem;
        }

        .tree-label {
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: var(--muted);
            margin: 0.7rem 0 0.45rem 0.1rem;
        }

        .tree-submenu {
            margin-left: 0.8rem;
        }

        .brand-box {
            padding: 1rem 0.25rem 1.4rem 0.25rem;
        }

        .brand-title {
            font-size: 1.45rem;
            font-weight: 800;
            line-height: 1.1;
            color: var(--ink);
        }

        .brand-subtitle {
            margin-top: 0.35rem;
            color: var(--muted);
            font-size: 0.82rem;
        }

        .hero {
            border-radius: 22px;
            padding: 1.65rem 1.8rem;
            margin-bottom: 1.35rem;
            background: linear-gradient(120deg, #312e81 0%, #4f46e5 55%, #7c3aed 100%);
            color: white;
            box-shadow: 0 12px 30px rgba(79, 70, 229, 0.18);
        }

        .hero h1 {
            color: white;
            margin: 0;
            font-size: 2rem;
        }

        .hero p {
            color: rgba(255,255,255,.84);
            margin: .55rem 0 0 0;
            max-width: 860px;
        }

        .kpi-card {
            background: var(--primary-soft);
            border: 1px solid #dfe3ff;
            border-radius: 18px;
            padding: 1.15rem 1.2rem;
            min-height: 125px;
            box-shadow: 0 5px 14px rgba(17,24,39,.05);
        }

        .kpi-label {
            color: var(--muted);
            font-size: .78rem;
            text-transform: uppercase;
            letter-spacing: .055em;
            font-weight: 700;
        }

        .kpi-value {
            margin-top: .3rem;
            color: var(--ink);
            font-size: 2rem;
            line-height: 1.1;
            font-weight: 800;
        }

        .kpi-note {
            margin-top: .35rem;
            color: var(--muted);
            font-size: .82rem;
        }

        .section-title {
            margin-top: .25rem;
            margin-bottom: .2rem;
            font-size: 1.2rem;
            font-weight: 800;
            color: var(--ink);
        }

        .section-subtitle {
            color: var(--muted);
            font-size: .9rem;
            margin-bottom: .8rem;
        }

        div[data-testid="stForm"] {
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.1rem 1.2rem 1.25rem 1.2rem;
            background: rgba(255,255,255,.65);
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
        }

        .status-chip {
            display: inline-block;
            padding: .2rem .55rem;
            border-radius: 999px;
            font-size: .75rem;
            font-weight: 700;
        }

        .status-ok { background: #d1fae5; color: #065f46; }
        .status-warn { background: #fef3c7; color: #92400e; }

        .footer-note {
            margin-top: 2rem;
            color: var(--muted);
            font-size: .78rem;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def livros_df(livros):
    return pd.DataFrame([
        {
            "ID": l.id,
            "Título": l.titulo,
            "Autor": l.autor,
            "Ano": l.ano_publicacao,
            "Cópias totais": l.copias_total,
            "Disponíveis": l.copias_disponiveis,
            "Situação": "Disponível" if l.copias_disponiveis > 0 else "Indisponível",
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
            "ID": e.id,
            "Livro": e.livro.titulo,
            "Usuário": e.usuario.nome,
            "Data do empréstimo": e.data_emprestimo.strftime("%d/%m/%Y %H:%M"),
            "Data da devolução": (
                e.data_devolucao.strftime("%d/%m/%Y %H:%M")
                if e.data_devolucao else "—"
            ),
            "Status": e.status.title(),
        }
        for e in emprestimos
    ])


def render_hero(titulo: str, texto: str, icone: str = "📚"):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{icone} {titulo}</h1>
            <p>{texto}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi(label: str, valor: str | int, nota: str):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{valor}</div>
            <div class="kpi-note">{nota}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def titulo_secao(titulo: str, subtitulo: str = ""):
    st.markdown(f'<div class="section-title">{titulo}</div>', unsafe_allow_html=True)
    if subtitulo:
        st.markdown(f'<div class="section-subtitle">{subtitulo}</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand-box">
            <div class="brand-title">📚 Biblioteca Digital</div>
            <div class="brand-subtitle">Gestão inteligente do acervo e dos empréstimos</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(f"Usuário: {st.session_state.biblioteca_usuario or 'admin'}")
    st.caption(f"Perfil: {st.session_state.biblioteca_perfil}")

    if st.button("🚪 Sair"):
        st.session_state.biblioteca_autenticado = False
        st.session_state.biblioteca_usuario = None
        st.session_state.biblioteca_perfil = "operador"
        st.rerun()

    if "biblioteca_menu" not in st.session_state:
        st.session_state.biblioteca_menu = "Dashboard"

    def nav_button(label: str, *, disabled: bool = False):
        selected = st.session_state.biblioteca_menu == label
        clicked = st.sidebar.button(
            label,
            key=f"nav_{label}",
            type="primary" if selected else "secondary",
            use_container_width=True,
            disabled=disabled,
        )
        if clicked:
            st.session_state.biblioteca_menu = label
        return clicked

    nav_button("Dashboard")

    livros_expanded = st.session_state.biblioteca_menu in {"Cadastrar", "Consultar"}
    with st.sidebar.expander("Livros", expanded=livros_expanded):
        nav_button("Cadastrar")
        nav_button("Consultar")

    gestao_expanded = st.session_state.biblioteca_menu in {"Emprestar Livro", "Devolução", "Relatórios"}
    with st.sidebar.expander("Gestão", expanded=gestao_expanded):
        nav_button("Emprestar Livro")
        nav_button("Devolução")
        nav_button("Relatórios")

    is_admin = st.session_state.biblioteca_perfil == "admin"
    admin_expanded = st.session_state.biblioteca_menu == "Usuários do Sistema"
    with st.sidebar.expander("Administração", expanded=admin_expanded):
        nav_button("Usuários do Sistema", disabled=not is_admin)

    menu = st.session_state.biblioteca_menu
    if st.session_state.biblioteca_perfil != "admin" and menu == "Usuários do Sistema":
        menu = "Dashboard"
        st.session_state.biblioteca_menu = menu

    st.divider()
    resumo_sidebar = service.resumo()
    st.caption("Situação do acervo")
    st.progress(
        min(float(resumo_sidebar["taxa_ocupacao"]) / 100, 1.0),
        text=f'{resumo_sidebar["taxa_ocupacao"]:.1f}% das cópias emprestadas',
    )
    st.caption(f'Atualizado em {datetime.now().strftime("%d/%m/%Y %H:%M")}')


# -----------------------------------------------------------------------------
# Dashboard
# -----------------------------------------------------------------------------
if menu == "Usuários do Sistema":
    if st.session_state.biblioteca_perfil != "admin":
        st.warning("Acesso restrito somente para administradores.")
        st.stop()

    render_hero(
        "Usuários do sistema",
        "Gerencie os acessos administrativos com login e senha protegidos por hash seguro.",
        "👥",
    )

    usuarios_sistema = service.listar_usuarios_sistema()
    if usuarios_sistema:
        st.dataframe(
            pd.DataFrame([
                {
                    "Usuário": u.username,
                    "Nome": u.nome,
                    "Perfil": u.perfil.title(),
                    "Ativo": "Sim" if u.ativo else "Não",
                }
                for u in usuarios_sistema
            ]),
            use_container_width=True,
            hide_index=True,
        )

    with st.form("form_usuario_sistema", clear_on_submit=True):
        username = st.text_input("Usuário", placeholder="bibliotecario")
        nome = st.text_input("Nome completo", placeholder="Maria da Silva")
        perfil = st.selectbox("Perfil", ["operador", "admin"])
        senha = st.text_input("Senha", type="password", placeholder="Digite uma senha forte")
        enviado = st.form_submit_button("➕ Criar usuário administrativo", use_container_width=True)

    if enviado:
        try:
            usuario = service.criar_usuario_sistema(username, senha, nome, perfil)
            st.success(f'Usuário administrativo “{usuario.username}” criado com sucesso.')
            st.rerun()
        except BibliotecaErro as exc:
            st.error(str(exc))

elif menu == "Dashboard":
    render_hero(
        "Painel da Biblioteca",
        "Uma visão consolidada do acervo, circulação de livros, utilizadores e atividade recente.",
        "📚",
    )

    resumo = service.resumo()
    cols = st.columns(5)
    with cols[0]:
        render_kpi("Títulos catalogados", resumo["livros_catalogados"], "Obras registadas no catálogo")
    with cols[1]:
        render_kpi("Utilizadores", resumo["usuarios_cadastrados"], "Leitores cadastrados")
    with cols[2]:
        render_kpi("Empréstimos ativos", resumo["emprestimos_ativos"], "Livros atualmente em circulação")
    with cols[3]:
        render_kpi("Cópias disponíveis", resumo["copias_disponiveis"], f'De {resumo["copias_total"]} cópias no acervo')
    with cols[4]:
        render_kpi("Ocupação", f'{resumo["taxa_ocupacao"]:.1f}%', "Percentual de cópias emprestadas")

    st.write("")
    left, right = st.columns([1.05, 1.95], gap="large")

    with left:
        titulo_secao("Situação dos empréstimos", "Comparativo entre empréstimos em aberto e já devolvidos.")
        dados_status = pd.DataFrame(service.emprestimos_por_status())
        if dados_status.empty:
            st.info("Ainda não existem empréstimos registrados.")
        else:
            fig = px.pie(
                dados_status,
                names="status",
                values="quantidade",
                hole=.58,
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=350,
                legend_title_text="",
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with right:
        titulo_secao("Livros mais procurados", "Ranking dos títulos com maior número de empréstimos registrados.")
        top = pd.DataFrame(service.top_livros(10))
        if top.empty:
            st.info("Ainda não existem dados suficientes para o ranking.")
        else:
            top = top.sort_values("emprestimos", ascending=True)
            fig = px.bar(
                top,
                x="emprestimos",
                y="livro",
                orientation="h",
                labels={"emprestimos": "Empréstimos", "livro": "Título"},
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=350,
                yaxis_title="",
                xaxis_title="Quantidade de empréstimos",
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    left2, right2 = st.columns([1.5, 1], gap="large")

    with left2:
        titulo_secao("Evolução mensal", "Quantidade de empréstimos realizados nos últimos períodos disponíveis.")
        mensal = pd.DataFrame(service.emprestimos_por_mes(12))
        if mensal.empty:
            st.info("Sem histórico temporal para apresentar.")
        else:
            mensal["Período"] = pd.to_datetime(mensal["mes"] + "-01").dt.strftime("%m/%Y")
            fig = px.line(
                mensal,
                x="Período",
                y="emprestimos",
                markers=True,
                labels={"emprestimos": "Empréstimos"},
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=330,
                xaxis_title="",
                yaxis_title="Empréstimos",
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with right2:
        titulo_secao("Indicadores operacionais", "Alertas rápidos para apoiar o acompanhamento do acervo.")
        indisponiveis = int(resumo["titulos_indisponiveis"])
        if indisponiveis:
            st.warning(f"⚠️ {indisponiveis} título(s) sem nenhuma cópia disponível.")
        else:
            st.success("✅ Todos os títulos possuem ao menos uma cópia disponível.")

        st.metric("Empréstimos devolvidos", resumo["emprestimos_devolvidos"])
        st.metric("Total de cópias", resumo["copias_total"])
        st.metric("Cópias em circulação", int(resumo["copias_total"]) - int(resumo["copias_disponiveis"]))

    titulo_secao("Atividade recente", "Últimos movimentos registrados no sistema.")
    recentes = emprestimos_df(service.emprestimos_recentes(8))
    if recentes.empty:
        st.info("Ainda não existem movimentos registrados.")
    else:
        st.dataframe(
            recentes,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("#", width="small"),
                "Status": st.column_config.TextColumn("Status", width="small"),
            },
        )


elif menu == "Cadastrar":
    render_hero(
        "Cadastro de livro",
        "Inclua um novo título no acervo e defina a quantidade inicial de cópias disponíveis.",
        "📘",
    )

    col_form, col_help = st.columns([1.5, 1], gap="large")
    with col_form:
        with st.form("form_livro", clear_on_submit=True):
            titulo = st.text_input("Título", placeholder="Ex.: Engenharia de Dados com Python")
            autor = st.text_input("Autor", placeholder="Ex.: Fernanda Lima")
            c1, c2 = st.columns(2)
            ano = c1.number_input("Ano de publicação", min_value=0, max_value=2100, value=2024, step=1)
            copias = c2.number_input("Número de cópias", min_value=1, max_value=10000, value=1, step=1)
            enviado = st.form_submit_button("➕ Cadastrar livro", use_container_width=True)

        if enviado:
            try:
                livro = service.cadastrar_livro(titulo, autor, int(ano), int(copias))
                st.success(f'Livro “{livro.titulo}” cadastrado com sucesso.')
            except BibliotecaErro as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Erro inesperado: {exc}")

    with col_help:
        titulo_secao("Boas práticas", "Informações úteis para manter o catálogo consistente.")
        st.info("💡 Utilize o título completo da obra e o nome do autor conforme a ficha catalográfica.")
        st.info("📦 O número de cópias representa o estoque físico inicial do título.")
        st.info("🔎 O livro ficará imediatamente disponível nas consultas e operações de empréstimo.")


elif menu == "👤 Cadastrar usuário":
    render_hero(
        "Cadastro de usuário",
        "Registe leitores da biblioteca com uma identificação única e um canal de contato.",
        "👤",
    )

    col_form, col_help = st.columns([1.5, 1], gap="large")
    with col_form:
        with st.form("form_usuario", clear_on_submit=True):
            nome = st.text_input("Nome completo", placeholder="Ex.: Ana Oliveira")
            identificacao = st.text_input("Número de identificação", placeholder="Ex.: USR00125")
            contato = st.text_input("Contato", placeholder="Ex.: ana@email.com ou +351 9xx xxx xxx")
            enviado = st.form_submit_button("👤 Cadastrar usuário", use_container_width=True)

        if enviado:
            try:
                usuario = service.cadastrar_usuario(nome, identificacao, contato)
                st.success(f'Usuário “{usuario.nome}” cadastrado com sucesso.')
            except BibliotecaErro as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Erro inesperado: {exc}")

    with col_help:
        titulo_secao("Identificação do leitor")
        st.info("🪪 A identificação é única e impede cadastros duplicados.")
        st.info("📧 O contato pode ser um e-mail ou telefone utilizado pela biblioteca.")


elif menu == "Emprestar Livro":
    render_hero(
        "Novo empréstimo",
        "Selecione um título disponível e o usuário responsável pelo empréstimo.",
        "🔄",
    )

    livros = service.listar_livros(somente_disponiveis=True)
    usuarios = service.listar_usuarios()

    if not livros:
        st.warning("Não há livros disponíveis para empréstimo.")
    elif not usuarios:
        st.warning("Cadastre ao menos um usuário antes de realizar empréstimos.")
    else:
        livro_map = {
            f"{l.titulo} — {l.autor} | {l.copias_disponiveis} disponível(eis)": l.id
            for l in livros
        }
        usuario_map = {
            f"{u.nome} — {u.identificacao}": u.id
            for u in usuarios
        }

        col_form, col_info = st.columns([1.55, 1], gap="large")
        with col_form:
            with st.form("form_emprestimo"):
                livro_sel = st.selectbox("Livro", list(livro_map))
                usuario_sel = st.selectbox("Usuário", list(usuario_map))
                enviado = st.form_submit_button("✅ Confirmar empréstimo", use_container_width=True)

            if enviado:
                try:
                    emp = service.emprestar_livro(livro_map[livro_sel], usuario_map[usuario_sel])
                    st.success(f"Empréstimo #{emp.id} realizado com sucesso.")
                    st.rerun()
                except BibliotecaErro as exc:
                    st.error(str(exc))
                except Exception as exc:
                    st.error(f"Erro inesperado: {exc}")

        with col_info:
            st.metric("Títulos disponíveis", len(livros))
            st.metric("Usuários cadastrados", len(usuarios))
            st.info("O sistema reduz automaticamente a quantidade disponível do livro após a confirmação.")


elif menu == "Devolução":
    render_hero(
        "Devolução de livro",
        "Finalize um empréstimo ativo e devolva automaticamente a cópia ao estoque disponível.",
        "↩️",
    )
    ativos = service.listar_emprestimos(somente_ativos=True)

    if not ativos:
        st.success("Não há empréstimos ativos no momento.")
    else:
        emp_map = {
            f"#{e.id} — {e.livro.titulo} — {e.usuario.nome}": e.id
            for e in ativos
        }
        with st.form("form_devolucao"):
            emp_sel = st.selectbox("Empréstimo ativo", list(emp_map))
            enviado = st.form_submit_button("↩️ Confirmar devolução", use_container_width=True)

        if enviado:
            try:
                emp = service.devolver_livro(emp_map[emp_sel])
                st.success(f"Empréstimo #{emp.id} devolvido com sucesso.")
                st.rerun()
            except BibliotecaErro as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Erro inesperado: {exc}")

        titulo_secao("Empréstimos aguardando devolução")
        st.dataframe(emprestimos_df(ativos), use_container_width=True, hide_index=True)


elif menu == "Consultar":
    render_hero(
        "Consulta ao acervo",
        "Pesquise títulos por nome, autor ou ano de publicação e veja a disponibilidade em tempo real.",
        "🔎",
    )

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        titulo = col1.text_input("Título contém", placeholder="Digite parte do título")
        autor = col2.text_input("Autor contém", placeholder="Digite parte do nome")
        ano_txt = col3.text_input("Ano exato", placeholder="Ex.: 2024")

    ano = None
    if ano_txt.strip():
        if ano_txt.isdigit():
            ano = int(ano_txt)
        else:
            st.warning("O ano deve ser numérico.")

    livros = service.buscar_livros(titulo=titulo or None, autor=autor or None, ano=ano)
    df = livros_df(livros)

    titulo_secao(f"Resultado da pesquisa ({len(df)} título(s))")
    if df.empty:
        st.info("Nenhum livro encontrado.")
    else:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("#", width="small"),
                "Ano": st.column_config.NumberColumn("Ano", format="%d"),
                "Situação": st.column_config.TextColumn("Situação", width="small"),
            },
        )


elif menu == "Relatórios":
    render_hero(
        "Relatórios gerenciais",
        "Acompanhe o catálogo, usuários e histórico de circulação, com opção de exportação em CSV.",
        "📊",
    )

    aba1, aba2, aba3, aba4, aba5 = st.tabs(
        ["📚 Disponíveis", "🔄 Emprestados", "👥 Usuários", "🕓 Histórico", "✍️ Autores"]
    )

    with aba1:
        df = livros_df(service.listar_livros(somente_disponiveis=True))
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Baixar CSV de livros disponíveis",
            df.to_csv(index=False).encode("utf-8-sig"),
            "livros_disponiveis.csv",
            "text/csv",
        )

    with aba2:
        df = emprestimos_df(service.listar_emprestimos(somente_ativos=True))
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Baixar CSV de empréstimos ativos",
            df.to_csv(index=False).encode("utf-8-sig"),
            "livros_emprestados.csv",
            "text/csv",
        )

    with aba3:
        df = usuarios_df(service.listar_usuarios())
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Baixar CSV de usuários",
            df.to_csv(index=False).encode("utf-8-sig"),
            "usuarios.csv",
            "text/csv",
        )

    with aba4:
        df = emprestimos_df(service.listar_emprestimos(somente_ativos=False))
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Baixar CSV do histórico",
            df.to_csv(index=False).encode("utf-8-sig"),
            "historico_emprestimos.csv",
            "text/csv",
        )

    with aba5:
        autores = pd.DataFrame(service.top_autores(12))
        if autores.empty:
            st.info("Ainda não existem empréstimos suficientes para gerar o ranking de autores.")
        else:
            fig = px.bar(
                autores.sort_values("emprestimos"),
                x="emprestimos",
                y="autor",
                orientation="h",
                labels={"emprestimos": "Empréstimos", "autor": "Autor"},
            )
            fig.update_layout(height=430, yaxis_title="", xaxis_title="Quantidade de empréstimos")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


st.markdown(
    '<div class="footer-note">Projeto Integrado • Sistema de Gerenciamento de Biblioteca • Python + Streamlit + SQLAlchemy</div>',
    unsafe_allow_html=True,
)
