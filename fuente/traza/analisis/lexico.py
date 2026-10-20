# SPDX-License-Identifier: GPL-3.0-or-later
"""Tokens según G01–G05; no comprueba gramática, nombres ni tipos."""
import re
from .fuente import Fuente
from .modelo import Token

RESERVADAS = frozenset(
    "fn pub type variant record let if else match where value check "
    "and or not true false".split()
)
# Los nombres predefinidos son IDENT; su redefinición se rechaza en resolución.
NUMERO = re.compile(r"[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?")
IDENTIFICADOR = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
HEX = frozenset("0123456789abcdefABCDEF")
ESCAPES = {'"': '"', "\\": "\\", "n": "\n", "r": "\r", "t": "\t"}
SIMBOLOS = (
    "::<", "::", "->", "=>", "<=", ">=", "==", "!=",
    "(", ")", "{", "}", "[", "]", "<", ">", ",", ":", ";",
    ".", "+", "-", "*", "/", "!", "?", "=",
)

class _Analizador:
    def __init__(self, fuente: Fuente):
        self.fuente = fuente
        self.texto = fuente.texto
        self.indice = 0

    def token(self, clase: str, inicio: int, valor: str | bytes | None = None) -> Token:
        return Token(clase, self.texto[inicio:self.indice], valor,
                     self.fuente.rango(inicio, self.indice))

    def cadena(self) -> Token:
        inicio = self.indice
        self.indice += 1
        contenido = []
        while self.indice < len(self.texto):
            caracter = self.texto[self.indice]
            if caracter == '"':
                self.indice += 1
                return self.token("STRING", inicio, "".join(contenido))
            if caracter in "\r\n":
                self.fuente.fallar("Salto de línea literal dentro de texto.",
                                  self.indice, self.indice + 1)
            if caracter != "\\":
                contenido.append(caracter)
                self.indice += 1
                continue
            escape = self.indice
            self.indice += 1
            if self.indice == len(self.texto):
                self.fuente.fallar("Escape incompleto.", escape, self.indice)
            caracter = self.texto[self.indice]
            if caracter in ESCAPES:
                contenido.append(ESCAPES[caracter])
                self.indice += 1
                continue
            if caracter != "u" or self.texto[self.indice:self.indice + 2] != "u{":
                self.fuente.fallar("Escape no admitido.", escape, self.indice + 1)
            self.indice += 2
            digitos = self.indice
            while self.indice < len(self.texto) and self.texto[self.indice] in HEX:
                self.indice += 1
            longitud = self.indice - digitos
            if (not 1 <= longitud <= 6 or self.indice == len(self.texto)
                    or self.texto[self.indice] != "}"):
                self.fuente.fallar("Escape Unicode inválido; usar u{HEX} con 1 a 6 dígitos.",
                                  escape, min(self.indice + 1, len(self.texto)))
            escalar = int(self.texto[digitos:self.indice], 16)
            self.indice += 1
            if escalar > 0x10FFFF or 0xD800 <= escalar <= 0xDFFF:
                self.fuente.fallar("El escape no representa un escalar Unicode.",
                                  escape, self.indice)
            contenido.append(chr(escalar))
        self.fuente.fallar("Literal de texto sin cierre.", inicio, self.indice)
        raise AssertionError("Inalcanzable")

    def bytes_literal(self) -> Token:
        inicio = self.indice
        self.indice += 2
        digitos = self.indice
        while self.indice < len(self.texto) and self.texto[self.indice] != '"':
            if self.texto[self.indice] not in HEX:
                self.fuente.fallar("Bytes requiere pares hexadecimales sin separadores.",
                                  self.indice, self.indice + 1)
            self.indice += 1
        if self.indice == len(self.texto):
            self.fuente.fallar("Literal de bytes sin cierre.", inicio, self.indice)
        if (self.indice - digitos) % 2:
            self.fuente.fallar("Literal de bytes con cantidad impar de dígitos.",
                              inicio, self.indice + 1)
        valor = bytes.fromhex(self.texto[digitos:self.indice])
        self.indice += 1
        return self.token("BYTES", inicio, valor)

    def analizar(self) -> tuple[Token, ...]:
        resultado = []
        while self.indice < len(self.texto):
            inicio = self.indice
            caracter = self.texto[inicio]
            if caracter in " \t\r\n":
                self.indice += 1
                continue
            if self.texto.startswith("//", inicio):
                fin = self.texto.find("\n", inicio + 2)
                self.indice = len(self.texto) if fin < 0 else fin
                continue
            if self.texto.startswith('b"', inicio):
                resultado.append(self.bytes_literal())
                continue
            if caracter == '"':
                resultado.append(self.cadena())
                continue
            coincidencia = NUMERO.match(self.texto, inicio)
            if coincidencia:
                self.indice = coincidencia.end()
                resultado.append(self.token("NUMBER", inicio, coincidencia.group()))
                continue
            coincidencia = IDENTIFICADOR.match(self.texto, inicio)
            if coincidencia:
                self.indice = coincidencia.end()
                texto = coincidencia.group()
                clase = texto if texto in RESERVADAS or texto == "_" else "IDENT"
                resultado.append(self.token(clase, inicio, texto))
                continue
            for simbolo in SIMBOLOS:
                if self.texto.startswith(simbolo, inicio):
                    self.indice += len(simbolo)
                    resultado.append(self.token(simbolo, inicio))
                    break
            else:
                self.fuente.fallar(f"Carácter no admitido: U+{ord(caracter):04X}.",
                                  inicio, inicio + 1)
        resultado.append(self.token("EOF", self.indice))
        return tuple(resultado)

def analizar(datos: bytes, archivo: str = "<entrada>") -> tuple[Token, ...]:
    """Analiza bytes completos; devuelve tokens inmutables o un ErrorLexico SG01."""
    return _Analizador(Fuente.desde_bytes(datos, archivo)).analizar()
