# SPDX-License-Identifier: GPL-3.0-or-later
"""Decimal finito exacto mínimo: literales, suma, resta, producto y orden."""
from dataclasses import dataclass
import re
from .errores import LimiteRecursos

PATRON = re.compile(r"([+-]?)([0-9]+)(?:\.([0-9]+))?(?:[eE]([+-]?[0-9]+))?\Z")
MAX_DIGITOS = 1000
MAX_EXPONENTE = 1000
MAX_BITS = 8192

@dataclass(frozen=True, slots=True)
class Numero:
    coeficiente: int
    exponente: int = 0

    def __post_init__(self):
        c, e = self.coeficiente, self.exponente
        if abs(c).bit_length() > MAX_BITS or abs(e) > MAX_EXPONENTE:
            raise LimiteRecursos("Presupuesto de Number agotado; no se redondea el valor.")
        if c == 0:
            e = 0
        else:
            while c % 10 == 0:
                c //= 10
                e += 1
        if abs(e) > MAX_EXPONENTE:
            raise LimiteRecursos("Exponente fuera del presupuesto del prototipo.")
        object.__setattr__(self, "coeficiente", c)
        object.__setattr__(self, "exponente", e)

    @classmethod
    def desde_texto(cls, texto):
        m = PATRON.fullmatch(texto)
        if not m:
            raise ValueError("Literal decimal inválido")
        signo, entero, fraccion, exponente = m.groups()
        fraccion = fraccion or ""
        if len(entero) + len(fraccion) > MAX_DIGITOS or len(exponente or "") > 6:
            raise LimiteRecursos("Literal fuera del presupuesto numérico.")
        e = int(exponente or "0") - len(fraccion)
        c = int(entero + fraccion) * (-1 if signo == "-" else 1)
        return cls(c, e)

    def _alinear(self, otro):
        e = min(self.exponente, otro.exponente)
        return (self.coeficiente * 10 ** (self.exponente - e),
                otro.coeficiente * 10 ** (otro.exponente - e), e)

    def __add__(self, otro):
        a, b, e = self._alinear(otro)
        return Numero(a + b, e)

    def __neg__(self):
        return Numero(-self.coeficiente, self.exponente)

    def __sub__(self, otro):
        return self + (-otro)

    def __mul__(self, otro):
        return Numero(self.coeficiente * otro.coeficiente, self.exponente + otro.exponente)

    def comparar(self, otro):
        a, b, _ = self._alinear(otro)
        return (a > b) - (a < b)

    def texto(self):
        c = str(abs(self.coeficiente))
        e = self.exponente
        if e >= 0:
            cuerpo = c + "0" * e
        elif len(c) + e > 0:
            cuerpo = c[:e] + "." + c[e:]
        else:
            cuerpo = "0." + "0" * (-e - len(c)) + c
        return ("-" if self.coeficiente < 0 else "") + cuerpo
