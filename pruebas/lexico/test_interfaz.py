# SPDX-License-Identifier: GPL-3.0-or-later
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RAIZ = Path(__file__).resolve().parents[2]

class InterfazTokens(unittest.TestCase):
    def invocar(self, *argumentos):
        return subprocess.run(
            [sys.executable, str(RAIZ / "herramientas/traza.py"), *argumentos],
            capture_output=True, text=True, encoding="utf-8", cwd=tempfile.gettempdir(),
            timeout=10, check=False
        )

    def test_tokens_desde_otro_directorio(self):
        ruta = RAIZ / "ejemplos/contratos/bounded.traza"
        resultado = self.invocar("tokens", str(ruta))
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        salida = json.loads(resultado.stdout)
        self.assertEqual(salida["fase"], "analisis_lexico")
        self.assertEqual(salida["tokens"][0]["clase"], "pub")
        self.assertEqual(salida["tokens"][-1]["clase"], "EOF")
        self.assertEqual(resultado.stderr, "")

    def test_diagnostico_es_json_y_no_result(self):
        with tempfile.TemporaryDirectory() as directorio:
            ruta = Path(directorio) / "invalido.traza"
            ruta.write_bytes(b"@")
            resultado = self.invocar("tokens", str(ruta))
        self.assertEqual(resultado.returncode, 1)
        self.assertEqual(resultado.stdout, "")
        diagnostico = json.loads(resultado.stderr)
        self.assertEqual(diagnostico["codigo"], "SG01")
        self.assertEqual(diagnostico["rango"]["inicio"]["desplazamiento"], 0)

    def test_bytes_se_serializan_como_hex(self):
        with tempfile.TemporaryDirectory() as directorio:
            ruta = Path(directorio) / "bytes.traza"
            ruta.write_bytes(b'b"00fF"')
            resultado = self.invocar("tokens", str(ruta))
        self.assertEqual(resultado.returncode, 0)
        self.assertEqual(json.loads(resultado.stdout)["tokens"][0]["valor"], {"hex": "00ff"})

    def test_archivo_inexistente_es_error_de_herramienta(self):
        resultado = self.invocar("tokens", str(RAIZ / "no-existe.traza"))
        self.assertEqual(resultado.returncode, 2)
        self.assertEqual(json.loads(resultado.stderr)["fase"], "herramienta")

    def test_no_se_ofrece_ejecucion_inexistente(self):
        resultado = self.invocar("compilar_nativo", "x.traza")
        self.assertEqual(resultado.returncode, 2)
        self.assertIn("invalid choice", resultado.stderr)
