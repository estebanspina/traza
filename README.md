# Traza

**Cada resultado, con fundamento.**

Lenguaje funcional en diseño con respuestas verificadas, aritmética decimal exacta y efectos explícitos. Surge del análisis crítico de C, COBOL y Haskell; su originalidad y sus ventajas deberán evaluarse con evidencia.

## Estado

PI01–PI02 completan la base reproducible y la preparación del catálogo: 116 reglas y 40 casos CF con sus variantes. Hay una primera implementación del **analizador léxico**, con tokens y diagnósticos. Todavía no hay parser, comprobador, intérprete ni compilador de Traza. Los casos semánticos permanecen pendientes.

## Principios

- Tipos generales y genéricos; especializaciones sólo con evidencia de mejora en ejecución o memoria.
- Respuestas con contratos demostrados o comprobados antes de entregar éxito.
- Composición de garantías sin repetir validaciones manuales que sigan siendo válidas.
- Evaluación estricta de izquierda a derecha y valores inmutables.
- Errores explícitos mediante Result; ausencia mediante Option.
- Number decimal exacto, redondeo solicitado y efectos declarados.

## Documentación

Consultar el [índice documental](documentacion/README.md), el [plan de implementación](documentacion/planificacion/07-plan-implementacion.md) y el [trabajo pendiente](documentacion/planificacion/trabajo-pendiente.md).

Los ocho documentos PDF existentes se incorporan como transcripciones textuales identificadas. Su normalización a Markdown y la incorporación de los binarios originales quedan pendientes. No se recrean tablas o código por inferencia.

## Preparación del desarrollo

Referencia reproducible: CPython 3.12.12, fijado en `.python-version`. No se necesitan dependencias externas. Ver [entorno de desarrollo](documentacion/desarrollo.md).

```sh
python --version
python herramientas/verificar.py
python herramientas/traza.py tokens ejemplos/contratos/bounded.traza
```

Las pruebas comprueban infraestructura, catálogo, análisis léxico e interfaz; **no ejecutan Traza**. El comando `tokens` produce JSON y no implica aceptación sintáctica. No existe todavía un comando `traza ejecutar` o `traza verificar`. Consultar [el lexer](documentacion/analizador-lexico.md) y [el catálogo](documentacion/conformidad/catalogo.md).

## Organización

| Ruta | Contenido |
| --- | --- |
| documentacion/ | Especificaciones, decisiones y planificación. |
| fuente/traza/ | Analizador léxico e interfaz del prototipo. |
| pruebas/ | Infraestructura y futuros casos ejecutables del lenguaje. |
| ejemplos/ | Programas de diseño con resultados esperados. |
| herramientas/ | Automatizaciones de desarrollo cuando se incorporen. |
| mediciones/ | Escenarios futuros de tiempo y memoria. |

Siguiente objetivo: completar la integración de PI03, comenzar el parser PI04 y avanzar hacia D0, donde `bounded(50)` deberá producir éxito y los valores fuera de rango deberán producir ContractViolation.

## Contribuciones y licencia

Ver [CONTRIBUIR.md](CONTRIBUIR.md) y [AGENTS.md](AGENTS.md).

El código original del proyecto se distribuye bajo **GNU GPL versión 3 o posterior**, identificador `GPL-3.0-or-later`. Consultar [LICENSE](LICENSE) y la [política de licencias](documentacion/licencias.md). No se concede automáticamente una excepción para un runtime futuro.
