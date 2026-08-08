# Sistema de Gerenciamento de Biblioteca

Projeto acadêmico em Python desenvolvido para atender aos requisitos de:

- cadastro de livros;
- cadastro de usuários;
- empréstimo com verificação de disponibilidade;
- devolução com atualização das cópias;
- pesquisa por título, autor e ano;
- relatórios;
- programação orientada a objetos;
- tratamento de erros e exceções;
- interface de console;
- interface web opcional;
- modularização;
- testes automatizados.

## Estrutura

- `models.py` — classes Livro, Usuario e Emprestimo.
- `database.py` — configuração do banco.
- `services.py` — regras de negócio.
- `console.py` — menu de console solicitado no enunciado.
- `app.py` — interface web em Streamlit.
- `seed.py` — dados de demonstração.
- `tests/` — testes automatizados.

## Execução local

### 1. Criar ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Inserir dados de exemplo (opcional)

```bash
python seed.py
```

### 4. Executar a versão de console

```bash
python console.py
```

### 5. Executar a versão web

```bash
streamlit run app.py
```

## Banco de dados

Por padrão, o projeto usa SQLite (`biblioteca.db`).

Para publicar na internet com banco PostgreSQL, defina a variável:

```text
DATABASE_URL=postgresql://usuario:senha@servidor/banco?sslmode=require
```

No Streamlit Community Cloud, coloque a variável em **App > Settings > Secrets**:

```toml
DATABASE_URL = "postgresql://usuario:senha@servidor/banco?sslmode=require"
```

## Testes

```bash
pytest -q
```

## Sugestão de hospedagem

Uma combinação simples para projeto acadêmico é:

- aplicação: Streamlit Community Cloud;
- banco persistente: Neon PostgreSQL.

O código pode ficar em um repositório GitHub e o Streamlit faz o deploy diretamente dele.

## Arquivos adicionais da entrega final

- `schema_postgresql.sql` — modelo SQL relacional para PostgreSQL;
- `DEPLOY.md` — roteiro completo de publicação;
- `gerar_qr.py` — gera o QR Code após a definição da URL pública;
- `.streamlit/secrets.toml.example` — exemplo seguro de configuração;
- `.github/workflows/tests.yml` — execução automática dos testes no GitHub;
- `docs/figuras/` — diagramas e representações utilizadas no relatório acadêmico.

## Resultado dos testes da versão entregue

A suíte automatizada possui 6 testes. Na versão preparada para entrega:

```text
6 passed
```

## Observação sobre a publicação

O projeto está pronto para deploy, mas a criação do repositório, do banco e do aplicativo em nuvem exige autenticação nas contas do titular. O arquivo `DEPLOY.md` contém o passo a passo e os parâmetros necessários.
