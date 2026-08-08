# Publicação gratuita: Streamlit Community Cloud + Neon PostgreSQL

Este projeto foi preparado para funcionar localmente com SQLite e, na internet, com PostgreSQL.

## 1. Criar um repositório no GitHub

Crie um repositório, por exemplo `sistema-biblioteca`, e envie todos os arquivos do projeto.

Exemplo usando Git:

```bash
git init
git add .
git commit -m "Projeto final - Sistema de Biblioteca"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/sistema-biblioteca.git
git push -u origin main
```

## 2. Criar o banco gratuito no Neon

1. Crie uma conta no Neon.
2. Crie um novo projeto PostgreSQL.
3. Copie a connection string fornecida pelo painel.
4. Prefira a conexão pooled quando disponível para aplicações web/serverless.

Formato típico:

```text
postgresql://USUARIO:SENHA@HOST/BANCO?sslmode=require
```

**Não** grave essa senha no GitHub.

## 3. Publicar no Streamlit Community Cloud

1. Acesse o Streamlit Community Cloud e conecte sua conta GitHub.
2. Clique em **Create app**.
3. Selecione o repositório e a branch `main`.
4. Informe `app.py` como entrypoint.
5. Em **Advanced settings > Secrets**, configure:

```toml
DATABASE_URL = "postgresql://USUARIO:SENHA@HOST/BANCO?sslmode=require"
```

6. Clique em **Deploy**.

A aplicação receberá uma URL fixa no domínio `streamlit.app`.

## 4. Teste após o deploy

Valide pelo menos:

- cadastro de livro;
- cadastro de usuário;
- empréstimo com cópia disponível;
- tentativa de empréstimo sem disponibilidade;
- devolução;
- consulta por título, autor e ano;
- relatórios e download CSV;
- persistência dos dados após reiniciar/reabrir a aplicação.

## 5. Gerar QR Code após receber a URL

```bash
python gerar_qr.py https://seu-subdominio.streamlit.app
```

O arquivo `qrcode_sistema.png` será criado na pasta atual.
