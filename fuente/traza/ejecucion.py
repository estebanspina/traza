# SPDX-License-Identifier: GPL-3.0-or-later
"""Máquina de continuaciones explícitas para el subconjunto D0 comprobado."""
from dataclasses import dataclass
from .analisis.sintactico import parsear
from .comprobacion import comprobar
from .errores import ErrorEntrada, LimiteRecursos
from .numeros import Numero

@dataclass(frozen=True, slots=True)
class ErrorValor:
    codigo: str
    condition_id: str | None = None
    location: str | None = None
    boundary: str | None = None

@dataclass(frozen=True, slots=True)
class Resultado:
    variante: str
    valor: object

@dataclass(frozen=True, slots=True)
class _Propagacion:
    resultado: Resultado

def contrato(nodo, frontera):
    p = nodo.rango.inicio
    return ErrorValor("ContractViolation", f"condicion:{p.desplazamiento}",
                      f"{nodo.rango.archivo}:{p.linea}:{p.columna}", frontera)

def operacion(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if isinstance(a, Numero):
        comparacion = a.comparar(b)
        return {"==": comparacion == 0, "!=": comparacion != 0,
                "<": comparacion < 0, "<=": comparacion <= 0,
                ">": comparacion > 0, ">=": comparacion >= 0}[op]
    if op == "==":
        return a == b
    if op == "!=":
        return a != b
    raise AssertionError("Operación no elaborada")

def predicado(n, candidato, entorno):
    if n.clase == "grupo":
        return predicado(n.datos[0], candidato, entorno)
    if n.clase == "literal":
        return Numero.desde_texto(n.datos[1]) if n.datos[0] == "NUMBER" else n.datos[1]
    if n.clase == "nombre":
        return candidato if n.datos[0] == "value" else entorno[n.datos[0]]
    if n.clase == "unario":
        op, hijo = n.datos
        valor = predicado(hijo, candidato, entorno)
        return not valor if op == "not" else -valor if op == "-" else valor
    op, a, b = n.datos
    x = predicado(a, candidato, entorno)
    if op == "and":
        return x and predicado(b, candidato, entorno)
    if op == "or":
        return x or predicado(b, candidato, entorno)
    return operacion(op, x, predicado(b, candidato, entorno))

class Maquina:
    def __init__(self, programa, max_pasos=100000):
        if max_pasos <= 0:
            raise ErrorEntrada("El presupuesto de pasos debe ser positivo.")
        self.programa = programa
        self.max_pasos = max_pasos
        self.eventos = []
        self.estados = dict(programa.obligaciones)

    def funcion(self, nombre, argumentos):
        f = self.programa.funciones[nombre]
        self.eventos.append(("entrada", nombre))
        env = dict(zip((x for x, _ in f.parametros), argumentos))
        valor = yield ("expresion", f.cuerpo, env)
        if isinstance(valor, _Propagacion):
            valor = valor.resultado
        t = f.retorno
        contenido = valor.valor if t.nombre == "Result" and valor.variante == "Ok" else valor
        exito = t.nombre != "Result" or valor.variante == "Ok"
        contrato_tipo = t.carga if t.nombre == "Result" else t
        if exito and contrato_tipo.condicion is not None and self.estados[nombre] == "desconocida":
            self.eventos.append(("control_retorno", nombre))
            if not predicado(contrato_tipo.condicion, contenido, env):
                return Resultado("Err", contrato(contrato_tipo.condicion, f"{nombre}:return"))
        return valor

    def expresion(self, n, env):
        k, d = n.clase, n.datos
        if k == "grupo":
            return (yield ("expresion", d[0], env))
        if k == "literal":
            return Numero.desde_texto(d[1]) if d[0] == "NUMBER" else d[1]
        if k == "nombre":
            return env[d[0]]
        if k == "ruta":
            return ErrorValor(d[1])
        if k == "bloque":
            local = dict(env)
            for nombre, _, hijo in d[0]:
                local[nombre] = yield ("expresion", hijo, local)
            return (yield ("expresion", d[1], local))
        if k == "unario":
            valor = yield ("expresion", d[1], env)
            return not valor if d[0] == "not" else -valor if d[0] == "-" else valor
        if k == "binario":
            op, a, b = d
            x = yield ("expresion", a, env)
            if op == "and" and not x:
                return False
            if op == "or" and x:
                return True
            y = yield ("expresion", b, env)
            return y if op in ("and", "or") else operacion(op, x, y)
        if k == "if":
            condicion = yield ("expresion", d[0], env)
            self.eventos.append(("rama", "verdadera" if condicion else "falsa"))
            return (yield ("expresion", d[1] if condicion else d[2], env))
        if k == "llamada":
            destino, nodos = d
            argumentos = []
            for hijo in nodos:
                argumentos.append((yield ("expresion", hijo, env)))
            if destino.clase == "ruta":
                return Resultado(destino.datos[1], argumentos[0])
            return (yield ("funcion", destino.datos[0], argumentos))
        if k == "propagar":
            valor = yield ("expresion", d[0], env)
            return valor.valor if valor.variante == "Ok" else _Propagacion(valor)
        if k == "check":
            valor = yield ("expresion", d[0], env)
            self.eventos.append(("control_check", str(n.rango.inicio.desplazamiento)))
            return (Resultado("Ok", valor) if predicado(d[1], valor, env)
                    else Resultado("Err", contrato(d[1], "check")))
        raise AssertionError("Nodo no comprobado")

    def ejecutar(self, nombre, argumentos):
        pila = [("funcion", self.funcion(nombre, argumentos))]
        enviado = None
        pasos = 0
        while pila:
            pasos += 1
            if pasos > self.max_pasos:
                raise LimiteRecursos("Presupuesto de pasos agotado; no es un Err de Traza.")
            try:
                solicitud = pila[-1][1].send(enviado)
            except StopIteration as terminado:
                pila.pop()
                enviado = terminado.value
                if isinstance(enviado, _Propagacion):
                    while pila and pila[-1][0] != "funcion":
                        pila.pop()
                continue
            clase, objetivo, contexto = solicitud
            generador = (self.funcion(objetivo, contexto) if clase == "funcion"
                         else self.expresion(objetivo, contexto))
            pila.append((clase, generador))
            enviado = None
        return enviado

def compilar(datos, archivo="<entrada>"):
    return comprobar(parsear(datos, archivo))

def convertir_entrada(valor, tipo):
    if tipo.nombre == "Number" and isinstance(valor, str):
        try:
            return Numero.desde_texto(valor)
        except ValueError:
            raise ErrorEntrada("Number requiere texto decimal válido.") from None
    if tipo.nombre == "Boolean" and type(valor) is bool:
        return valor
    if tipo.nombre == "Text" and isinstance(valor, str):
        return valor
    raise ErrorEntrada(f"Argumento externo no admitido para {tipo.nombre}.")

def ejecutar(programa, entrada, argumentos, max_pasos=100000):
    if entrada not in programa.funciones:
        raise ErrorEntrada("La función de entrada no existe.")
    funcion = programa.funciones[entrada]
    if not funcion.nodo.datos[0]:
        raise ErrorEntrada("La función de entrada debe ser pública.")
    if len(argumentos) != len(funcion.parametros):
        raise ErrorEntrada("Cantidad de argumentos externos incompatible.")
    valores = []
    for argumento, (_, tipo) in zip(argumentos, funcion.parametros):
        valor = convertir_entrada(argumento, tipo)
        if tipo.condicion is not None and not predicado(tipo.condicion, valor, {}):
            raise ErrorEntrada("El argumento externo no satisface su refinamiento.")
        valores.append(valor)
    maquina = Maquina(programa, max_pasos)
    try:
        valor = maquina.ejecutar(entrada, valores)
    except RecursionError:
        raise LimiteRecursos("Presupuesto de anidamiento de predicados agotado.") from None
    return valor, tuple(maquina.eventos)

def serializar(valor):
    if isinstance(valor, Numero):
        return {"tipo": "Number", "valor": valor.texto()}
    if isinstance(valor, Resultado):
        if valor.variante == "Err":
            error = valor.valor
            salida = {"variante": "Err", "codigo": error.codigo}
            for campo in ("condition_id", "location", "boundary"):
                if getattr(error, campo) is not None:
                    salida[campo] = getattr(error, campo)
            return salida
        return {"variante": "Ok", "valor": serializar(valor.valor)}
    if isinstance(valor, bytes):
        return {"tipo": "Bytes", "hex": valor.hex()}
    if type(valor) is bool:
        return {"tipo": "Boolean", "valor": valor}
    if isinstance(valor, str):
        return {"tipo": "Text", "valor": valor}
    if isinstance(valor, ErrorValor):
        return {"tipo": "Error", "codigo": valor.codigo}
    raise TypeError("Valor del anfitrión no perteneciente a Traza")
