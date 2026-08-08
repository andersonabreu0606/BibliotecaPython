-- Modelo relacional do Sistema de Gerenciamento de Biblioteca
-- Compatível conceitualmente com PostgreSQL. O SQLAlchemy cria as tabelas automaticamente.

CREATE TABLE livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(150) NOT NULL,
    ano_publicacao INTEGER NOT NULL,
    copias_total INTEGER NOT NULL DEFAULT 1 CHECK (copias_total >= 0),
    copias_disponiveis INTEGER NOT NULL DEFAULT 1 CHECK (copias_disponiveis >= 0),
    CONSTRAINT ck_livros_disp_menor_total CHECK (copias_disponiveis <= copias_total)
);

CREATE INDEX ix_livros_titulo ON livros (titulo);
CREATE INDEX ix_livros_autor ON livros (autor);
CREATE INDEX ix_livros_ano_publicacao ON livros (ano_publicacao);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    identificacao VARCHAR(80) NOT NULL UNIQUE,
    contato VARCHAR(150) NOT NULL
);

CREATE TABLE emprestimos (
    id SERIAL PRIMARY KEY,
    livro_id INTEGER NOT NULL REFERENCES livros(id),
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    data_emprestimo TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_devolucao TIMESTAMP NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'EMPRESTADO'
);

CREATE INDEX ix_emprestimos_livro_id ON emprestimos (livro_id);
CREATE INDEX ix_emprestimos_usuario_id ON emprestimos (usuario_id);
