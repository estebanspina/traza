# Documentación de Traza

## Estado y lectura

El nombre Traza y la decisión de repositorio público con GPL son posteriores a los documentos iniciales. Las especificaciones siguen siendo propuestas 0.1. El contexto y el brief son antecedentes históricos; una decisión pendiente en ellos puede haber sido concretada por una especificación posterior.

Los documentos técnicos siguientes son transcripciones completas del texto extraído de sus PDF, conservadas por página en bloques de texto. No son los PDF ni una conversión editorial completa a Markdown. Se necesita cotejo visual con los originales antes de normalizar tablas y código.

## Índice vigente

| Orden | Documento |
| --- | --- |
| 01 | [Semántica mínima](especificaciones/01-semantica-minima.md) |
| 02 | [Tipos y contratos](especificaciones/02-tipos-contratos.md) |
| 03 | [Modelo numérico](especificaciones/03-modelo-numerico.md) |
| 04 | [Sintaxis y gramática inicial](especificaciones/04-sintaxis-gramatica.md) |
| 05 | [Casos de conformidad](conformidad/05-casos-conformidad.md) |
| 06 | [Arquitectura del prototipo](arquitectura/06-arquitectura-prototipo.md) |
| 07 | [Plan de implementación](planificacion/07-plan-implementacion.md) |
| 08 | [Evaluación y evolución](evaluacion/08-evaluacion-evolucion.md) |

Antecedentes: [contexto 1.1](contexto.md) y [Project Brief 1.0](project-brief.md).

## Evolución del índice
El documento 01 había previsto para 07 un registro de decisiones y para 08 una guía y referencia. Las entregas realizadas fueron un plan de implementación y una estrategia de evaluación. Se conserva el texto histórico y se registra la diferencia en [ADR 0001](decisiones/0001-identidad-y-base-documental.md). El registro de decisiones y una guía inicial se mantienen como documentos complementarios, sin renumerar retrospectivamente los PDF.

## Pendientes editoriales
- Recuperar e incorporar los PDF binarios originales en publicaciones/.
- Normalizar las transcripciones a Markdown cotejado, sin cambiar semántica.
- Corregir enlaces históricos que apuntan a nombres de archivos previos.
- Mantener referencias de regla y casos C, TC, MN, GR y CF.
- Registrar contradicciones y resolverlas explícitamente antes de habilitar capacidades afectadas.

Consultar [trabajo pendiente](planificacion/trabajo-pendiente.md), [guía inicial](guia-inicial.md), [licencias](licencias.md) y [decisiones](decisiones/readme.md).

## Desarrollo implementado

- [Entorno y verificación](desarrollo.md).
- [Catálogo completo](conformidad/catalogo.md).
- [Analizador léxico](analizador-lexico.md).
- [Avance PI01–PI03](planificacion/avance-pi01-pi03.md).

## Parser, ejecución y continuidad

- [Parser y ejecución D0](ejecucion-d0.md).
- [Contexto para retomar](../contexto.md).
- [Avance del parser y D0](planificacion/avance-parser-d0.md).
