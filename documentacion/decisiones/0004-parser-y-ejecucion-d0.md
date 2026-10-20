# ADR 0004 · Parser y ejecución comprobada D0

Fecha: 20 de octubre de 2026.
Estado: implementación experimental para la ruta D0; no completa P2 ni P3.

## Decisión
Implementar la EBNF G23 mediante descenso recursivo sobre los tokens existentes. El AST es inmutable y conserva rangos. El parser acepta construcciones que el ejecutor todavía no soporta: aceptación sintáctica y ejecución son fases distintas.

Para D0, comprobar primero todas las funciones del programa, resolver sus firmas y validar tipos y predicados del subconjunto. Ejecutar sólo el artefacto Comprobado. Éste conserva AST, firmas y obligaciones; todavía no es el núcleo elaborado completo de A09. PI13 y el comprobador completo siguen pendientes.

## Subconjunto
Primitivas Number, Boolean, Text, Bytes, Error y Result de una primitiva con Error; funciones puras con firma, recursión, let, if, operaciones + - *, comparaciones, and/or/not, constructores Result, check numérico y ?.

Los refinamientos ejecutables son comparaciones numéricas y conectores sobre value y constantes. Las relaciones con otros parámetros quedan NI01: conservar nombres del contrato del callee sin sustituir parámetros podría introducir pruebas falsas.

Aliases, genéricos, listas, registros, match, cierres, efectos y división se analizan pero aún no se ejecutan. NI01 identifica capacidad pendiente y no significa que el programa sea inválido en el lenguaje completo.

## Garantías
Demostrado omite el control de retorno; refutado produce D05; desconocido sólo se admite en Result compatible y se comprueba antes de Ok. Una precondición no demostrada produce D04. Un retorno desconocido directo produce D06. Los retornos de ramas se revisan separadamente cuando corresponde.

Los argumentos externos se validan antes de llamar; un fallo de entrada no fabrica un Result de la función. No se admiten números JSON para Number: se requiere texto decimal.

## Ejecución y recursos
La máquina mantiene continuaciones y marcos explícitos. ? utiliza un estado interno de propagación y termina sólo la función contenedora; Err ordinario continúa siendo un valor.

Number usa coeficiente/exponente enteros sin float. Presupuestos iniciales: 1000 dígitos por literal, exponente absoluto hasta 1000 y coeficiente hasta 8192 bits; 100000 transiciones por ejecución por defecto. Son límites externos de la herramienta, no límites semánticos de Number ni nuevos errores de Result. Presupuestos de memoria y fuente aún pendientes.

El control de retorno se ejecuta sobre el candidato ya evaluado. Los metadatos incluyen condición, ubicación y frontera. Las trazas se usan para pruebas, no para prometer costos de producción.

## Límites
No se implementan el catálogo numérico completo ni un backend nativo. No se asegura terminación ni aislamiento de código hostil. La batería completa CF y la normalización editorial de los PDF siguen pendientes.
