# SPDX-License-Identifier: GPL-3.0-or-later
"""Comprobación conservadora del subconjunto ejecutable D0."""
from dataclasses import dataclass, replace
from types import MappingProxyType
from .analisis.arbol import Nodo, Programa
from .analisis.modelo import Diagnostico
from .errores import ErrorPrograma, LimiteRecursos
from .numeros import Numero

PREDEFINIDOS = frozenset("Number Boolean Text Bytes List Option Result Error Rounding".split())
ERRORES = frozenset(("InvalidInput", "DivisionByZero", "InexactResult",
                    "InvalidNumericOperand", "InvalidScale", "InvalidRoundingMode",
                    "InvalidNumericText", "NotRepresentable"))

def fallo(nodo, codigo, mensaje):
    raise ErrorPrograma(Diagnostico(codigo, mensaje, nodo.rango), "comprobacion_estatica")

def no_implementado(nodo, mensaje):
    fallo(nodo, "NI01", mensaje)

def clave(nodo):
    if isinstance(nodo, Nodo):
        return (nodo.clase, tuple(clave(x) for x in nodo.datos))
    if isinstance(nodo, tuple):
        return tuple(clave(x) for x in nodo)
    return nodo

@dataclass(frozen=True)
class Tipo:
    nombre: str
    carga: object = None
    condicion: Nodo | None = None

@dataclass(frozen=True)
class Info:
    tipo: Tipo
    inferior: Numero | None = None
    superior: Numero | None = None
    constante: object = None
    exito: object = None
    variante: str | None = None
    garantias: tuple = ()

@dataclass(frozen=True)
class Funcion:
    nodo: Nodo
    parametros: tuple
    retorno: Tipo
    cuerpo: Nodo

@dataclass(frozen=True)
class Comprobado:
    programa: Programa
    funciones: object
    obligaciones: tuple

def tipo(n):
    if n.clase == "refinado":
        base = tipo(n.datos[0])
        if base.nombre != "Number":
            no_implementado(n, "Por ahora sólo se ejecutan refinamientos de Number.")
        return replace(base, condicion=n.datos[1])
    if n.clase != "tipo":
        no_implementado(n, "Tipo estructural o función aún no ejecutable.")
    nombre, argumentos = n.datos
    if nombre == "Result":
        if len(argumentos) != 2 or tipo(argumentos[1]) != Tipo("Error"):
            fallo(n, "D01", "Se requiere Result<T, Error> en este subconjunto.")
        carga = tipo(argumentos[0])
        if carga.nombre not in ("Number", "Boolean", "Text", "Bytes"):
            no_implementado(n, "Result anidado aún no ejecutable.")
        return Tipo("Result", carga)
    if nombre not in ("Number", "Boolean", "Text", "Bytes", "Error"):
        no_implementado(n, f"Tipo {nombre} aún no ejecutable.")
    if argumentos:
        fallo(n, "D01", f"{nombre} no recibe argumentos de tipo.")
    return Tipo(nombre)

def min_num(a, b):
    return a if a.comparar(b) <= 0 else b

def max_num(a, b):
    return a if a.comparar(b) >= 0 else b

def info_firma(t):
    if t.nombre == "Result":
        return Info(t, exito=info_firma(t.carga), variante="Mixto")
    i = Info(t)
    if t.condicion is not None:
        i = replace(i, garantias=(clave(t.condicion),))
        i = aplicar_intervalo(i, t.condicion)
    return i

def numero_constante(n):
    if n.clase == "grupo":
        return numero_constante(n.datos[0])
    if n.clase == "literal" and n.datos[0] == "NUMBER":
        return Numero.desde_texto(n.datos[1])
    if n.clase == "unario" and n.datos[0] in ("+", "-"):
        v = numero_constante(n.datos[1])
        return v if n.datos[0] == "+" or v is None else -v
    return None

def aplicar_intervalo(i, p):
    if p.clase == "grupo":
        return aplicar_intervalo(i, p.datos[0])
    if p.clase == "binario":
        op, a, b = p.datos
        if op == "and":
            return aplicar_intervalo(aplicar_intervalo(i, a), b)
        if a.clase == "nombre" and a.datos[0] == "value":
            c = numero_constante(b)
            if c is not None:
                if op in (">", ">=", "=="):
                    i = replace(i, inferior=c if i.inferior is None else max_num(i.inferior, c))
                if op in ("<", "<=", "=="):
                    i = replace(i, superior=c if i.superior is None else min_num(i.superior, c))
    return i

def validar_predicado(n, entorno):
    if n.clase == "grupo":
        return validar_predicado(n.datos[0], entorno)
    if n.clase == "literal":
        if n.datos[0] in ("NUMBER", "Boolean"):
            return "Number" if n.datos[0] == "NUMBER" else "Boolean"
    if n.clase == "nombre":
        if n.datos[0] in entorno and entorno[n.datos[0]].tipo.nombre == "Number":
            return "Number"
    if n.clase == "unario":
        op, hijo = n.datos
        t = validar_predicado(hijo, entorno)
        if op == "not" and t == "Boolean":
            return "Boolean"
        if op in ("+", "-") and numero_constante(hijo) is not None:
            return "Number"
    if n.clase == "binario":
        op, a, b = n.datos
        ta, tb = validar_predicado(a, entorno), validar_predicado(b, entorno)
        if op in ("and", "or") and ta == tb == "Boolean":
            return "Boolean"
        if op in ("<", "<=", ">", ">=", "==", "!=") and ta == tb == "Number":
            return "Boolean"
    if n.clase == "llamada" and n.datos[0].clase == "nombre":
        if n.datos[0].datos[0] in ("is_integer", "is_quantized", "length"):
            no_implementado(n, "Predicado incorporado todavía no ejecutable.")
    fallo(n, "D03", "Predicado fuera del subconjunto puro de comparaciones e intervalos.")

def intervalo(n, entorno):
    if n.clase == "grupo":
        return intervalo(n.datos[0], entorno)
    v = numero_constante(n)
    if v is not None:
        return v, v
    if n.clase == "nombre" and n.datos[0] in entorno:
        i = entorno[n.datos[0]]
        return i.inferior, i.superior
    return None, None

def concluir(p, candidato, entorno):
    if clave(p) in candidato.garantias:
        return True
    contexto = {**entorno, "value": candidato}
    def decidir(n):
        if n.clase == "grupo":
            return decidir(n.datos[0])
        if n.clase == "literal" and n.datos[0] == "Boolean":
            return n.datos[1]
        if n.clase == "unario" and n.datos[0] == "not":
            x = decidir(n.datos[1])
            return None if x is None else not x
        if n.clase != "binario":
            return None
        op, a, b = n.datos
        if op in ("and", "or"):
            x, y = decidir(a), decidir(b)
            if op == "and":
                return False if x is False or y is False else True if x is y is True else None
            return True if x is True or y is True else False if x is y is False else None
        ai, ass = intervalo(a, contexto)
        bi, bs = intervalo(b, contexto)
        if op in (">", ">="):
            ai, ass, bi, bs = bi, bs, ai, ass
            op = "<" if op == ">" else "<="
        if op in ("<", "<="):
            if ass is not None and bi is not None:
                d = ass.comparar(bi)
                if d < 0 or op == "<=" and d == 0:
                    return True
            if ai is not None and bs is not None:
                d = ai.comparar(bs)
                if d > 0 or op == "<" and d == 0:
                    return False
        if op in ("==", "!="):
            exactos = (ai is not None and ass is not None and bi is not None and bs is not None
                       and ai == ass and bi == bs)
            distintos = ((ass is not None and bi is not None and ass.comparar(bi) < 0)
                         or (bs is not None and ai is not None and bs.comparar(ai) < 0))
            r = ai == bi if exactos else False if distintos else None
            return None if r is None else r if op == "==" else not r
        return None
    return decidir(p)

class Comprobador:
    def __init__(self, programa):
        self.programa = programa
        self.funciones = {}
        self.obligaciones = []

    def registrar(self):
        for n in self.programa.declaraciones:
            if n.clase != "funcion":
                no_implementado(n, "Aliases aún no ejecutables; sí se analizan sintácticamente.")
            publica, nombre, genericos, parametros, retorno, efectos, cuerpo = n.datos
            if nombre in self.funciones or nombre in PREDEFINIDOS:
                fallo(n, "SG05", "Nombre superior duplicado o reservado.")
            if genericos or efectos:
                no_implementado(n, "Funciones genéricas o con efectos aún no ejecutables.")
            nombres = [p[0] for p in parametros]
            if len(set(nombres)) != len(nombres) or set(nombres) & PREDEFINIDOS:
                fallo(n, "SG05", "Parámetro duplicado o reservado.")
            self.funciones[nombre] = Funcion(
                n, tuple((x, tipo(t)) for x, t in parametros), tipo(retorno), cuerpo)
        for funcion in self.funciones.values():
            contexto = {x: Info(Tipo(t.nombre)) for x, t in funcion.parametros}
            for _, t in funcion.parametros:
                if t.condicion is not None:
                    self.predicado(t.condicion, contexto)
            t = funcion.retorno.carga if funcion.retorno.nombre == "Result" else funcion.retorno
            if t.condicion is not None:
                self.predicado(t.condicion, contexto)

    def predicado(self, p, entorno):
        def revisar(n):
            if isinstance(n, Nodo):
                if n.clase == "nombre" and n.datos[0] != "value":
                    no_implementado(n, "Relaciones de contrato con otros parámetros aún no ejecutables.")
                for dato in n.datos:
                    revisar(dato)
            elif isinstance(n, tuple):
                for dato in n:
                    revisar(dato)
        if validar_predicado(p, {**entorno, "value": Info(Tipo("Number"))}) != "Boolean":
            fallo(p, "D03", "El predicado debe producir Boolean.")
        revisar(p)

    def compatible(self, i, t, n, entorno, retorno=False):
        if i.tipo.nombre != t.nombre:
            fallo(n, "D01", f"Se esperaba {t.nombre}; se obtuvo {i.tipo.nombre}.")
        if t.nombre == "Result":
            if i.exito is not None:
                return self.compatible(i.exito, t.carga, n, entorno, retorno)
            return True
        if t.condicion is None:
            return True
        r = concluir(t.condicion, i, entorno)
        if not retorno and r is not True:
            fallo(n, "D04", "La precondición requiere una comprobación explícita.")
        return r

    def inferir(self, n, env, retorno, parametros_bloque=()):
        k, d = n.clase, n.datos
        if k == "grupo":
            return self.inferir(d[0], env, retorno)
        if k == "literal":
            etiqueta, valor = d
            t = {"NUMBER": "Number", "STRING": "Text", "BYTES": "Bytes",
                 "Boolean": "Boolean"}[etiqueta]
            if t == "Number":
                v = Numero.desde_texto(valor)
                return Info(Tipo(t), v, v, v)
            return Info(Tipo(t), constante=valor)
        if k == "nombre":
            if d[0] not in env:
                fallo(n, "SG05", f"Nombre no vinculado: {d[0]}.")
            return env[d[0]]
        if k == "ruta":
            if d[0] == "Error" and d[1] in ERRORES:
                return Info(Tipo("Error"))
            fallo(n, "D01", "Constructor desconocido o utilizado sin su carga.")
        if k == "bloque":
            local, vistos = dict(env), set(parametros_bloque)
            for nombre, anotacion, valor in d[0]:
                if nombre in vistos or nombre in PREDEFINIDOS:
                    fallo(valor, "SG05", "Vinculación duplicada o reservada.")
                vistos.add(nombre)
                i = self.inferir(valor, local, retorno)
                if anotacion is not None:
                    self.compatible(i, tipo(anotacion), valor, local)
                local[nombre] = i
            return self.inferir(d[1], local, retorno)
        if k == "unario":
            op, hijo = d
            i = self.inferir(hijo, env, retorno)
            esperado = "Boolean" if op == "not" else "Number"
            self.compatible(i, Tipo(esperado), n, env)
            if op == "not":
                return Info(Tipo("Boolean"), constante=None if i.constante is None else not i.constante)
            if op == "+":
                return i
            return Info(Tipo("Number"), -i.superior if i.superior is not None else None,
                        -i.inferior if i.inferior is not None else None)
        if k == "binario":
            op, a, b = d
            x, y = self.inferir(a, env, retorno), self.inferir(b, env, retorno)
            if op == "/":
                no_implementado(n, "División aún no ejecutable; requiere Result numérico.")
            if op in ("and", "or"):
                self.compatible(x, Tipo("Boolean"), a, env)
                self.compatible(y, Tipo("Boolean"), b, env)
                return Info(Tipo("Boolean"))
            if op in ("+", "-", "*", "<", "<=", ">", ">="):
                self.compatible(x, Tipo("Number"), a, env)
                self.compatible(y, Tipo("Number"), b, env)
            elif op in ("==", "!="):
                if x.tipo.nombre != y.tipo.nombre or x.tipo.nombre not in ("Number", "Boolean", "Text", "Bytes"):
                    fallo(n, "D01", "Igualdad requiere primitivas de la misma categoría.")
            if op in ("==", "!=", "<", "<=", ">", ">="):
                return Info(Tipo("Boolean"))
            if op == "+":
                return Info(Tipo("Number"),
                            x.inferior + y.inferior if x.inferior is not None and y.inferior is not None else None,
                            x.superior + y.superior if x.superior is not None and y.superior is not None else None)
            if op == "-":
                return Info(Tipo("Number"),
                            x.inferior - y.superior if x.inferior is not None and y.superior is not None else None,
                            x.superior - y.inferior if x.superior is not None and y.inferior is not None else None)
            if all(v is not None for v in (x.inferior, x.superior, y.inferior, y.superior)):
                valores = [a * b for a in (x.inferior, x.superior) for b in (y.inferior, y.superior)]
                inferior = superior = valores[0]
                for v in valores[1:]:
                    inferior, superior = min_num(inferior, v), max_num(superior, v)
                return Info(Tipo("Number"), inferior, superior)
            return Info(Tipo("Number"))
        if k == "if":
            condicion = self.inferir(d[0], env, retorno)
            self.compatible(condicion, Tipo("Boolean"), d[0], env)
            a, b = self.inferir(d[1], env, retorno), self.inferir(d[2], env, retorno)
            if a.tipo.nombre != b.tipo.nombre:
                fallo(n, "D01", "Las ramas tienen categorías incompatibles.")
            if condicion.constante is not None:
                return a if condicion.constante else b
            if a.tipo.nombre == "Result":
                if a.exito is None:
                    return replace(b, variante="Mixto")
                if b.exito is None:
                    return replace(a, variante="Mixto")
                carga = self.unir(a.exito, b.exito, n)
                return Info(Tipo("Result", carga.tipo), exito=carga, variante="Mixto")
            return self.unir(a, b, n)
        if k == "llamada":
            destino, argumentos = d
            valores = [self.inferir(a, env, retorno) for a in argumentos]
            if destino.clase == "ruta" and destino.datos[0] == "Result":
                if len(valores) != 1 or destino.datos[1] not in ("Ok", "Err"):
                    fallo(n, "D01", "Constructor Result inválido.")
                if destino.datos[1] == "Err":
                    self.compatible(valores[0], Tipo("Error"), n, env)
                    return Info(Tipo("Result"), variante="Err")
                return Info(Tipo("Result", valores[0].tipo), exito=valores[0], variante="Ok")
            if destino.clase != "nombre" or destino.datos[0] not in self.funciones:
                fallo(n, "SG05", "Función no declarada en el subconjunto ejecutable.")
            if destino.datos[0] in env:
                fallo(n, "D01", "El nombre de llamada está oculto por un valor local.")
            funcion = self.funciones[destino.datos[0]]
            if len(valores) != len(funcion.parametros):
                fallo(n, "D01", "Cantidad de argumentos incompatible.")
            for valor, (_, esperado) in zip(valores, funcion.parametros):
                self.compatible(valor, esperado, n, env)
            return info_firma(funcion.retorno)
        if k == "propagar":
            if retorno.nombre != "Result":
                fallo(n, "D01", "? requiere una función con retorno Result compatible.")
            i = self.inferir(d[0], env, retorno)
            if i.tipo.nombre != "Result":
                fallo(n, "D01", "? sólo opera sobre Result.")
            if i.exito is None:
                no_implementado(n, "Propagación sin tipo de éxito inferible; anotar una función auxiliar.")
            return i.exito
        if k == "check":
            i = self.inferir(d[0], env, retorno)
            self.compatible(i, Tipo("Number"), d[0], env)
            self.predicado(d[1], env)
            refinado = replace(i, garantias=(*i.garantias, clave(d[1])))
            refinado = aplicar_intervalo(refinado, d[1])
            return Info(Tipo("Result", refinado.tipo), exito=refinado, variante="Mixto")
        no_implementado(n, f"Construcción {k} analizada, pero aún no ejecutable.")

    def unir(self, a, b, n):
        if a.tipo.nombre != b.tipo.nombre:
            fallo(n, "D01", "Ramas de éxito incompatibles.")
        return Info(Tipo(a.tipo.nombre),
                    min_num(a.inferior, b.inferior) if a.inferior is not None and b.inferior is not None else None,
                    max_num(a.superior, b.superior) if a.superior is not None and b.superior is not None else None,
                    garantias=tuple(x for x in a.garantias if x in b.garantias))

    def retornos(self, n, env, funcion):
        if n.clase == "bloque":
            local = dict(env)
            for nombre, _, valor in n.datos[0]:
                local[nombre] = self.inferir(valor, local, funcion.retorno)
            return self.retornos(n.datos[1], local, funcion)
        if n.clase == "if":
            condicion, a, b = n.datos
            i = self.inferir(condicion, env, funcion.retorno)
            if i.constante is not None:
                return self.retornos(a if i.constante else b, env, funcion)
            return self.retornos(a, env, funcion) + self.retornos(b, env, funcion)
        i = self.inferir(n, env, funcion.retorno)
        r = self.compatible(i, funcion.retorno, n, env, retorno=True)
        if r is False:
            fallo(n, "D05", "Retorno exitoso demostrado inválido.")
        if r is None and funcion.retorno.nombre != "Result":
            fallo(n, "D06", "El retorno desconocido exige Result compatible.")
        return [r]

    def comprobar(self):
        self.registrar()
        for nombre, funcion in self.funciones.items():
            env = {x: info_firma(t) for x, t in funcion.parametros}
            self.inferir(funcion.cuerpo, env, funcion.retorno, tuple(env))
            estados = self.retornos(funcion.cuerpo, env, funcion)
            estado = "desconocida" if any(r is None for r in estados) else "demostrada"
            self.obligaciones.append((nombre, estado))
        return Comprobado(self.programa, MappingProxyType(dict(self.funciones)),
                          tuple(self.obligaciones))

def comprobar(programa):
    try:
        return Comprobador(programa).comprobar()
    except RecursionError:
        raise LimiteRecursos("Programa demasiado anidado para el comprobador inicial.") from None
