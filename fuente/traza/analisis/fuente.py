# SPDX-License-Identifier: GPL-3.0-or-later
"""UTF-8 estricto y mapa de escalares a desplazamientos de bytes."""
from dataclasses import dataclass
from .modelo import Diagnostico, ErrorLexico, Posicion, Rango

def _posiciones(texto: str) -> tuple[Posicion, ...]:
    posiciones = []
    desplazamiento, linea, columna = 0, 1, 1
    for caracter in texto:
        posiciones.append(Posicion(desplazamiento, linea, columna))
        desplazamiento += len(caracter.encode("utf-8"))
        if caracter == "\n":
            linea, columna = linea + 1, 1
        else:
            columna += 1
    posiciones.append(Posicion(desplazamiento, linea, columna))
    return tuple(posiciones)

@dataclass(frozen=True, slots=True)
class Fuente:
    texto: str
    archivo: str
    posiciones: tuple[Posicion, ...]

    @classmethod
    def desde_bytes(cls, datos: bytes, archivo: str) -> "Fuente":
        if not isinstance(datos, bytes):
            raise TypeError("La fuente debe recibirse como bytes UTF-8.")
        try:
            texto = datos.decode("utf-8", errors="strict")
        except UnicodeDecodeError as error:
            prefijo = datos[:error.start].decode("utf-8", errors="strict")
            inicio = _posiciones(prefijo)[-1]
            # La secuencia inválida no representa ningún escalar: la columna
            # señala su inicio y el rango binario identifica todos sus bytes.
            fin = Posicion(error.end, inicio.linea, inicio.columna)
            raise ErrorLexico(Diagnostico(
                "SG01", "Secuencia UTF-8 inválida.", Rango(archivo, inicio, fin)
            )) from None
        fuente = cls(texto, archivo, _posiciones(texto))
        for indice, caracter in enumerate(texto):
            if caracter == "\r" and texto[indice:indice + 2] != "\r\n":
                fuente.fallar("Final de línea CR aislado; usar LF o CRLF.", indice, indice + 1)
        return fuente

    def rango(self, inicio: int, fin: int) -> Rango:
        return Rango(self.archivo, self.posiciones[inicio], self.posiciones[fin])

    def fallar(self, mensaje: str, inicio: int, fin: int) -> None:
        raise ErrorLexico(Diagnostico("SG01", mensaje, self.rango(inicio, fin)))
