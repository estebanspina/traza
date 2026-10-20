# SPDX-License-Identifier: GPL-3.0-or-later
"""Validación de preparación de pruebas, sin ejecutar el lenguaje."""
import json
from pathlib import Path
import re

FASES = {"analisis_sintactico", "comprobacion_estatica", "ejecucion", "proceso"}
MODALIDADES = {"programa", "vector", "propiedad", "protocolo"}

def exigir(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise ValueError(mensaje)

def leer_json(ruta: Path) -> dict:
    return json.loads(ruta.read_text(encoding="utf-8"))

def ruta_del_repositorio(raiz: Path, nombre: str) -> Path:
    exigir(isinstance(nombre, str) and bool(nombre), "Ruta no textual o vacía")
    relativa = Path(nombre)
    exigir(not relativa.is_absolute() and ".." not in relativa.parts, "Ruta fuera del repositorio")
    ruta = (raiz / relativa).resolve()
    exigir(ruta.is_relative_to(raiz.resolve()) and ruta.is_file(), f"Archivo inexistente: {nombre}")
    return ruta

def sin_flotantes(valor: object) -> None:
    exigir(not isinstance(valor, float), "No se admite float en expectativas")
    if isinstance(valor, dict):
        if valor.get("tipo") == "Number":
            exigir(isinstance(valor.get("valor"), str), "Number debe conservarse como texto")
            exigir(re.fullmatch(r"[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?",
                               valor["valor"]) is not None, "Literal Number inválido")
        for contenido in valor.values():
            sin_flotantes(contenido)
    elif isinstance(valor, list):
        for contenido in valor:
            sin_flotantes(contenido)

def validar(raiz: Path) -> tuple[int, int, int]:
    catalogo = leer_json(raiz / "pruebas/conformidad/catalogo.json")
    indice = leer_json(raiz / "documentacion/conformidad/reglas.json")
    exigir(catalogo["version_esquema"] == "0.1", "Versión de catálogo no soportada")
    exigir(indice["version_esquema"] == "0.1", "Versión de reglas no soportada")
    reglas = {regla["id"]: regla for regla in indice["reglas"]}
    exigir(len(reglas) == len(indice["reglas"]), "Reglas duplicadas")
    esperadas = {f"{prefijo}{i:02}" for prefijo, cantidad in
                 (("S", 24), ("T", 28), ("N", 32), ("G", 32))
                 for i in range(1, cantidad + 1)}
    exigir(set(reglas) == esperadas, "Catálogo de reglas incompleto")
    for regla in reglas.values():
        origen = ruta_del_repositorio(raiz, regla["documento"]).read_text(encoding="utf-8")
        patron = rf"^ {re.escape(regla['id'])} {re.escape(regla['titulo'])}$"
        exigir(re.search(patron, origen, re.MULTILINE) is not None,
               f"Regla sin título de origen: {regla['id']}")
        exigir(regla["estado"] == "pendiente", "No confundir catálogo con implementación")
    casos = catalogo["casos"]
    ids = [caso["id"] for caso in casos]
    exigir(len(ids) == len(set(ids)), "Casos duplicados")
    exigir(set(ids) == {f"CF{i:02}" for i in range(1, 41)}, "Faltan casos CF")
    total_variantes = 0
    relaciones = {regla: set() for regla in reglas}
    for caso in casos:
        exigir(caso["estado"] == "pendiente", "Conformidad aún no ejecutada")
        exigir(caso["fase_esperada"] in FASES, "Fase desconocida")
        exigir(caso["modalidad"] in MODALIDADES, "Modalidad desconocida")
        exigir(bool(caso["reglas"]), "Caso sin referencia de regla")
        for identificador in caso["reglas"]:
            exigir(identificador in reglas, "Referencia a regla inexistente")
            relaciones[identificador].add(caso["id"])
        variantes = caso["variantes"]
        exigir(isinstance(variantes, list) and bool(variantes), "Caso sin variantes")
        nombres = [v["nombre"] for v in variantes]
        exigir(len(nombres) == len(set(nombres)), "Variantes duplicadas")
        for variante in variantes:
            exigir(isinstance(variante["argumentos"], list), "Argumentos inválidos")
            exigir(isinstance(variante["esperado"], dict) and bool(variante["esperado"]),
                   "Variante sin oráculo")
            programa = variante.get("programa", caso.get("programa"))
            if caso["modalidad"] == "programa":
                exigir(programa is not None, "Variante sin programa")
            if programa is not None:
                ruta_del_repositorio(raiz, programa)
            sin_flotantes(variante)
        if caso["modalidad"] == "vector":
            exigir(bool(caso.get("operacion")), "Vector sin operación")
        if caso["modalidad"] == "propiedad":
            exigir(isinstance(caso["generador"]["semilla"], int), "Semilla no reproducible")
            exigir(caso["generador"]["cantidad"] > 0, "Generador vacío")
        if caso["modalidad"] == "protocolo":
            exigir(bool(caso.get("protocolo")), "Falta protocolo")
        total_variantes += len(variantes)
    for identificador, regla in reglas.items():
        exigir(set(regla["casos"]) == relaciones[identificador], "Trazabilidad no recíproca")
    return len(reglas), len(casos), total_variantes
