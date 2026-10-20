# SPDX-License-Identifier: GPL-3.0-or-later
"""Descenso recursivo de la EBNF G23, sin comprobación de tipos."""
from .arbol import Nodo, Programa
from .lexico import analizar
from .modelo import Diagnostico, Rango
from ..errores import ErrorPrograma, LimiteRecursos

COMPARACIONES = frozenset(("==", "!=", "<", "<=", ">", ">="))

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def es(self, clase):
        return self.tokens[self.i].clase == clase

    def tomar(self, clase):
        if not self.es(clase):
            self.error(f"Se esperaba {clase}; se encontró {self.tokens[self.i].clase}.")
        token = self.tokens[self.i]
        self.i += 1
        return token

    def aceptar(self, clase):
        if self.es(clase):
            return self.tomar(clase)
        return None

    def error(self, mensaje, codigo="SG02"):
        raise ErrorPrograma(Diagnostico(codigo, mensaje, self.tokens[self.i].rango),
                            "analisis_sintactico")

    def nodo(self, inicio, clase, *datos):
        return Nodo(clase, tuple(datos),
                    Rango(self.tokens[inicio].rango.archivo,
                          self.tokens[inicio].rango.inicio,
                          self.tokens[max(inicio, self.i - 1)].rango.fin))

    def lista(self, elemento, cierre, permitir_vacia=True):
        elementos = []
        if permitir_vacia and self.es(cierre):
            self.tomar(cierre)
            return tuple(elementos)
        elementos.append(elemento())
        while self.aceptar(","):
            elementos.append(elemento())
        self.tomar(cierre)
        return tuple(elementos)

    def genericos(self):
        if not self.aceptar("<"):
            return ()
        return self.lista(lambda: self.tomar("IDENT").texto, ">", False)

    def parametro(self):
        nombre = self.tomar("IDENT").texto
        self.tomar(":")
        return nombre, self.tipo()

    def parametros(self):
        self.tomar("(")
        return self.lista(self.parametro, ")")

    def efectos(self):
        if not self.aceptar("!"):
            return ()
        self.tomar("{")
        return self.lista(lambda: self.tomar("IDENT").texto, "}")

    def programa(self):
        declaraciones = []
        while not self.es("EOF"):
            inicio = self.i
            publica = bool(self.aceptar("pub"))
            if self.aceptar("type"):
                nombre = self.tomar("IDENT").texto
                genericos = self.genericos()
                self.tomar("=")
                tipo = self.tipo()
                self.tomar(";")
                declaraciones.append(self.nodo(inicio, "alias", publica, nombre, genericos, tipo))
            else:
                self.tomar("fn")
                nombre = self.tomar("IDENT").texto
                genericos = self.genericos()
                parametros = self.parametros()
                self.tomar("->")
                retorno = self.tipo()
                efectos = self.efectos()
                cuerpo = self.bloque()
                declaraciones.append(self.nodo(
                    inicio, "funcion", publica, nombre, genericos, parametros,
                    retorno, efectos, cuerpo))
        self.tomar("EOF")
        return Programa(tuple(declaraciones))

    def campo_tipo(self):
        nombre = self.tomar("IDENT").texto
        self.tomar(":")
        return nombre, self.tipo()

    def variante(self):
        nombre = self.tomar("IDENT").texto
        carga = None
        if self.aceptar("("):
            carga = self.tipo()
            self.tomar(")")
        return nombre, carga

    def tipo(self):
        inicio = self.i
        if self.aceptar("{"):
            base = self.nodo(inicio, "tipo_registro", self.lista(self.campo_tipo, "}"))
        elif self.aceptar("variant"):
            self.tomar("{")
            base = self.nodo(inicio, "tipo_variante", self.lista(self.variante, "}", False))
        elif self.aceptar("("):
            self.tomar("fn")
            parametros = self.parametros()
            self.tomar("->")
            retorno = self.tipo()
            efectos = self.efectos()
            self.tomar(")")
            base = self.nodo(inicio, "tipo_funcion", parametros, retorno, efectos)
        else:
            nombre = self.tomar("IDENT").texto
            argumentos = ()
            if self.aceptar("<"):
                argumentos = self.lista(self.tipo, ">", False)
            base = self.nodo(inicio, "tipo", nombre, argumentos)
        if self.aceptar("where"):
            self.tomar("{")
            condicion = self.expresion()
            self.tomar("}")
            return self.nodo(inicio, "refinado", base, condicion)
        return base

    def bloque(self):
        inicio = self.i
        self.tomar("{")
        vinculaciones = []
        while self.aceptar("let"):
            nombre = self.tomar("IDENT").texto
            tipo = self.tipo() if self.aceptar(":") else None
            self.tomar("=")
            valor = self.expresion()
            if not self.es(";"):
                self.error("Falta punto y coma después de let.", "SG03")
            self.tomar(";")
            vinculaciones.append((nombre, tipo, valor))
        if self.es("}"):
            self.error("El bloque requiere una expresión final.", "SG03")
        final = self.expresion()
        if self.es(";"):
            self.error("La expresión final no lleva punto y coma.", "SG03")
        self.tomar("}")
        return self.nodo(inicio, "bloque", tuple(vinculaciones), final)

    def expresion(self):
        inicio = self.i
        if self.aceptar("if"):
            self.tomar("(")
            condicion = self.expresion()
            self.tomar(")")
            verdadero = self.bloque()
            self.tomar("else")
            falso = self.bloque()
            return self.nodo(inicio, "if", condicion, verdadero, falso)
        if self.aceptar("match"):
            self.tomar("(")
            sujeto = self.expresion()
            self.tomar(")")
            self.tomar("{")
            brazos = [self.brazo()]
            while self.aceptar(","):
                if self.es("}"):
                    break
                brazos.append(self.brazo())
            self.tomar("}")
            return self.nodo(inicio, "match", sujeto, tuple(brazos))
        if self.aceptar("check"):
            self.tomar("(")
            valor = self.expresion()
            self.tomar(")")
            self.tomar("where")
            self.tomar("{")
            condicion = self.expresion()
            self.tomar("}")
            return self.nodo(inicio, "check", valor, condicion)
        if self.aceptar("fn"):
            parametros = self.parametros()
            self.tomar("->")
            retorno = self.tipo()
            efectos = self.efectos()
            cuerpo = self.bloque()
            return self.nodo(inicio, "lambda", parametros, retorno, efectos, cuerpo)
        return self.binario(0)

    def binario(self, nivel):
        niveles = (("or",), ("and",), tuple(COMPARACIONES), ("+", "-"), ("*", "/"))
        if nivel == len(niveles):
            return self.unario()
        inicio = self.i
        izquierdo = self.binario(nivel + 1)
        while self.tokens[self.i].clase in niveles[nivel]:
            operador = self.tokens[self.i].clase
            self.tomar(operador)
            derecho = self.binario(nivel + 1)
            izquierdo = self.nodo(inicio, "binario", operador, izquierdo, derecho)
            if nivel == 2:
                if self.tokens[self.i].clase in COMPARACIONES:
                    self.error("No se admiten comparaciones encadenadas.", "SG04")
                break
        return izquierdo

    def unario(self):
        inicio = self.i
        if self.tokens[self.i].clase in ("+", "-", "not"):
            operador = self.tokens[self.i].clase
            self.tomar(operador)
            return self.nodo(inicio, "unario", operador, self.unario())
        return self.sufijos()

    def sufijos(self):
        inicio = self.i
        valor = self.primario()
        while True:
            if self.aceptar("("):
                valor = self.nodo(inicio, "llamada", valor, self.lista(self.expresion, ")"))
            elif self.aceptar("."):
                valor = self.nodo(inicio, "campo", valor, self.tomar("IDENT").texto)
            elif self.aceptar("::<"):
                valor = self.nodo(inicio, "instancia", valor, self.lista(self.tipo, ">", False))
            elif self.aceptar("?"):
                valor = self.nodo(inicio, "propagar", valor)
            else:
                return valor

    def campo_valor(self):
        nombre = self.tomar("IDENT").texto
        self.tomar(":")
        return nombre, self.expresion()

    def primario(self):
        inicio = self.i
        clase = self.tokens[self.i].clase
        if clase in ("NUMBER", "STRING", "BYTES"):
            token = self.tomar(clase)
            return self.nodo(inicio, "literal", clase, token.valor)
        if clase in ("true", "false"):
            self.tomar(clase)
            return self.nodo(inicio, "literal", "Boolean", clase == "true")
        if self.aceptar("value"):
            return self.nodo(inicio, "nombre", "value")
        if self.aceptar("("):
            valor = self.expresion()
            self.tomar(")")
            return self.nodo(inicio, "grupo", valor)
        if self.aceptar("["):
            return self.nodo(inicio, "lista", self.lista(self.expresion, "]"))
        if self.aceptar("record"):
            self.tomar("{")
            return self.nodo(inicio, "registro", self.lista(self.campo_valor, "}"))
        if clase == "IDENT":
            primero = self.tomar("IDENT").texto
            if self.aceptar("::"):
                return self.nodo(inicio, "ruta", primero, self.tomar("IDENT").texto)
            return self.nodo(inicio, "nombre", primero)
        self.error("Se esperaba una expresión.")

    def patron(self):
        inicio = self.i
        if self.aceptar("_"):
            return self.nodo(inicio, "comodin")
        if self.aceptar("-"):
            return self.nodo(inicio, "patron_literal", "NUMBER",
                             "-" + self.tomar("NUMBER").texto)
        clase = self.tokens[self.i].clase
        if clase in ("NUMBER", "STRING", "true", "false"):
            token = self.tomar(clase)
            return self.nodo(inicio, "patron_literal", clase, token.valor)
        nombre = self.tomar("IDENT").texto
        if self.aceptar("::"):
            etiqueta = self.tomar("IDENT").texto
            carga = None
            if self.aceptar("("):
                carga = self.patron()
                self.tomar(")")
            return self.nodo(inicio, "patron_variante", nombre, etiqueta, carga)
        return self.nodo(inicio, "captura", nombre)

    def brazo(self):
        patron = self.patron()
        self.tomar("=>")
        return patron, self.bloque()

def parsear(datos: bytes, archivo: str = "<entrada>") -> Programa:
    try:
        return Parser(analizar(datos, archivo)).programa()
    except RecursionError:
        raise LimiteRecursos("Fuente demasiado anidada para el parser de referencia.") from None
