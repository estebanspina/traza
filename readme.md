# Traza

**Cada resultado, con fundamento.**

Lenguaje funcional en diseño con respuestas verificadas, aritmética decimal exacta y efectos explícitos. Surge del análisis crítico de C, COBOL y Haskell; su originalidad y sus ventajas deberán evaluarse con evidencia.

## Estado

PI01–PI02 completaron la preparación del repositorio y del catálogo de 116 reglas y 40 casos CF. Ya hay lexer, parser y **ejecución comprobada del subconjunto D0**, con funciones puras, aritmética exacta mínima y contratos de retorno.

El parser reconoce la gramática propuesta; el ejecutor soporta un subconjunto explícito. No hay todavía un compilador nativo, comprobador completo, efectos ni biblioteca numérica completa. Las características pendientes se informan con NI01.

Ver [parser y ejecución D0](documentacion/ejecucion-d0.md) y [contexto.md](contexto.md) para retomar el proyecto.

## Principios

- Tipos generales y genéricos; especializaciones sólo con evidencia de mejora en ejecución o memoria.
- Respuestas con contratos demostrados o comprobados antes de entregar éxito.
- Composición de garantías sin repetir validaciones manuales que sigan siendo válidas.
- Evaluación estricta de izquierda a derecha y valores inmutables.
- Errores explícitos mediante Result; ausencia mediante Option.
- Number decimal exacto, redondeo solicitado y efectos declarados.

## Documentación

Consultar el [índice documental](documentacion/readme.md), el [plan de implementación](documentacion/planificacion/07-plan-implementacion.md) y el [trabajo pendiente](documentacion/planificacion/trabajo-pendiente.md).

Los ocho documentos PDF existentes se incorporan como transcripciones textuales identificadas. Su normalización a Markdown y la incorporación de los binarios originales quedan pendientes. No se recrean tablas o código por inferencia.

## Preparación del desarrollo

Referencia reproducible: CPython 3.12.12, fijado en `.python-version`. No se necesitan dependencias externas. Ver [entorno de desarrollo](documentacion/desarrollo.md).

```sh
python --version
python herramientas/verificar.py
python herramientas/probar_d0.py
python herramientas/traza.py ejecutar ejemplos/contratos/bounded.traza --entrada bounded --argumentos '["50"]'
```

Las pruebas distinguen infraestructura, análisis y ejecución. D0 comprueba éxitos, violaciones de contrato y rechazo estático; eso no equivale a aprobar todos los casos CF. Consultar el [catálogo](documentacion/conformidad/catalogo.md) y el informe de `probar_d0.py`.

## Organización

| Ruta | Contenido |
| --- | --- |
| documentacion/ | Especificaciones, decisiones y planificación. |
| fuente/traza/ | Lexer, parser, comprobación y ejecución del subconjunto D0. |
| pruebas/ | Infraestructura y futuros casos ejecutables del lenguaje. |
| ejemplos/ | Programas de diseño con resultados esperados. |
| herramientas/ | Automatizaciones de desarrollo cuando se incorporen. |
| mediciones/ | Escenarios futuros de tiempo y memoria. |

Siguiente objetivo: ampliar resolución, comprobación y elaboración para más construcciones de la gramática, manteniendo D0 como regresión.

## Contribuciones y licencia

Ver [contribuir.md](contribuir.md) y [agents.md](agents.md).

El código original del proyecto se distribuye bajo **GNU GPL versión 3 o posterior**, identificador `GPL-3.0-or-later`. Consultar [license.md](license.md) y la [política de licencias](documentacion/licencias.md). No se concede automáticamente una excepción para un runtime futuro.
