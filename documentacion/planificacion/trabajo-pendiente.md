# Trabajo pendiente

Fuente: documento 07. Esta tabla es seguimiento inicial, no certificación de paquetes terminados. PI01 está en preparación; PI02 contiene sólo un catálogo parcial para D0. No se crearon issues, hitos o proyectos remotos automáticamente.

| Paquete | Objetivo | Dependencias | Cierre |
| --- | --- | --- | --- |
| PI01 | Base reproducible del repositorio | Ninguna | Entorno, comandos, estructura e integración continua con alcance declarado. |
| PI02 | Catálogo de reglas y fixtures | PI01 | Reglas y casos trazables; manifiestos con fase y resultado esperado. |
| PI03 | Fuente, lexer y rangos | PI01, PI02 | UTF-8, escapes, bytes y posiciones comprobados. |
| PI04 | Parser y precedencias | PI03 | Gramática 04 y rechazos CF37. |
| PI05 | Resolución y aliases | PI04 | Ámbitos, firmas, recursión y ciclos. |
| PI06 | Number exacto mínimo | PI02 | Coeficiente/exponente, cero, suma y comparación sin float. |
| PI07 | Tipos básicos y firmas | PI05, PI06 | Number, Boolean y Result tipados. |
| PI08 | Obligaciones y retorno validado | PI07 | Desconocido produce control antes de Ok compatible. |
| PI09 | Núcleo y ejecutor D0 | PI08 | D0 atraviesa todas las fases sin simular la ejecución. |
| PI10 | Tipos estructurales y funciones | PI07 | Genéricos, sustitución y patrones. |
| PI11 | Motor de refinamientos | PI08, PI10 | Tres estados de prueba y presupuesto. |
| PI12 | Efectos y catálogo simulado | PI10 | Pureza e inclusión de efectos. |
| PI13 | Elaboración completa | PI11, PI12 | Check, retorno y ? explícitos. |
| PI14 | Máquina, cierres y control | PI09, PI13 | Orden, ámbito, recursión y propagación. |
| PI15 | Modelo numérico completo | PI06 | División, redondeo, conversión y prioridades. |
| PI16 | Oráculos y propiedades | PI02, PI15 | CF16–36 con referencia independiente. |
| PI17 | Capacidades y recursos | PI12, PI14 | Autoridad, adaptadores y cierre de recursos. |
| PI18 | CLI y manifiestos ejecutables | PI13, PI14 | Check/run/test con fases e informes. |
| PI19 | Límites y regresión | PI16, PI17, PI18 | Recursos y fallos externos diferenciados. |
| PI20 | Entrega y mediciones | PI19 | Reproducción limpia y límites publicados. |

## Siguiente incremento
- Validar la CI de infraestructura en GitHub y revisar esta base.
- Completar PI01 y PI02, incluido el catálogo de todos los casos y variantes.
- Implementar PI03–05 y PI06.
- Integrar PI07–09 para D0: bounded(50) → Ok(50), bounded(-1) y bounded(101) → Err(ContractViolation); retorno constante inválido → rechazo estático.
- No habilitar comandos de ejecución que todavía no estén implementados.

## Deuda documental
Normalizar las transcripciones cotejando los PDF originales y completar la matriz de reglas. El lexer auxiliar previo no se incluye ni se presenta como frontend completo.
