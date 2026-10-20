# SPDX-License-Identifier: GPL-3.0-or-later
"""Datos inmutables de fuente, tokens y diagnósticos."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Posicion:
    desplazamiento: int
    linea: int
    columna: int

@dataclass(frozen=True, slots=True)
class Rango:
    archivo: str
    inicio: Posicion
    fin: Posicion

@dataclass(frozen=True, slots=True)
class Diagnostico:
    codigo: str
    mensaje: str
    rango: Rango

class ErrorLexico(Exception):
    """Fallo de análisis del anfitrión; no es un Error del programa Traza."""
    def __init__(self, diagnostico: Diagnostico):
        self.diagnostico = diagnostico
        super().__init__(
            f"{diagnostico.rango.archivo}:"
            f"{diagnostico.rango.inicio.linea}:"
            f"{diagnostico.rango.inicio.columna}: "
            f"{diagnostico.codigo}: {diagnostico.mensaje}"
        )

@dataclass(frozen=True, slots=True)
class Token:
    clase: str
    texto: str
    valor: str | bytes | None
    rango: Rango
