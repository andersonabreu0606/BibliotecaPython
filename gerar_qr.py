from __future__ import annotations

import sys
from pathlib import Path
import qrcode


def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python gerar_qr.py https://seu-sistema.streamlit.app")
        raise SystemExit(1)

    url = sys.argv[1].strip()
    if not (url.startswith("https://") or url.startswith("http://")):
        print("Informe uma URL válida iniciando com http:// ou https://")
        raise SystemExit(1)

    img = qrcode.make(url)
    destino = Path("qrcode_sistema.png")
    img.save(destino)
    print(f"QR Code gerado em: {destino.resolve()}")


if __name__ == "__main__":
    main()
