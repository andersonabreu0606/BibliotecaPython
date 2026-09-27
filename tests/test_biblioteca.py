import pytest

from database import Database
from services import BibliotecaService, BibliotecaErro, validar_credenciais


@pytest.fixture()
def service(tmp_path):
    db_path = tmp_path / "teste.db"
    db = Database(f"sqlite:///{db_path}")
    db.criar_tabelas()
    return BibliotecaService(db)


def test_validar_credenciais_padrao(monkeypatch):
    monkeypatch.setenv("BIBLIOTECA_LOGIN", "admin")
    monkeypatch.setenv("BIBLIOTECA_SENHA", "biblioteca123")

    assert validar_credenciais("admin", "biblioteca123") is True
    assert validar_credenciais("admin", "senha_errada") is False


def test_usuario_sistema_com_hash(service):
    usuario = service.criar_usuario_sistema("bibliotecario", "senhaSegura@123", "Bibliotecário", "operador")

    assert usuario.id is not None
    assert usuario.password_hash != "senhaSegura@123"
    assert service.autenticar_usuario("bibliotecario", "senhaSegura@123").username == "bibliotecario"

    with pytest.raises(BibliotecaErro):
        service.autenticar_usuario("bibliotecario", "senha-errada")


def test_cadastro_e_consulta(service):
    livro = service.cadastrar_livro("Livro Teste", "Autor X", 2024, 2)
    assert livro.id is not None

    encontrados = service.buscar_livros(titulo="teste")
    assert len(encontrados) == 1
    assert encontrados[0].titulo == "Livro Teste"


def test_usuario_identificacao_unica(service):
    service.cadastrar_usuario("Pessoa A", "ID001", "a@email.com")

    with pytest.raises(BibliotecaErro):
        service.cadastrar_usuario("Pessoa B", "ID001", "b@email.com")


def test_emprestimo_atualiza_copias(service):
    livro = service.cadastrar_livro("Livro A", "Autor", 2020, 1)
    usuario = service.cadastrar_usuario("Aluno", "A1", "x@email.com")

    service.emprestar_livro(livro.id, usuario.id)

    atualizado = service.buscar_livros(titulo="Livro A")[0]
    assert atualizado.copias_disponiveis == 0


def test_nao_empresta_sem_disponibilidade(service):
    livro = service.cadastrar_livro("Livro A", "Autor", 2020, 1)
    u1 = service.cadastrar_usuario("Aluno 1", "A1", "1@email.com")
    u2 = service.cadastrar_usuario("Aluno 2", "A2", "2@email.com")

    service.emprestar_livro(livro.id, u1.id)

    with pytest.raises(BibliotecaErro):
        service.emprestar_livro(livro.id, u2.id)


def test_devolucao_retorna_copia(service):
    livro = service.cadastrar_livro("Livro A", "Autor", 2020, 1)
    usuario = service.cadastrar_usuario("Aluno", "A1", "x@email.com")

    emp = service.emprestar_livro(livro.id, usuario.id)
    service.devolver_livro(emp.id)

    atualizado = service.buscar_livros(titulo="Livro A")[0]
    assert atualizado.copias_disponiveis == 1

    ativos = service.listar_emprestimos(somente_ativos=True)
    assert len(ativos) == 0


def test_impede_devolucao_duplicada(service):
    livro = service.cadastrar_livro("Livro A", "Autor", 2020, 1)
    usuario = service.cadastrar_usuario("Aluno", "A1", "x@email.com")

    emp = service.emprestar_livro(livro.id, usuario.id)
    service.devolver_livro(emp.id)

    with pytest.raises(BibliotecaErro):
        service.devolver_livro(emp.id)
