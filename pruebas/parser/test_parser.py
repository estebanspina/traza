# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import unittest
from traza.analisis.sintactico import parsear
from traza.errores import ErrorPrograma

RAIZ = Path(__file__).resolve().parents[2]

class ParserTraza(unittest.TestCase):
    def programa(self, texto):
        return parsear(texto.encode(), "prueba.traza")

    def expr(self, texto):
        return self.programa("fn f() -> Number { " + texto + " }").declaraciones[0].datos[6].datos[1]

    def test_precedencias(self):
        nodo = self.expr("1 + 2 * 3")
        self.assertEqual(nodo.datos[0], "+")
        self.assertEqual(nodo.datos[2].datos[0], "*")
        nodo = self.expr("1 - 2 - 3")
        self.assertEqual(nodo.datos[0], "-")
        self.assertEqual(nodo.datos[1].datos[0], "-")
        nodo = self.expr("true or false and not true")
        self.assertEqual(nodo.datos[0], "or")
        self.assertEqual(nodo.datos[2].datos[0], "and")
        self.assertEqual(self.expr("not x < 5").datos[1].clase, "unario")

    def test_sufijos_y_genericos_sin_ambiguedad(self):
        n = self.expr("f::<Number>(x).field?")
        self.assertEqual(n.clase, "propagar")
        self.assertEqual(n.datos[0].clase, "campo")
        self.assertEqual(n.datos[0].datos[0].clase, "llamada")
        self.assertEqual(n.datos[0].datos[0].datos[0].clase, "instancia")
        self.assertEqual(self.expr("x < y").clase, "binario")

    def test_gramatica_completa_de_tipos_y_estructuras(self):
        fuente = """
pub type Choice<T> = variant {First(T), Second};
type Pair = {left: Number, right: Number};
type Empty = {};
type Callback = (fn(x: Number) -> Number !{ReadFile});
pub fn identity<T>(x: T) -> T { x }
fn demo() -> Pair {
 let f: (fn(x: Number) -> Number) = fn(x: Number) -> Number { x * 2 };
 let empty = record {};
 let xs: List<Number> = [];
 record {left: f(2), right: identity::<Number>(3)}
}
"""
        self.assertEqual(len(self.programa(fuente).declaraciones), 6)

    def test_contratos_llaves_y_comparaciones(self):
        p = self.programa("""pub fn f(x: Number)
 -> Result<Number where {value > 0 and value <= 100}, Error> {
 let y = (check (x) where {value > 0})?;
 Result::Ok(y)
}""")
        self.assertEqual(p.declaraciones[0].datos[4].datos[1][0].clase, "refinado")

    def test_match_patrones_y_coma_final(self):
        n = self.expr('match (x) { Choice::First(n) => {n}, -1 => {0}, _ => {2}, }')
        self.assertEqual(n.clase, "match")
        self.assertEqual(len(n.datos[1]), 3)
        self.assertEqual(n.datos[1][0][0].clase, "patron_variante")

    def test_vacio_y_rangos(self):
        self.assertEqual(self.programa("").declaraciones, ())
        p = self.programa("fn f() -> Number { 1 }")
        n = p.declaraciones[0]
        self.assertEqual(n.rango.inicio.desplazamiento, 0)
        self.assertEqual(n.rango.fin.desplazamiento, 22)

    def test_rechazos_con_fase_y_codigo(self):
        casos = [
            ("fn f() -> Number {}", "SG03"),
            ("fn f() -> Number { 1; }", "SG03"),
            ("fn f() -> Number { let x = 1 x }", "SG03"),
            ("fn f() -> Number { 0 <= x <= 100 }", "SG04"),
            ("fn f() -> Number { if (true) {1} }", "SG02"),
            ("fn f() -> Number { record {x: 1,} }", "SG02"),
            ("fn f(x: Number,) -> Number {x}", "SG02"),
            ("type A = variant {};", "SG02"),
            ("fn f() -> Number { check (1) where {value > 0}? }", "SG02"),
            ("let x = 1;", "SG02"),
            ("fn f() -> Number {1} basura", "SG02"),
        ]
        for fuente, codigo in casos:
            with self.subTest(fuente=fuente), self.assertRaises(ErrorPrograma) as error:
                self.programa(fuente)
            self.assertEqual(error.exception.fase, "analisis_sintactico")
            self.assertEqual(error.exception.diagnostico.codigo, codigo)

    def test_programas_cf_sintacticos_sin_confundir_tipos(self):
        archivos = list((RAIZ / "pruebas/conformidad/programas").rglob("*.traza"))
        for archivo in archivos:
            with self.subTest(archivo=archivo.name):
                if archivo.name.startswith("cf37-"):
                    with self.assertRaises(ErrorPrograma):
                        parsear(archivo.read_bytes(), archivo.name)
                else:
                    parsear(archivo.read_bytes(), archivo.name)
