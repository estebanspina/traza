# SPDX-License-Identifier: GPL-3.0-or-later
"""Análisis léxico del subconjunto inicial."""
from .lexico import analizar
from .modelo import Diagnostico, ErrorLexico, Posicion, Rango, Token

__all__ = ["analizar", "Diagnostico", "ErrorLexico", "Posicion", "Rango", "Token"]
