# SPDX-License-Identifier: GPL-3.0-or-later
from dataclasses import FrozenInstanceError
from pathlib import Path
import random
import unittest
from traza.analisis import ErrorLexico, analizar
from traza.analisis.lexico import RESERVADAS, SIMBOLOS

RAIZ = Path(__file__).resolve().parents[2]

class AnalisisLexico(unittest.TestCase):
    def clases(self, texto):
        return [t.clase for t in analizar(texto.encode("utf-8"))]

    def test_fuente_vacia_y_comentarios(self):
        for texto in ("", " \t\n\r\n", "// comentario", "// á 😀\r\n// fin"):
            with self.subTest(texto=texto):
                tokens = analizar(texto.encode())
                self.assertEqual([t.clase for t in tokens], ["EOF"])
                self.assertEqual(tokens[-1].rango.inicio.desplazamiento, len(texto.encode()))

    def test_palabras_reservadas_y_predefinidos(self):
        palabras = sorted(RESERVADAS)
        self.assertEqual(self.clases(" ".join(palabras)), palabras + ["EOF"])
        tokens = analizar(b"_ _x x1 Number Result Rounding Fn FN truex")
        self.assertEqual([t.clase for t in tokens], ["_"] + ["IDENT"] * 8 + ["EOF"])

    def test_prefijos_no_cortan_identificadores(self):
        tokens = analizar(b"fnx valuex anderson recordatorio b b0")
        self.assertEqual([t.clase for t in tokens], ["IDENT"] * 6 + ["EOF"])

    def test_todos_los_simbolos_y_maxima_longitud(self):
        tokens = analizar(" ".join(SIMBOLOS).encode())
        self.assertEqual([t.clase for t in tokens], list(SIMBOLOS) + ["EOF"])
        self.assertEqual(self.clases("f::<T>(x)!=y<=z::A=>q->r"),
                         ["IDENT", "::<", "IDENT", ">", "(", "IDENT", ")", "!=",
                          "IDENT", "<=", "IDENT", "::", "IDENT", "=>", "IDENT",
                          "->", "IDENT", "EOF"])
        self.assertEqual(self.clases("List<List<Number>>"),
                         ["IDENT", "<", "IDENT", "<", "IDENT", ">", ">", "EOF"])

    def test_numeros_son_texto_exacto(self):
        literales = ["0", "001", "1.00", "0.1", "12e3", "1E-20", "2e+3",
                     "9" * 10000, "1e999999999999999999999999"]
        for literal in literales:
            with self.subTest(longitud=len(literal)):
                token, eof = analizar(literal.encode())
                self.assertEqual((token.clase, token.texto, token.valor),
                                 ("NUMBER", literal, literal))
                self.assertEqual(eof.clase, "EOF")

    def test_signos_son_operadores(self):
        self.assertEqual(self.clases("-1 +2 -1.25e-2"),
                         ["-", "NUMBER", "+", "NUMBER", "-", "NUMBER", "EOF"])

    def test_fragmentos_numericos_no_imponen_reglas_del_parser(self):
        self.assertEqual(self.clases("1. .5 1e+ 1_000"),
                         ["NUMBER", ".", ".", "NUMBER", "NUMBER", "IDENT", "+",
                          "NUMBER", "IDENT", "EOF"])

    def test_texto_unicode_sin_normalizacion(self):
        for texto in ("á", "a\u0301", "😀", "\x00"):
            token = analizar(('"' + texto + '"').encode())[0]
            self.assertEqual(token.valor, texto)
        self.assertNotEqual(analizar('"á"'.encode())[0].valor,
                            analizar('"a\u0301"'.encode())[0].valor)

    def test_escapes(self):
        token = analizar(br'"\"\\\n\r\t\u{41}\u{1f600}"')[0]
        self.assertEqual(token.valor, '"\\\n\r\tA😀')
        self.assertEqual(analizar(br'"\u{0}\u{10ffff}"')[0].valor, "\x00\U0010ffff")
        self.assertEqual(analizar(b'""')[0].valor, "")

    def test_bytes_y_prefijo(self):
        for literal, esperado in ((b'b""', b""), (b'b"00fF"', b"\x00\xff"),
                                  (b'b"4142"', b"AB")):
            token = analizar(literal)[0]
            self.assertEqual((token.clase, token.valor), ("BYTES", esperado))
        self.assertEqual(self.clases('b "00" B"00"'),
                         ["IDENT", "STRING", "IDENT", "STRING", "EOF"])

    def test_comentario_no_se_interpreta_dentro_de_literal(self):
        self.assertEqual(analizar(b'"// comentario" // fin')[0].valor, "// comentario")
        self.assertEqual(self.clases("a//comentario\n/b"), ["IDENT", "/", "IDENT", "EOF"])
        self.assertEqual(self.clases("/* x */"), ["/", "*", "IDENT", "*", "/", "EOF"])

    def test_posiciones_utf8_y_crlf(self):
        tokens = analizar('"á😀"\r\n  fn'.encode(), "caso.traza")
        cadena, palabra, eof = tokens
        self.assertEqual((cadena.rango.inicio.desplazamiento,
                          cadena.rango.fin.desplazamiento), (0, 8))
        self.assertEqual((cadena.rango.fin.linea, cadena.rango.fin.columna), (1, 5))
        self.assertEqual((palabra.rango.inicio.desplazamiento,
                          palabra.rango.inicio.linea, palabra.rango.inicio.columna),
                         (12, 2, 3))
        self.assertEqual((eof.rango.inicio.desplazamiento, eof.rango.inicio.columna),
                         (14, 5))
        self.assertEqual(eof.rango.inicio, eof.rango.fin)
        self.assertEqual(cadena.rango.archivo, "caso.traza")

    def test_tokens_inmutables(self):
        tokens = analizar(b"fn")
        self.assertIsInstance(tokens, tuple)
        with self.assertRaises(FrozenInstanceError):
            tokens[0].texto = "pub"

    def test_rechazos_lexicos(self):
        invalidos = [
            b'"sin cierre', b'"escape\\', br'"\q"', br'"\u{}"',
            br'"\u{1234567}"', br'"\u{GG}"', br'"\u{D800}"',
            br'"\u{DFFF}"', br'"\u{110000}"', br'"\u{41"',
            b'"a\nb"', b'"a\r\nb"', b'b"F"', b'b"GG"', b'b"00 01"',
            br'b"\n"', b'b"00', b"'texto'", b"@", b"\x00", b"\r",
            "\ufefffn".encode(), "á".encode(), "９".encode(),
            "\u00a0".encode(), b"\xff", b"\xe2\x82", b"\xc0\x80",
            b"\xed\xa0\x80",
        ]
        for datos in invalidos:
            with self.subTest(datos=datos), self.assertRaises(ErrorLexico) as error:
                analizar(datos, "invalido.traza")
            if error.exception is not None:
                self.assertEqual(error.exception.diagnostico.codigo, "SG01")

    def test_ubicacion_de_utf8_invalido(self):
        with self.assertRaises(ErrorLexico) as error:
            analizar('á\n'.encode() + b"\xff", "utf8.traza")
        rango = error.exception.diagnostico.rango
        self.assertEqual((rango.inicio.desplazamiento, rango.fin.desplazamiento), (3, 4))
        self.assertEqual((rango.inicio.linea, rango.inicio.columna), (2, 1))

    def test_escape_invalido_tiene_rango_del_escape(self):
        with self.assertRaises(ErrorLexico) as error:
            analizar(br'"ab\q"')
        rango = error.exception.diagnostico.rango
        self.assertEqual((rango.inicio.desplazamiento, rango.fin.desplazamiento), (3, 5))

    def test_api_no_acepta_texto_ya_decodificado(self):
        with self.assertRaises(TypeError):
            analizar("fn")

    def test_fuentes_cf_se_tokenizan_sin_aprobarlas(self):
        archivos = list((RAIZ / "pruebas/conformidad/programas").rglob("*.traza"))
        self.assertGreater(len(archivos), 10)
        for archivo in archivos:
            with self.subTest(archivo=archivo.name):
                self.assertEqual(analizar(archivo.read_bytes(), archivo.name)[-1].clase, "EOF")

    def test_propiedad_rangos_reconstruyen_lexemas(self):
        azar = random.Random(20261020)
        atomos = ['fn', '_', 'x9', '12.30e-4', '"á😀"', 'b"00FF"',
                  '::<', '>=', '?', '(', ')', '{', '}', '// fin\n']
        for _ in range(100):
            texto = " \t".join(azar.choice(atomos) for _ in range(30))
            datos = texto.encode()
            anterior = 0
            for token in analizar(datos):
                inicio = token.rango.inicio.desplazamiento
                fin = token.rango.fin.desplazamiento
                self.assertLessEqual(anterior, inicio)
                self.assertLessEqual(inicio, fin)
                self.assertEqual(datos[inicio:fin].decode(), token.texto)
                self.assertEqual(token.rango.inicio.linea,
                                 datos[:inicio].decode().count("\n") + 1)
                anterior = fin
