# SPDX-License-Identifier: GPL-3.0-or-later
"""Interfaz experimental de tokens; no ejecuta ni verifica programas Traza."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
from .analisis import ErrorLexico, analizar

def main(argumentos: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="traza", description=__doc__)
    subcomandos = parser.add_subparsers(dest="comando", required=True)
    tokens = subcomandos.add_parser("tokens", help="Analizar léxicamente una fuente UTF-8")
    tokens.add_argument("archivo", type=Path)
    opciones = parser.parse_args(argumentos)
    try:
        datos = opciones.archivo.read_bytes()
    except OSError as error:
        print(json.dumps({"fase": "herramienta", "mensaje": str(error)},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    try:
        resultado = analizar(datos, opciones.archivo.as_posix())
    except ErrorLexico as error:
        print(json.dumps({"fase": "analisis_lexico", **asdict(error.diagnostico)},
                         ensure_ascii=False), file=sys.stderr)
        return 1
    salida = []
    for token in resultado:
        registro = asdict(token)
        if isinstance(token.valor, bytes):
            registro["valor"] = {"hex": token.valor.hex()}
        salida.append(registro)
    print(json.dumps({"fase": "analisis_lexico", "tokens": salida}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
