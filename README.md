# Traza

**Cada resultado, con fundamento.**

Lenguaje funcional en diseño con respuestas verificadas, aritmética decimal exacta y efectos explícitos. Surge del análisis crítico de C, COBOL y Haskell; su originalidad y sus ventajas deberán evaluarse con evidencia.

## Estado

Este repositorio contiene la base documental, la estructura de desarrollo y los primeros fixtures de conformidad. **Todavía no hay lexer, comprobador, intérprete ni compilador ejecutable de Traza.** Los programas de ejemplo describen resultados esperados; no son pruebas del lenguaje ya aprobadas.

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

Requisito del entorno inicial: Python 3.12. No se necesita instalar dependencias externas para comprobar esta base.

```sh
python --version
python -m unittest discover -s pruebas/infraestructura -v
python -m compileall -q fuente pruebas
```

Estas comprobaciones verifican manifiestos e integridad documental; **no ejecutan Traza**. Los fixtures permanecen con estado pendiente. No existe todavía un comando `traza ejecutar` o `traza verificar`.

## Organización

| Ruta | Contenido |
| --- | --- |
| documentacion/ | Especificaciones, decisiones y planificación. |
| fuente/traza/ | Paquete reservado para el prototipo de referencia. |
| pruebas/ | Infraestructura y futuros casos ejecutables del lenguaje. |
| ejemplos/ | Programas de diseño con resultados esperados. |
| herramientas/ | Automatizaciones de desarrollo cuando se incorporen. |
| mediciones/ | Escenarios futuros de tiempo y memoria. |

Primer objetivo: PI01–PI02 y después la demostración D0, con `bounded(50)` exitoso y valores fuera de rango rechazados mediante ContractViolation.

## Contribuciones y licencia

Ver [CONTRIBUIR.md](CONTRIBUIR.md) y [AGENTS.md](AGENTS.md).

El código original del proyecto se distribuye bajo **GNU GPL versión 3 o posterior**, identificador `GPL-3.0-or-later`. Consultar [LICENSE](LICENSE) y la [política de licencias](documentacion/licencias.md). No se concede automáticamente una excepción para un runtime futuro.
