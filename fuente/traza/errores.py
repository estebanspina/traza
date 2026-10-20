# SPDX-License-Identifier: GPL-3.0-or-later
"""Errores de fases y límites externos, separados de Result del lenguaje."""
from .analisis.modelo import Diagnostico

class ErrorPrograma(Exception):
    def __init__(self, diagnostico: Diagnostico, fase: str):
        self.diagnostico = diagnostico
        self.fase = fase
        super().__init__(diagnostico.mensaje)

class LimiteRecursos(Exception):
    """Presupuesto agotado: no es un fallo numérico ni un Err de Traza."""

class ErrorEntrada(Exception):
    """Argumentos externos inválidos antes de invocar una función."""
