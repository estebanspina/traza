# SPDX-License-Identifier: GPL-3.0-or-later
import copy
from pathlib import Path
import tempfile
import unittest
from herramientas.catalogo import leer_json, ruta_del_repositorio, sin_flotantes, validar

RAIZ = Path(__file__).resolve().parents[2]

class CatalogoDeConformidad(unittest.TestCase):
    def test_catalogo_completo_y_referencias_reciprocas(self):
        reglas, casos, variantes = validar(RAIZ)
        self.assertEqual((reglas, casos), (116, 40))
        self.assertGreater(variantes, 40)

    def test_no_admite_numeros_aproximados(self):
        for valor in (0.1, {"tipo": "Number", "valor": 0.1},
                      {"tipo": "Number", "valor": "NaN"}):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                sin_flotantes(valor)
        sin_flotantes({"tipo": "Number", "valor": "123456789012345678901.23e-40"})

    def test_rutas_no_pueden_escapar(self):
        for ruta in ("../README.md", "/etc/passwd", "no-existe.traza"):
            with self.subTest(ruta=ruta), self.assertRaises(ValueError):
                ruta_del_repositorio(RAIZ, ruta)

    def test_variantes_criticas_presentes(self):
        casos = {c["id"]: c for c in leer_json(
            RAIZ / "pruebas/conformidad/catalogo.json")["casos"]}
        for identificador, minimo in (("CF02", 2), ("CF05", 2), ("CF15", 2),
                                     ("CF24", 2), ("CF25", 2), ("CF30", 2),
                                     ("CF31", 2), ("CF32", 2), ("CF33", 2),
                                     ("CF37", 4), ("CF39", 2), ("CF40", 3)):
            with self.subTest(caso=identificador):
                self.assertGreaterEqual(len(casos[identificador]["variantes"]), minimo)
        self.assertEqual(casos["CF35"]["generador"]["escalas"], [0, 2, 8])
        self.assertEqual(len(casos["CF35"]["generador"]["modos"]), 6)
        self.assertEqual(casos["CF14"]["fase_esperada"], "proceso")
        self.assertEqual(casos["CF33"]["protocolo"]["enlace_api"], "pendiente_de_esquemas")
