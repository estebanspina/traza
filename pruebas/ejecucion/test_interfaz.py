# SPDX-License-Identifier: GPL-3.0-or-later
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from herramientas.probar_d0 import probar, coincide

RAIZ = Path(__file__).resolve().parents[2]

class InterfazEjecucion(unittest.TestCase):
    def invocar(self, *argumentos):
        return subprocess.run([sys.executable, str(RAIZ / "herramientas/traza.py"), *argumentos],
                              cwd=tempfile.gettempdir(), capture_output=True, text=True,
                              encoding="utf-8", timeout=10, check=False)

    def archivo(self, fuente, comando, *argumentos):
        with tempfile.TemporaryDirectory() as directorio:
            ruta = Path(directorio) / "programa.traza"
            ruta.write_text(fuente, encoding="utf-8")
            return self.invocar(comando, str(ruta), *argumentos)

    def test_analizar_no_significa_aceptar_tipos(self):
        fuente = "pub fn main() -> Number {true}"
        r = self.archivo(fuente, "analizar")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["fase"], "analisis_sintactico")
        r = self.archivo(fuente, "verificar")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(r.stderr)["codigo"], "D01")

    def test_ejecutar_bounded_con_err_es_ejecucion_correcta(self):
        ruta = RAIZ / "ejemplos/contratos/bounded.traza"
        for valor, variante in (("50", "Ok"), ("101", "Err"), ("-1", "Err")):
            with self.subTest(valor=valor):
                r = self.invocar("ejecutar", str(ruta), "--entrada", "bounded",
                                 "--argumentos", json.dumps([valor]), "--traza")
                self.assertEqual(r.returncode, 0, r.stderr)
                salida = json.loads(r.stdout)
                self.assertEqual(salida["resultado"]["variante"], variante)
                self.assertIn(["control_retorno", "bounded"], salida["eventos"])

    def test_argumentos_mal_formados_son_error_de_entrada(self):
        fuente = "pub fn main(x: Number) -> Number {x}"
        for argumentos in ("[1]", "[true]", "[0.1]", '["NaN"]', "{}", "mal", "[]"):
            with self.subTest(argumentos=argumentos):
                r = self.archivo(fuente, "ejecutar", "--entrada", "main",
                                 "--argumentos", argumentos)
                self.assertEqual(r.returncode, 2)
                self.assertEqual(json.loads(r.stderr)["fase"], "entrada")

    def test_limite_no_es_err_del_lenguaje(self):
        r = self.archivo("pub fn main() -> Number {main()}", "ejecutar",
                         "--entrada", "main", "--max-pasos", "50")
        self.assertEqual(r.returncode, 3)
        self.assertEqual(json.loads(r.stderr)["fase"], "recursos")
        self.assertEqual(r.stdout, "")

    def test_no_implementado_no_se_ejecuta(self):
        r = self.archivo("pub fn main() -> List<Number> {[1]}", "ejecutar",
                         "--entrada", "main")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(r.stderr)["codigo"], "NI01")

    def test_verificacion_expone_obligacion_desconocida(self):
        r = self.invocar("verificar", str(RAIZ / "ejemplos/contratos/bounded.traza"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["obligaciones"],
                         [{"funcion": "bounded", "estado": "desconocida"}])

    def test_informe_d0_y_oraculo_no_aprueban_resultado_incorrecto(self):
        informe = probar()
        self.assertEqual((informe["aprobados"], informe["total"]), (4, 4))
        self.assertFalse(coincide({"diagnostico": "NI01"}, {"diagnostico": "D05"}))
        self.assertFalse(coincide({"variante": "Ok"}, {"variante": "Err"}))
        self.assertTrue(coincide({"tipo": "Number", "valor": "50.0"},
                                {"tipo": "Number", "valor": "50"}))
        self.assertFalse(coincide({"codigo": "ContractViolation"},
                                 {"campos_requeridos": ["location"]}))
