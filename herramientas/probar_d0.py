# SPDX-License-Identifier: GPL-3.0-or-later
"""Ejecuta el manifiesto D0 real y publica un informe JSON reproducible."""
import json
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fuente"))
from traza.ejecucion import compilar, ejecutar, serializar
from traza.errores import ErrorPrograma
from traza.numeros import Numero

def coincide(obtenido, esperado):
    if isinstance(esperado, dict):
        if esperado.get("tipo") == "Number":
            return (isinstance(obtenido, dict) and obtenido.get("tipo") == "Number"
                    and Numero.desde_texto(obtenido["valor"]) == Numero.desde_texto(esperado["valor"]))
        if not isinstance(obtenido, dict):
            return False
        for campo, valor in esperado.items():
            if campo == "campos_requeridos":
                if not all(obtenido.get(nombre) for nombre in valor):
                    return False
            elif campo not in obtenido or not coincide(obtenido[campo], valor):
                return False
        return True
    return obtenido == esperado

def probar(raiz=RAIZ):
    manifiesto = json.loads(
        (raiz / "pruebas/conformidad/manifiestos/d0.json").read_text(encoding="utf-8"))
    informes = []
    for caso in manifiesto["casos"]:
        ruta = raiz / caso["programa"]
        eventos = ()
        try:
            programa = compilar(ruta.read_bytes(), caso["programa"])
        except ErrorPrograma as error:
            fase = error.fase
            obtenido = {"diagnostico": error.diagnostico.codigo}
        else:
            if caso["fase_esperada"] == "comprobacion_estatica":
                fase, obtenido = "comprobacion_estatica", {"aceptado": True}
            else:
                fase = "ejecucion"
                valor, eventos = ejecutar(programa, caso["entrada"],
                                         [a["valor"] for a in caso["argumentos"]])
                obtenido = serializar(valor)
        aprobado = fase == caso["fase_esperada"] and coincide(obtenido, caso["esperado"])
        informes.append({"id": caso["id"], "estado": "aprobado" if aprobado else "fallido",
                         "fase": fase, "obtenido": obtenido, "eventos": eventos})
    return {"version_especificacion": manifiesto["version_especificacion"],
            "alcance": "Manifiesto D0; no es la batería completa CF",
            "aprobados": sum(i["estado"] == "aprobado" for i in informes),
            "total": len(informes), "casos": informes}

def main():
    informe = probar()
    print(json.dumps(informe, ensure_ascii=False))
    return 0 if informe["total"] and informe["aprobados"] == informe["total"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
