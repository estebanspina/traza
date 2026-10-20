# SPDX-License-Identifier: GPL-3.0-or-later
import json
from pathlib import Path
import unittest
from traza.ejecucion import compilar, ejecutar, serializar
from traza.errores import ErrorPrograma, ErrorEntrada, LimiteRecursos
from traza.numeros import Numero

RAIZ = Path(__file__).resolve().parents[2]
PROGRAMAS = RAIZ / "pruebas/conformidad/programas"

class EjecucionD0(unittest.TestCase):
    def programa(self, fuente):
        return compilar(fuente.encode(), "prueba.traza")

    def correr(self, fuente, entrada="main", argumentos=(), max_pasos=100000):
        return ejecutar(self.programa(fuente), entrada, argumentos, max_pasos)

    def test_manifiesto_d0_realmente_ejecutado(self):
        m = json.loads((RAIZ / "pruebas/conformidad/manifiestos/d0.json").read_text())
        for caso in m["casos"]:
            ruta = RAIZ / caso["programa"]
            with self.subTest(caso=caso["id"]):
                if caso["fase_esperada"] == "comprobacion_estatica":
                    with self.assertRaises(ErrorPrograma) as error:
                        compilar(ruta.read_bytes(), caso["programa"])
                    self.assertEqual(error.exception.diagnostico.codigo, caso["esperado"]["diagnostico"])
                else:
                    p = compilar(ruta.read_bytes(), caso["programa"])
                    valor, eventos = ejecutar(p, caso["entrada"],
                                             [a["valor"] for a in caso["argumentos"]])
                    salida = serializar(valor)
                    for campo, esperado in caso["esperado"].items():
                        if campo == "campos_requeridos":
                            for nombre in esperado:
                                self.assertTrue(salida[nombre])
                        else:
                            self.assertEqual(salida[campo], esperado)
                    self.assertIn(("control_retorno", "bounded"), eventos)

    def test_pipeline_conserva_garantia_y_propaga(self):
        ruta = PROGRAMAS / "aceptados/pipeline.traza"
        p = compilar(ruta.read_bytes(), ruta.as_posix())
        v, eventos = ejecutar(p, "pipeline", ["25"])
        self.assertEqual(serializar(v), {"variante": "Ok", "valor": {"tipo": "Number", "valor": "50"}})
        self.assertIn(("entrada", "double"), eventos)
        self.assertNotIn(("control_retorno", "double"), eventos)
        v, eventos = ejecutar(p, "pipeline", ["101"])
        self.assertEqual(serializar(v)["codigo"], "ContractViolation")
        self.assertNotIn(("entrada", "double"), eventos)

    def test_check_explicito(self):
        ruta = PROGRAMAS / "aceptados/below-fifty.traza"
        p = compilar(ruta.read_bytes(), ruta.as_posix())
        self.assertEqual(serializar(ejecutar(p, "below_fifty", ["49"])[0])["variante"], "Ok")
        self.assertEqual(serializar(ejecutar(p, "below_fifty", ["50"])[0])["codigo"], "ContractViolation")

    def test_rechazos_de_contratos_y_tipos(self):
        ejemplos = [
            ("rechazados/retorno-sin-canal.traza", "D06"),
            ("rechazados/precondicion.traza", "D04"),
            ("rechazados/transformacion.traza", "D04"),
            ("rechazados/retorno-imposible.traza", "D05"),
        ]
        for ruta, codigo in ejemplos:
            with self.subTest(ruta=ruta), self.assertRaises(ErrorPrograma) as error:
                compilar((PROGRAMAS / ruta).read_bytes())
            self.assertEqual(error.exception.diagnostico.codigo, codigo)
        for cuerpo in ("true + 1", "not 1", "if (1) {1} else {2}"):
            with self.subTest(cuerpo=cuerpo), self.assertRaises(ErrorPrograma):
                self.programa(f"pub fn main() -> Number {{ {cuerpo} }}")

    def test_return_err_no_se_refina(self):
        ruta = PROGRAMAS / "aceptados/error-ordinario.traza"
        p = compilar(ruta.read_bytes())
        self.assertEqual(serializar(ejecutar(p, "failed", [])[0]),
                         {"variante": "Err", "codigo": "InvalidInput"})

    def test_numero_exacto_y_limites_externos(self):
        v, _ = self.correr("pub fn main() -> Number {0.1 + 0.2}")
        self.assertEqual(v, Numero.desde_texto("0.3"))
        v, _ = self.correr("pub fn main() -> Number {125.50 * 0.015}")
        self.assertEqual(v.texto(), "1.8825")
        self.assertEqual(Numero.desde_texto("-0.00"), Numero(0))
        with self.assertRaises(LimiteRecursos):
            self.programa("pub fn main() -> Number {1e999999}")
        with self.assertRaises(LimiteRecursos):
            self.correr("pub fn main() -> Number { main() }", max_pasos=100)

    def test_pila_de_llamadas_no_depende_de_recursion_python(self):
        fuente = """pub fn down(n: Number) -> Number {
 if (n == 0) {0} else {down(n - 1)}
}"""
        v, _ = self.correr(fuente, "down", ["1200"])
        self.assertEqual(v, Numero(0))

    def test_ramas_y_cortocircuito_no_ejecutan_recursion(self):
        ruta = PROGRAMAS / "aceptados/ramas.traza"
        p = compilar(ruta.read_bytes())
        for nombre, esperado in (("selected", Numero(7)), ("and_short", False), ("or_short", True)):
            with self.subTest(nombre=nombre):
                v, eventos = ejecutar(p, nombre, [])
                self.assertEqual(v, esperado)
                self.assertNotIn(("entrada", "forever"), eventos)

    def test_err_ordinario_no_corta_argumentos(self):
        fuente = """fn first() -> Result<Number, Error> {Result::Err(Error::InvalidInput)}
fn second() -> Number {2}
fn take(r: Result<Number, Error>, n: Number) -> Number {n}
pub fn main() -> Number {take(first(), second())}"""
        v, eventos = self.correr(fuente)
        self.assertEqual(v, Numero(2))
        entradas = [nombre for clase, nombre in eventos if clase == "entrada"]
        self.assertEqual(entradas, ["main", "first", "second", "take"])

    def test_propagacion_no_cruza_la_funcion_mas_cercana(self):
        fuente = """fn fail(x: Number) -> Result<Number, Error> {
 let y = (check (x) where {value < 0})?;
 Result::Ok(y)
}
fn pass(r: Result<Number, Error>) -> Result<Number, Error> {r}
pub fn main() -> Result<Number, Error> {pass(fail(1))}"""
        v, eventos = self.correr(fuente)
        self.assertEqual(serializar(v)["codigo"], "ContractViolation")
        self.assertIn(("entrada", "pass"), eventos)

    def test_argumentos_externos_no_se_convierten_implicitamente(self):
        p = self.programa("pub fn main(x: Number where {value >= 0}) -> Number {x}")
        for args in ([1], [True], ["NaN"], ["-1"], []):
            with self.subTest(args=args), self.assertRaises(ErrorEntrada):
                ejecutar(p, "main", args)
        with self.assertRaises(ErrorEntrada):
            ejecutar(p, "ausente", ["1"])
        p = self.programa("fn privada() -> Number {1}")
        with self.assertRaises(ErrorEntrada):
            ejecutar(p, "privada", [])

    def test_funciones_y_vinculaciones_duplicadas_y_sombreado(self):
        invalidos = [
            "fn f() -> Number {1} fn f() -> Number {2}",
            "pub fn main(x: Number, x: Number) -> Number {x}",
            "pub fn main(x: Number) -> Number {let x = 1; x}",
            "pub fn main() -> Number {let Number = 1; Number}",
            "fn foo() -> Number {1} pub fn main() -> Number {let foo = 2; foo()}",
        ]
        for fuente in invalidos:
            with self.subTest(fuente=fuente), self.assertRaises(ErrorPrograma):
                self.programa(fuente)
        v, _ = self.correr("pub fn main(x: Number) -> Number {if (true) {let x = 3; x} else {x}}",
                          argumentos=["1"])
        self.assertEqual(v, Numero(3))

    def test_predicados_arbitrarios_y_relacionales_no_se_aceptan(self):
        for fuente, codigo in [
            ("fn f(x: Number) -> Boolean {true} pub fn main(x: Number) -> Result<Number where {f(value)}, Error> {Result::Ok(x)}", "D03"),
            ("pub fn main(x: Number) -> Result<Number where {value >= x}, Error> {Result::Ok(x)}", "NI01"),
        ]:
            with self.subTest(codigo=codigo), self.assertRaises(ErrorPrograma) as error:
                self.programa(fuente)
            self.assertEqual(error.exception.diagnostico.codigo, codigo)

    def test_retorno_refutado_de_rama_y_rama_imposible(self):
        with self.assertRaises(ErrorPrograma) as error:
            self.programa("pub fn main(b: Boolean) -> Result<Number where {value <= 100}, Error> {if (b) {Result::Ok(101)} else {Result::Ok(50)}}")
        self.assertEqual(error.exception.diagnostico.codigo, "D05")
        v, _ = self.correr("pub fn main() -> Result<Number where {value <= 100}, Error> {if (true) {Result::Ok(50)} else {Result::Ok(101)}}")
        self.assertEqual(serializar(v)["variante"], "Ok")

    def test_estructura_sin_ejecutor_es_no_implementada(self):
        for fuente in ("type X = Number; pub fn main() -> Number {1}",
                       "pub fn main<T>(x: T) -> T {x}",
                       "pub fn main() -> List<Number> {[1]}",
                       "pub fn main() -> Number {1/8}",
                       "pub fn main() -> Number !{ReadFile} {1}"):
            with self.subTest(fuente=fuente), self.assertRaises(ErrorPrograma) as error:
                self.programa(fuente)
            self.assertEqual(error.exception.diagnostico.codigo, "NI01")

    def test_ramas_demostradas_imposibles_no_refutan_el_retorno(self):
        fuentes = [
            ("pub fn main() -> Result<Number where {value <= 100}, Error> {if (1 == 1) {Result::Ok(50)} else {Result::Ok(101)}}", []),
            ("pub fn main(x: Number where {value >= 0}) -> Result<Number where {value <= 100}, Error> {if (x < 0) {Result::Ok(101)} else {Result::Ok(50)}}", ["3"]),
            ("pub fn main(x: Number) -> Result<Number where {value <= 100}, Error> {if (x < x) {Result::Ok(101)} else {Result::Ok(50)}}", ["3"]),
        ]
        for fuente, argumentos in fuentes:
            with self.subTest(fuente=fuente):
                v, _ = self.correr(fuente, argumentos=argumentos)
                self.assertEqual(serializar(v)["valor"]["valor"], "50")

    def test_conectores_constantes_descartan_ramas_imposibles(self):
        for condicion in ("true and true", "false or true", "not false"):
            fuente = ("pub fn main() -> Result<Number where {value <= 100}, Error> {"
                      "if (" + condicion + ") {Result::Ok(50)} else {Result::Ok(101)}}")
            with self.subTest(condicion=condicion):
                v, _ = self.correr(fuente)
                self.assertEqual(serializar(v)["valor"]["valor"], "50")
