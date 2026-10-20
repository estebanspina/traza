# ADR 0002 · Entorno y catálogo inicial

Fecha: 20 de octubre de 2026.
Estado: decisión de implementación para PI01–PI02.

## Entorno
Fijar CPython 3.12.12 y acciones por SHA; usar biblioteca estándar sin instalación de dependencias. Un único comando descubre todas las pruebas desde la raíz real del repositorio y registra el entorno. No prometer reproducción binaria idéntica del runner.

## Catálogo
Mantener reglas y casos en JSON con versión de esquema 0.1. Los valores Number son texto, nunca float. Cada caso tiene reglas, fase, modalidad, variantes y expectativas. Todos permanecen pendientes mientras no exista su ejecutor.

Los protocolos de fallo fatal y conversiones externas no se reemplazan con intrínsecos inventados. Las propiedades fijan semilla y cantidad inicial, sin ejecutar un generador todavía inexistente.

## Consecuencias
PI01 y PI02 podrán cerrarse cuando la CI compruebe su integridad. Esto no cierra PI03 ni acredita los 40 casos semánticos. La normalización editorial de los PDF es deuda separada.
