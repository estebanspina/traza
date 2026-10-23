# Avance · Parser y ejecución D0

Fecha: 20 de octubre de 2026.

## Resultado
Ruta completa fuente → lexer → parser → comprobación del subconjunto → máquina de ejecución. D0 ejecuta sus cuatro expectativas y distingue rechazo estático, Result y error externo.

## Estado del plan
PI01–PI02 conservan su cierre de preparación. PI03 está integrado con el parser inicial PI04. PI05–PI09 tienen únicamente el subconjunto necesario para D0, no un cierre general de todos sus requisitos. PI10–PI20 no se consideran completados.

## Evidencia
[CI del commit b0b235ac1280e69501d4ce6722c8b8b2697754a9](https://github.com/estebanspina/traza/actions/runs/39466594938): **64 pruebas aprobadas y D0 4/4**, incluidas las regresiones de ramas imposibles y conectores constantes.

Entrega: [PR #2](https://github.com/estebanspina/traza/pull/2). El cierre documental conserva la misma implementación comprobada.

## Límites
Ver ejecución-d0.md y ADR 0004. No hay soporte de ejecución de toda la gramática, backend nativo ni evaluación comparativa de rendimiento.

## Continuidad
contexto.md en la raíz resume las decisiones del usuario, la historia, los comandos, la evidencia y los próximos pasos. La evidencia de cierre está registrada allí.
