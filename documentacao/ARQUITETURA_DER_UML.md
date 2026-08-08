# DER e UML finais

O sistema possui três entidades principais: **Livro**, **Usuário** e **Empréstimo**.

- Um livro pode participar de zero ou muitos empréstimos.
- Um usuário pode realizar zero ou muitos empréstimos.
- Cada empréstimo pertence exatamente a um livro e a um usuário.
- `livro_id` e `usuario_id` são chaves estrangeiras da tabela `emprestimos`.
- O estoque disponível é mantido em `copias_disponiveis` e atualizado pelas operações de empréstimo/devolução.

O diagrama UML também evidencia a camada de serviço (`BibliotecaService`) e a infraestrutura de persistência (`Database`).
