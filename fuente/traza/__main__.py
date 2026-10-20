# SPDX-License-Identifier: GPL-3.0-or-later
"""Herramientas experimentales de Traza: tokens, AST, comprobación y ejecución D0."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
from .analisis import ErrorLexico, analizar
from .analisis.sintactico import parsear
from .ejecucion import compilar, ejecutar, serializar
from .errores import ErrorPrograma, ErrorEntrada, LimiteRecursos

def json_seguro(valor):
    if isinstance(valor, bytes):
        return {"hex": valor.hex()}
    if isinstance(valor, dict):
        return {k: json_seguro(v) for k, v in valor.items()}
    if isinstance(valor, (tuple, list)):
        return [json_seguro(v) for v in valor]
    return valor

def main(argumentos: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="traza", description=__doc__)
    comandos = parser.add_subparsers(dest="comando", required=True)
    for nombre in ("tokens", "analizar", "verificar", "ejecutar"):
        comando = comandos.add_parser(nombre)
        comando.add_argument("archivo", type=Path)
        if nombre == "ejecutar":
            comando.add_argument("--entrada", required=True)
            comando.add_argument("--argumentos", default="[]", help="JSON: Number como texto")
            comando.add_argument("--max-pasos", type=int, default=100000)
            comando.add_argument("--traza", action="store_true")
    opciones = parser.parse_args(argumentos)
    try:
        datos = opciones.archivo.read_bytes()
    except OSError as error:
        print(json.dumps({"fase": "herramienta", "mensaje": str(error)},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    try:
        nombre = opciones.archivo.as_posix()
        if opciones.comando == "tokens":
            salida = {"fase": "analisis_lexico",
                      "tokens": [asdict(t) for t in analizar(datos, nombre)]}
        elif opciones.comando == "analizar":
            salida = {"fase": "analisis_sintactico", "programa": asdict(parsear(datos, nombre))}
        else:
            programa = compilar(datos, nombre)
            obligaciones = [{"funcion": n, "estado": e} for n, e in programa.obligaciones]
            if opciones.comando == "verificar":
                salida = {"fase": "comprobacion_estatica", "aceptado": True,
                          "alcance": "subconjunto D0", "obligaciones": obligaciones}
            else:
                try:
                    entradas = json.loads(opciones.argumentos)
                except (ValueError, RecursionError):
                    raise ErrorEntrada("Argumentos JSON inválidos.") from None
                if not isinstance(entradas, list):
                    raise ErrorEntrada("--argumentos requiere una lista JSON.")
                valor, eventos = ejecutar(programa, opciones.entrada, entradas, opciones.max_pasos)
                salida = {"fase": "ejecucion", "resultado": serializar(valor),
                          "obligaciones": obligaciones}
                if opciones.traza:
                    salida["eventos"] = eventos
    except ErrorLexico as error:
        print(json.dumps({"fase": "analisis_lexico", **asdict(error.diagnostico)},
                         ensure_ascii=False), file=sys.stderr)
        return 1
    except ErrorPrograma as error:
        print(json.dumps({"fase": error.fase, **asdict(error.diagnostico)},
                         ensure_ascii=False), file=sys.stderr)
        return 1
    except ErrorEntrada as error:
        print(json.dumps({"fase": "entrada", "mensaje": str(error)}, ensure_ascii=False),
              file=sys.stderr)
        return 2
    except (LimiteRecursos, RecursionError) as error:
        print(json.dumps({"fase": "recursos", "mensaje": str(error)}, ensure_ascii=False),
              file=sys.stderr)
        return 3
    print(json.dumps(json_seguro(salida), ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
