from database import Database
from services import BibliotecaService, BibliotecaErro


db = Database()
db.criar_tabelas()
service = BibliotecaService(db)


def cabecalho(texto: str) -> None:
    print("\n" + "=" * 60)
    print(texto)
    print("=" * 60)


def cadastrar_livro() -> None:
    cabecalho("CADASTRO DE LIVRO")
    titulo = input("Título: ")
    autor = input("Autor: ")
    ano = int(input("Ano de publicação: "))
    copias = int(input("Número de cópias: "))
    livro = service.cadastrar_livro(titulo, autor, ano, copias)
    print(f"Livro cadastrado com ID {livro.id}.")


def cadastrar_usuario() -> None:
    cabecalho("CADASTRO DE USUÁRIO")
    nome = input("Nome: ")
    identificacao = input("Número de identificação: ")
    contato = input("Contato: ")
    usuario = service.cadastrar_usuario(nome, identificacao, contato)
    print(f"Usuário cadastrado com ID {usuario.id}.")


def emprestar() -> None:
    cabecalho("EMPRÉSTIMO")
    for l in service.listar_livros(somente_disponiveis=True):
        print(f"{l.id}: {l.titulo} | disponíveis: {l.copias_disponiveis}")
    livro_id = int(input("ID do livro: "))

    for u in service.listar_usuarios():
        print(f"{u.id}: {u.nome} | {u.identificacao}")
    usuario_id = int(input("ID do usuário: "))

    emp = service.emprestar_livro(livro_id, usuario_id)
    print(f"Empréstimo #{emp.id} realizado.")


def devolver() -> None:
    cabecalho("DEVOLUÇÃO")
    ativos = service.listar_emprestimos(somente_ativos=True)
    for e in ativos:
        print(f"{e.id}: {e.livro.titulo} -> {e.usuario.nome}")

    emprestimo_id = int(input("ID do empréstimo: "))
    emp = service.devolver_livro(emprestimo_id)
    print(f"Empréstimo #{emp.id} devolvido.")


def consultar() -> None:
    cabecalho("CONSULTA")
    titulo = input("Título contém (Enter para ignorar): ").strip() or None
    autor = input("Autor contém (Enter para ignorar): ").strip() or None
    ano_txt = input("Ano exato (Enter para ignorar): ").strip()
    ano = int(ano_txt) if ano_txt else None

    livros = service.buscar_livros(titulo=titulo, autor=autor, ano=ano)
    if not livros:
        print("Nenhum livro encontrado.")
        return

    for l in livros:
        print(
            f"{l.id}: {l.titulo} | {l.autor} | {l.ano_publicacao} | "
            f"Disponíveis: {l.copias_disponiveis}/{l.copias_total}"
        )


def relatorios() -> None:
    cabecalho("RELATÓRIOS")

    print("\nLivros disponíveis:")
    for l in service.listar_livros(somente_disponiveis=True):
        print(f"- {l.titulo} ({l.copias_disponiveis} disponível/eis)")

    print("\nEmpréstimos ativos:")
    for e in service.listar_emprestimos(somente_ativos=True):
        print(f"- #{e.id} {e.livro.titulo} -> {e.usuario.nome}")

    print("\nUsuários cadastrados:")
    for u in service.listar_usuarios():
        print(f"- {u.nome} [{u.identificacao}] - {u.contato}")


def menu() -> None:
    while True:
        cabecalho("SISTEMA DE GERENCIAMENTO DE BIBLIOTECA")
        print("1 - Cadastrar livro")
        print("2 - Cadastrar usuário")
        print("3 - Empréstimo")
        print("4 - Devolução")
        print("5 - Consultar livros")
        print("6 - Relatórios")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                cadastrar_livro()
            elif opcao == "2":
                cadastrar_usuario()
            elif opcao == "3":
                emprestar()
            elif opcao == "4":
                devolver()
            elif opcao == "5":
                consultar()
            elif opcao == "6":
                relatorios()
            elif opcao == "0":
                print("Sistema encerrado.")
                break
            else:
                print("Opção inválida.")
        except BibliotecaErro as exc:
            print(f"ERRO: {exc}")
        except ValueError:
            print("ERRO: informe valores numéricos quando solicitado.")
        except Exception as exc:
            print(f"ERRO INESPERADO: {exc}")

        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    menu()
