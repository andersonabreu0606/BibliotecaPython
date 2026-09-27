from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "log"
LOG_DIR.mkdir(exist_ok=True)


def formatar_nome_funcionalidade(nome: str) -> str:
    base = nome.removeprefix("test_")
    return base.replace("_", " ").strip().title()


def extrair_resultados(pytest_output: str) -> list[str]:
    linhas: list[str] = []
    padrao = re.compile(r"(.+::[A-Za-z0-9_]+)\s+(PASSED|FAILED|ERROR)\b")

    for linha in pytest_output.splitlines():
        match = padrao.search(linha)
        if not match:
            continue

        nome, status = match.groups()
        nome_funcionalidade = nome.split("::")[-1]
        linhas.append(f"FUNCIONALIDADE: {formatar_nome_funcionalidade(nome_funcionalidade)} | RESULTADO: {status}")

    return linhas


def main() -> int:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    log_path = LOG_DIR / f"log_{timestamp}.log"

    cmd = [sys.executable, "-m", "pytest", "-vv", "-rA"]
    process = subprocess.run(
        cmd,
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    resultados = extrair_resultados(process.stdout)
    linhas_log = ["RELATORIO DE TESTES - DEPLOY", f"DATA/HORA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]
    linhas_log.extend(resultados)
    linhas_log.append("")
    linhas_log.append("RESULTADO FINAL: PASSOU" if process.returncode == 0 else "RESULTADO FINAL: FALHOU")

    with log_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(linhas_log) + "\n")

    if process.stdout:
        print(process.stdout, end="")
    print(f"\nLog salvo em: {log_path}")

    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
