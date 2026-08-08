-- MASSA DE TESTE - SISTEMA DE GERENCIAMENTO DE BIBLIOTECA
-- PostgreSQL / Neon
-- Gerado para as tabelas: livros, usuarios e emprestimos

-- ATENÇÃO: o bloco abaixo APAGA os dados existentes.
-- Remova/comente o TRUNCATE caso queira acrescentar os dados aos já existentes.
BEGIN;

TRUNCATE TABLE emprestimos, livros, usuarios RESTART IDENTITY CASCADE;

-- ============================================================
-- 1. LIVROS
-- ============================================================
INSERT INTO livros (id, titulo, autor, ano_publicacao, copias_total, copias_disponiveis) VALUES
(1, 'Dom Casmurro', 'Machado de Assis', 1899, 6, 5),
(2, 'Memórias Póstumas de Brás Cubas', 'Machado de Assis', 1881, 5, 5),
(3, 'O Alienista', 'Machado de Assis', 1882, 3, 3),
(4, 'Grande Sertão: Veredas', 'João Guimarães Rosa', 1956, 5, 4),
(5, 'Capitães da Areia', 'Jorge Amado', 1937, 3, 2),
(6, 'A Hora da Estrela', 'Clarice Lispector', 1977, 4, 4),
(7, 'Vidas Secas', 'Graciliano Ramos', 1938, 5, 2),
(8, 'O Cortiço', 'Aluísio Azevedo', 1890, 5, 1),
(9, 'Iracema', 'José de Alencar', 1865, 2, 2),
(10, 'Macunaíma', 'Mário de Andrade', 1928, 5, 4),
(11, '1984', 'George Orwell', 1949, 6, 6),
(12, 'A Revolução dos Bichos', 'George Orwell', 1945, 2, 2),
(13, 'Admirável Mundo Novo', 'Aldous Huxley', 1932, 2, 2),
(14, 'Fahrenheit 451', 'Ray Bradbury', 1953, 6, 5),
(15, 'O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 1943, 2, 1),
(16, 'O Senhor dos Anéis', 'J. R. R. Tolkien', 1954, 2, 1),
(17, 'O Hobbit', 'J. R. R. Tolkien', 1937, 3, 3),
(18, 'Harry Potter e a Pedra Filosofal', 'J. K. Rowling', 1997, 3, 3),
(19, 'Cem Anos de Solidão', 'Gabriel García Márquez', 1967, 5, 5),
(20, 'O Nome da Rosa', 'Umberto Eco', 1980, 5, 5),
(21, 'Python Fluente', 'Luciano Ramalho', 2015, 5, 5),
(22, 'Introdução à Ciência de Dados', 'Carlos Silva', 2022, 3, 3),
(23, 'Fundamentos de Banco de Dados', 'Ana Oliveira', 2020, 5, 5),
(24, 'Arquitetura de Dados Moderna', 'Ricardo Martins', 2024, 2, 2),
(25, 'Machine Learning na Prática', 'Mariana Costa', 2023, 3, 3),
(26, 'Inteligência Artificial Aplicada', 'Paulo Ferreira', 2025, 5, 3),
(27, 'Engenharia de Dados com Python', 'Fernanda Lima', 2024, 2, 2),
(28, 'SQL para Análise de Dados', 'João Santos', 2021, 5, 4),
(29, 'NoSQL: Conceitos e Aplicações', 'Juliana Rocha', 2022, 4, 4),
(30, 'Big Data e Analytics', 'Pedro Almeida', 2020, 5, 4),
(31, 'Redes Neurais Artificiais', 'Helena Souza', 2023, 4, 3),
(32, 'Deep Learning Essencial', 'Gabriel Costa', 2024, 5, 4),
(33, 'Estatística para Ciência de Dados', 'Renata Alves', 2021, 6, 3),
(34, 'Business Intelligence', 'Carlos Martins', 2019, 5, 3),
(35, 'Cloud Computing', 'Eduardo Ferreira', 2022, 3, 2),
(36, 'Segurança da Informação', 'Tatiana Rocha', 2023, 3, 3),
(37, 'Governança de Dados', 'Mariana Lima', 2024, 4, 4),
(38, 'Data Warehouse', 'Paulo Costa', 2018, 3, 2),
(39, 'ETL e Integração de Dados', 'Fernanda Santos', 2020, 4, 1),
(40, 'Visualização de Dados', 'Ana Martins', 2021, 6, 6);

-- ============================================================
-- 2. USUÁRIOS
-- ============================================================
INSERT INTO usuarios (id, nome, identificacao, contato) VALUES
(1, 'Ana Oliveira', 'USR00001', 'usuario00001@email.com'),
(2, 'Bruno Rodrigues', 'USR00002', 'usuario00002@email.com'),
(3, 'Carlos Rocha', 'USR00003', 'usuario00003@email.com'),
(4, 'Daniel Carvalho', 'USR00004', 'usuario00004@email.com'),
(5, 'Eduardo Silva', 'USR00005', 'usuario00005@email.com'),
(6, 'Fernanda Oliveira', 'USR00006', 'usuario00006@email.com'),
(7, 'Gabriel Rodrigues', 'USR00007', 'usuario00007@email.com'),
(8, 'Helena Rocha', 'USR00008', 'usuario00008@email.com'),
(9, 'Isabela Carvalho', 'USR00009', 'usuario00009@email.com'),
(10, 'João Silva', 'USR00010', 'usuario00010@email.com'),
(11, 'Karina Oliveira', 'USR00011', 'usuario00011@email.com'),
(12, 'Lucas Rodrigues', 'USR00012', 'usuario00012@email.com'),
(13, 'Mariana Rocha', 'USR00013', 'usuario00013@email.com'),
(14, 'Nicolas Carvalho', 'USR00014', 'usuario00014@email.com'),
(15, 'Olivia Silva', 'USR00015', 'usuario00015@email.com'),
(16, 'Paulo Oliveira', 'USR00016', 'usuario00016@email.com'),
(17, 'Renata Rodrigues', 'USR00017', 'usuario00017@email.com'),
(18, 'Sergio Rocha', 'USR00018', 'usuario00018@email.com'),
(19, 'Tatiana Carvalho', 'USR00019', 'usuario00019@email.com'),
(20, 'Victor Silva', 'USR00020', 'usuario00020@email.com'),
(21, 'Beatriz Oliveira', 'USR00021', 'usuario00021@email.com'),
(22, 'Rafael Rodrigues', 'USR00022', 'usuario00022@email.com'),
(23, 'Juliana Rocha', 'USR00023', 'usuario00023@email.com'),
(24, 'Pedro Carvalho', 'USR00024', 'usuario00024@email.com'),
(25, 'Camila Silva', 'USR00025', 'usuario00025@email.com');

-- ============================================================
-- 3. EMPRÉSTIMOS
-- ============================================================
INSERT INTO emprestimos (id, livro_id, usuario_id, data_emprestimo, data_devolucao, status) VALUES
(1, 8, 1, '2026-07-06 13:00:00', '2026-07-15 13:00:00', 'DEVOLVIDO'),
(2, 9, 24, '2026-06-14 11:00:00', '2026-07-04 11:00:00', 'DEVOLVIDO'),
(3, 28, 2, '2026-06-04 11:00:00', '2026-06-12 11:00:00', 'DEVOLVIDO'),
(4, 15, 17, '2026-06-04 13:00:00', '2026-06-23 13:00:00', 'DEVOLVIDO'),
(5, 27, 8, '2026-07-28 14:00:00', '2026-07-30 14:00:00', 'DEVOLVIDO'),
(6, 11, 23, '2026-07-25 15:00:00', '2026-08-04 15:00:00', 'DEVOLVIDO'),
(7, 10, 7, '2026-07-14 11:00:00', '2026-07-18 11:00:00', 'DEVOLVIDO'),
(8, 25, 4, '2026-07-16 15:00:00', '2026-07-26 15:00:00', 'DEVOLVIDO'),
(9, 3, 24, '2026-07-29 11:00:00', '2026-08-12 11:00:00', 'DEVOLVIDO'),
(10, 6, 18, '2026-07-08 15:00:00', '2026-07-28 15:00:00', 'DEVOLVIDO'),
(11, 13, 23, '2026-06-09 10:00:00', '2026-06-18 10:00:00', 'DEVOLVIDO'),
(12, 19, 3, '2026-06-30 11:00:00', '2026-07-14 11:00:00', 'DEVOLVIDO'),
(13, 18, 15, '2026-07-17 12:00:00', '2026-07-30 12:00:00', 'DEVOLVIDO'),
(14, 23, 7, '2026-07-05 11:00:00', '2026-07-12 11:00:00', 'DEVOLVIDO'),
(15, 35, 24, '2026-07-02 12:00:00', '2026-07-18 12:00:00', 'DEVOLVIDO'),
(16, 25, 9, '2026-06-29 15:00:00', '2026-07-02 15:00:00', 'DEVOLVIDO'),
(17, 15, 2, '2026-07-11 16:00:00', '2026-07-21 16:00:00', 'DEVOLVIDO'),
(18, 5, 7, '2026-07-11 13:00:00', '2026-07-28 13:00:00', 'DEVOLVIDO'),
(19, 26, 21, '2026-07-29 12:00:00', '2026-08-08 12:00:00', 'DEVOLVIDO'),
(20, 9, 8, '2026-07-04 16:00:00', '2026-07-24 16:00:00', 'DEVOLVIDO'),
(21, 26, 12, '2026-06-29 12:00:00', NULL, 'EMPRESTADO'),
(22, 33, 16, '2026-06-12 10:00:00', NULL, 'EMPRESTADO'),
(23, 8, 5, '2026-06-21 16:00:00', NULL, 'EMPRESTADO'),
(24, 39, 3, '2026-07-20 16:00:00', NULL, 'EMPRESTADO'),
(25, 39, 15, '2026-07-03 10:00:00', NULL, 'EMPRESTADO'),
(26, 8, 22, '2026-07-05 15:00:00', NULL, 'EMPRESTADO'),
(27, 8, 10, '2026-07-26 12:00:00', NULL, 'EMPRESTADO'),
(28, 30, 1, '2026-07-04 12:00:00', NULL, 'EMPRESTADO'),
(29, 33, 4, '2026-07-09 13:00:00', NULL, 'EMPRESTADO'),
(30, 10, 12, '2026-06-21 10:00:00', NULL, 'EMPRESTADO'),
(31, 39, 11, '2026-08-02 10:00:00', NULL, 'EMPRESTADO'),
(32, 8, 12, '2026-07-10 13:00:00', NULL, 'EMPRESTADO'),
(33, 4, 8, '2026-06-11 11:00:00', NULL, 'EMPRESTADO'),
(34, 32, 3, '2026-06-17 12:00:00', NULL, 'EMPRESTADO'),
(35, 31, 18, '2026-06-22 14:00:00', NULL, 'EMPRESTADO'),
(36, 34, 20, '2026-07-25 13:00:00', NULL, 'EMPRESTADO'),
(37, 35, 25, '2026-06-26 14:00:00', NULL, 'EMPRESTADO'),
(38, 26, 22, '2026-07-18 17:00:00', NULL, 'EMPRESTADO'),
(39, 34, 15, '2026-06-16 13:00:00', NULL, 'EMPRESTADO'),
(40, 15, 3, '2026-07-14 10:00:00', NULL, 'EMPRESTADO'),
(41, 38, 18, '2026-06-30 13:00:00', NULL, 'EMPRESTADO'),
(42, 1, 3, '2026-06-08 13:00:00', NULL, 'EMPRESTADO'),
(43, 5, 2, '2026-07-13 11:00:00', NULL, 'EMPRESTADO'),
(44, 33, 8, '2026-07-06 17:00:00', NULL, 'EMPRESTADO'),
(45, 14, 18, '2026-06-17 17:00:00', NULL, 'EMPRESTADO'),
(46, 16, 16, '2026-07-23 13:00:00', NULL, 'EMPRESTADO'),
(47, 7, 4, '2026-07-26 15:00:00', NULL, 'EMPRESTADO'),
(48, 28, 14, '2026-07-30 10:00:00', NULL, 'EMPRESTADO'),
(49, 7, 2, '2026-07-22 15:00:00', NULL, 'EMPRESTADO'),
(50, 7, 8, '2026-06-25 13:00:00', NULL, 'EMPRESTADO');

-- ============================================================
-- 4. AJUSTE DAS SEQUÊNCIAS APÓS IDs EXPLÍCITOS
-- ============================================================
SELECT setval(pg_get_serial_sequence('livros','id'), COALESCE(MAX(id), 1), true) FROM livros;
SELECT setval(pg_get_serial_sequence('usuarios','id'), COALESCE(MAX(id), 1), true) FROM usuarios;
SELECT setval(pg_get_serial_sequence('emprestimos','id'), COALESCE(MAX(id), 1), true) FROM emprestimos;

COMMIT;

-- ============================================================
-- 5. CONSULTAS DE VALIDAÇÃO
-- ============================================================
SELECT COUNT(*) AS total_livros FROM livros;
SELECT COUNT(*) AS total_usuarios FROM usuarios;
SELECT COUNT(*) AS total_emprestimos FROM emprestimos;
SELECT status, COUNT(*) AS quantidade FROM emprestimos GROUP BY status ORDER BY status;

SELECT
    e.id,
    u.nome AS usuario,
    l.titulo AS livro,
    e.data_emprestimo,
    e.data_devolucao,
    e.status
FROM emprestimos e
JOIN usuarios u ON u.id = e.usuario_id
JOIN livros l ON l.id = e.livro_id
ORDER BY e.id;