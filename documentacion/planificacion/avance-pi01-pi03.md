# Avance PI01–PI03 · 20 de octubre de 2026

## PI01 · Completado
- CPython 3.12.12 fijado; acciones de CI por SHA.
- Sin dependencias externas para las comprobaciones.
- Comando único de verificación con descubrimiento recursivo, fallo si no encuentra pruebas y registro de entorno.
- Estructura, guía de contribución, licencia y documentación identificadas.

## PI02 · Completado como preparación
- 116 reglas S/T/N/G con origen verificable.
- CF01–CF40 y variantes con reglas, fase, modalidad y expectativa.
- Fuentes de programas para contratos, control y rechazos.
- Vectores numéricos, propiedades con semilla y protocolos para fallos externos.
- Integridad comprobada con referencias recíprocas; Number como texto, sin float.
- Conformidad semántica pendiente: no hay un intérprete que la ejecute.

Evidencia de PI01–PI02: [ejecución CI del primer incremento](https://github.com/estebanspina/traza/actions/runs/39462762166), commit a172ecaa7c667470e01ad3fc6094170bcf967e18.

## PI03 · Iniciado
- Fuente UTF-8 estricta con rangos de bytes [inicio, fin).
- Posiciones desde 1 contando escalares; LF y CRLF.
- G01–G05: reservadas, identificadores, números exactos como texto, cadenas, bytes, comentarios y símbolos.
- Primer diagnóstico SG01, tokens inmutables y JSON de inspección.
- Pruebas de frontera e interfaz; verificar su resultado en la CI del commit que incorpora este informe.

## Pendientes
No hay parser, resolución, tipos, contratos ejecutables ni runtime. El lexer tokeniza incluso programas que deben ser rechazados en fases posteriores. Presupuestos de fuente y proceso se completarán con PI19. La normalización editorial de los PDF sigue separada del cierre de preparación PI01–PI02.
