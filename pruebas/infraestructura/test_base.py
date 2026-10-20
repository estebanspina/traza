# SPDX-License-Identifier: GPL-3.0-or-later
"""Comprueba infraestructura del repositorio; no interpreta Traza."""
import json
from pathlib import Path
import unittest

RAIZ = Path(__file__).resolve().parents[2]

class BaseDelRepositorio(unittest.TestCase):
    def setUp(self):
        self.manifiesto = json.loads(
            (RAIZ / "pruebas/conformidad/manifiestos/d0.json").read_text(encoding="utf-8")
        )

    def test_programas_y_expectativas_del_manifiesto(self):
        self.assertEqual(self.manifiesto["version_esquema"], "0.1")
        vistos = set()
        for caso in self.manifiesto["casos"]:
            with self.subTest(caso=caso["id"]):
                self.assertNotIn(caso["id"], vistos)
                vistos.add(caso["id"])
                ruta = (RAIZ / caso["programa"]).resolve()
                self.assertTrue(ruta.is_relative_to(RAIZ))
                self.assertTrue(ruta.is_file())
                self.assertEqual(caso["estado"], "pendiente")
                self.assertIn(caso["fase_esperada"], {"ejecucion", "comprobacion_estatica"})
                self.assertTrue(caso["esperado"])
                for argumento in caso["argumentos"]:
                    if argumento["tipo"] == "Number":
                        self.assertIsInstance(argumento["valor"], str)
        self.assertEqual(vistos, {"CF01", "CF02", "CF02-negativo", "CF06"})

    def test_valores_de_frontera_de_d0(self):
        casos = {caso["id"]: caso for caso in self.manifiesto["casos"]}
        self.assertEqual(casos["CF01"]["argumentos"][0]["valor"], "50")
        self.assertEqual(casos["CF01"]["esperado"]["variante"], "Ok")
        for identificador, valor in (("CF02", "101"), ("CF02-negativo", "-1")):
            caso = casos[identificador]
            self.assertEqual(caso["argumentos"][0]["valor"], valor)
            self.assertEqual(caso["esperado"]["codigo"], "ContractViolation")
            self.assertEqual(set(caso["esperado"]["campos_requeridos"]),
                             {"condition_id", "location", "boundary"})
        self.assertEqual(casos["CF06"]["esperado"]["diagnostico"], "D05")

    def test_serie_documental_completa(self):
        directorio = RAIZ / "documentacion"
        for numero in range(1, 9):
            encontrados = list(directorio.glob(f"*/{numero:02}-*.md"))
            self.assertEqual(len(encontrados), 1, numero)
            texto = encontrados[0].read_text(encoding="utf-8")
            self.assertIn("Transcripción textual", texto)
            self.assertIn("Página 1", texto)
            self.assertGreater(len(texto), 1000)

    def test_base_de_licencia(self):
        texto = (RAIZ / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", texto)
        self.assertIn("Version 3, 29 June 2007", texto)
        self.assertIn("17. Interpretation of Sections 15 and 16.", texto)

if __name__ == "__main__":
    unittest.main()
