# SPDX-License-Identifier: GPL-3.0-or-later
"""Punto único de verificación; no instala dependencias ni ejecuta Traza."""
from pathlib import Path
import compileall
import platform
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]

def main() -> int:
    print(f"Python {platform.python_version()} | {platform.platform()}", flush=True)
    if sys.version_info[:2] != (3, 12):
        print("Se requiere Python 3.12; ver .python-version.", file=sys.stderr)
        return 2
    sys.path.insert(0, str(RAIZ / "fuente"))
    sys.path.insert(0, str(RAIZ))
    suite = unittest.defaultTestLoader.discover(
        str(RAIZ / "pruebas"), top_level_dir=str(RAIZ)
    )
    if suite.countTestCases() == 0:
        print("Error: no se descubrieron pruebas.", file=sys.stderr)
        return 2
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    sintaxis = all(
        compileall.compile_dir(str(RAIZ / ruta), quiet=1)
        for ruta in ("fuente", "pruebas", "herramientas")
    )
    return 0 if resultado.wasSuccessful() and sintaxis else 1

if __name__ == "__main__":
    raise SystemExit(main())
