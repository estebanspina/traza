# SPDX-License-Identifier: GPL-3.0-or-later
"""Árbol sintáctico inmutable; sus nodos conservan rangos de fuente."""
from dataclasses import dataclass
from .modelo import Rango

@dataclass(frozen=True, slots=True)
class Nodo:
    clase: str
    datos: tuple
    rango: Rango

@dataclass(frozen=True, slots=True)
class Programa:
    declaraciones: tuple[Nodo, ...]
