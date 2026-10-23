# Instrucciones para agentes y colaboradores

## Alcance
Estas instrucciones cubren todo el repositorio. Usar castellano para documentación, mensajes de diagnóstico y nombres internos del proyecto, conservando nombres exigidos por herramientas y palabras de la gramática. No traducir la sintaxis de Traza sin una propuesta semántica.

## Nombres de archivos
Usar nombres de archivos en minúsculas. La licencia se conserva en license.md sin modificar su texto; la documentación usa extensión .md. Mantener los nombres de directorios técnicos exigidos por herramientas, como .github/ISSUE_TEMPLATE. Actualizar enlaces, metadatos y referencias al renombrar.

## Antes de cambiar código
Leer el README, el índice documental y las reglas pertinentes. Mantener la diferencia entre decisión del usuario, propuesta semántica, arquitectura y comportamiento implementado. Las transcripciones históricas no se reescriben silenciosamente.

## Invariantes
- No usar float ni redondeo implícito para implementar Number.
- No fabricar firmas Result ni excepciones ocultas.
- No entregar un éxito que incumpla su contrato.
- No transferir automáticamente garantías a transformaciones que puedan romperlas.
- No confundir Err ordinario, propagación por ? y fallo del proceso.
- No ejecutar programas del usuario durante la comprobación de predicados.
- No declarar conformidad, originalidad o rendimiento sin evidencia.
- Mantener efectos y capacidades explícitos.

## Trabajo
Implementar incrementos pequeños según PI01–PI20. Crear componentes cuando exista código que los justifique; no llenar carpetas vacías. No introducir funcionalidades ajenas al paquete abordado. Registrar ambigüedades en decisiones y actualizar reglas y pruebas si cambia semántica.

## Verificación
Ejecutar las comprobaciones del README y las pruebas de la fase afectada. Informar qué se ejecutó y qué quedó pendiente. CI de infraestructura no equivale a conformidad de Traza. Conservar versiones, entradas y semillas cuando existan.

## Licencia
Usar SPDX-License-Identifier: GPL-3.0-or-later en código original nuevo. Preservar avisos de terceros. No añadir excepciones de runtime ni dependencias con licencia incompatible por inferencia.
