"""Ponto de entrada de ``python -m cpf``."""

import sys

from cpf.cli import main

# No Windows, com saída redirecionada, o Python usa a página de código local
# e corrompe os acentos; a CLI fala sempre UTF-8. Bytes inválidos na entrada
# viram "�" (e portanto CPF inválido), sem traceback.
for _fluxo in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(_fluxo, "reconfigure"):
        _fluxo.reconfigure(encoding="utf-8", errors="replace")

raise SystemExit(main())
