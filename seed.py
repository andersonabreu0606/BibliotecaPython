from database import Database
from services import BibliotecaService, BibliotecaErro

db = Database()
db.criar_tabelas()
service = BibliotecaService(db)

livros = [
    ("Dom Casmurro", "Machado de Assis", 1899, 3),
    ("1984", "George Orwell", 1949, 2),
    ("O Pequeno Príncipe", "Antoine de Saint-Exupéry", 1943, 4),
]

usuarios = [
    ("Ana Souza", "USR001", "ana@email.com"),
    ("Carlos Lima", "USR002", "carlos@email.com"),
    ("Mariana Alves", "USR003", "+351 910 000 003"),
]

for item in livros:
    try:
        service.cadastrar_livro(*item)
    except BibliotecaErro:
        pass

for item in usuarios:
    try:
        service.cadastrar_usuario(*item)
    except BibliotecaErro:
        pass

print("Dados de exemplo inseridos.")
