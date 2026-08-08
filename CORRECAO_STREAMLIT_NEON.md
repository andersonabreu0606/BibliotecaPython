# Correção Streamlit + Neon

## 1. Neon

No projeto Neon, abra **Connect** e copie a **Direct connection string**.

Formato esperado:

```text
postgresql://usuario:senha@ep-xxxx.neon.tech/neondb?sslmode=require
```

## 2. Streamlit Community Cloud

Abra **Manage app > Settings > Secrets** e configure:

```toml
DATABASE_URL = "postgresql://usuario:senha@ep-xxxx.neon.tech/neondb?sslmode=require"
```

Salve e reinicie/redeploy a aplicação.

## 3. Driver

A versão corrigida usa Psycopg 3, compatível com Python 3.14, e normaliza automaticamente:

```text
postgresql://...
```

para:

```text
postgresql+psycopg://...
```

## 4. Se ainda falhar

Abra os logs do Streamlit e procure a última linha de `sqlalchemy.exc.OperationalError` ou `psycopg.OperationalError`.

Causas típicas:

- `password authentication failed` — utilizador/senha incorretos;
- `could not translate host name` — hostname incorreto;
- `connection timed out` — endpoint/rede;
- erro de SSL — use a URL completa com `sslmode=require`;
- `database ... does not exist` — nome do banco incorreto.
