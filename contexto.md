# Contexto de continuidad · Traza

Fecha de actualización: 23 de octubre de 2026.
Repositorio público: https://github.com/estebanspina/traza
Idioma de trabajo y documentación: castellano.
Licencia: GNU GPL versión 3 o posterior, GPL-3.0-or-later.

Este documento resume decisiones y estado para retomar el trabajo sin depender del historial del chat. Leer también agents.md, readme.md y las especificaciones pertinentes antes de modificar código. El repositorio y sus pruebas son la fuente de estado actual; este contexto no reemplaza las reglas semánticas.

## Intención del usuario
Crear un lenguaje funcional nuevo, originalmente comparando C, COBOL y Haskell con enfoque crítico y de abogado del diablo. Conservar eficiencia y control de representación, claridad de reglas y composición funcional sin trasladar todos los mecanismos de esos lenguajes.

El usuario pidió tipos generales y genéricos, evitando tipos específicos de negocio salvo justificación por ciclos de reloj o memoria. Las respuestas de funciones deben tener garantías comprobadas para evitar validaciones manuales repetidas cuando sigan siendo válidas. No prometer originalidad demostrada ni costo cero.

El nombre elegido es **Traza**. Identidad propuesta: «Cada resultado, con fundamento». El usuario prefiere nombres de archivos en minúsculas y la licencia en license.md, con su contenido intacto. El directorio técnico .github/ISSUE_TEMPLATE conserva el nombre requerido por GitHub.

Todo avance de desarrollo debe enviarse a GitHub. Trabajar mediante ramas, pruebas en GitHub Actions y solicitudes de cambios; integrar resultados comprobados. El usuario pidió guardar contexto al finalizar esta etapa.

## Decisiones de lenguaje
- Evaluación estricta de izquierda a derecha, valores inmutables y ámbito léxico.
- Funciones y estructuras generales; aliases transparentes y parámetros genéricos en la especificación.
- Result representa éxito o error; Option representa ausencia.
- Err ordinario no interrumpe argumentos; ? propaga explícitamente desde la función contenedora compatible.
- Contratos where sobre value: demostrados omiten control; refutados en una ruta alcanzable producen rechazo; desconocidos se validan antes de entregar éxito si hay Result compatible.
- Una precondición desconocida debe establecerse con check explícito antes de llamar; no se fabrican firmas ni excepciones ocultas.
- Las transformaciones pueden perder garantías. Las propiedades de estado externo no conservan vigencia indefinidamente.
- Number es un decimal finito exacto, lógicamente coeficiente entero por potencia de diez. No hay NaN, infinito ni cero negativo observable.
- Suma, resta y producto exactos; división exacta o redondeada explícitamente según la especificación. Seis modos, sin modo predeterminado.
- La escala de presentación no forma parte del valor. Formatear no redondea implícitamente.
- Efectos declarados y capacidades explícitas; fallos del proceso separados de errores Result.

## Base documental
documentacion/readme.md contiene el índice vigente de las ocho entregas: semántica, tipos/contratos, números, gramática, conformidad, arquitectura, implementación y evaluación/evolución.

Los documentos se importaron como transcripciones textuales de PDF, preservadas por página. Los binarios originales y la normalización editorial cotejada siguen pendientes. No reinterpretar tablas o código por inferencia. Contexto 1.1 y brief 1.0 se conservan como antecedentes históricos.

El índice previsto originalmente para 07 y 08 cambió durante las entregas; ADR 0001 documenta esa diferencia. El registro de decisiones y la guía son complementos del índice real.

## Base completada antes de esta etapa
PI01: CPython 3.12.12 fijado, acciones por SHA, sin dependencias externas, comando único de verificación.
PI02: 116 reglas S/T/N/G y 40 casos CF con 56 variantes, modalidades y trazabilidad. Preparación de catálogo no equivale a conformidad ejecutada.
Lexer: UTF-8 estricto, LF/CRLF, identificadores ASCII, reservadas, literales, escapes, bytes, comentarios, máxima longitud, tokens y rangos inmutables.
PR #1 integrada: https://github.com/estebanspina/traza/pull/1
Estado anterior: commit 7138221d5f3189e40c4d3ec4ed42565339408204, con 32 pruebas aprobadas.

## Implementado en esta etapa
- Parser de la EBNF G23 con AST inmutable, rangos y precedencias.
- Comprobador conservador de un subconjunto, con firmas superiores, duplicados, tipos, precondiciones y obligaciones de retorno.
- Number mínimo exacto: literales, +, -, *, igualdad y orden.
- Máquina de continuaciones y marcos explícitos para evitar depender de la pila Python en llamadas recursivas.
- Funciones puras, recursión, let, if, cortocircuito, primitivas, Result, check numérico y ?.
- Comandos tokens, analizar, verificar y ejecutar.
- Arnés D0 real: cuatro expectativas, incluidas las dos entradas fuera de rango y D05.
- Pruebas de fases, CLI, garantías, argumentos externos y recursos.

El artefacto Comprobado conserva AST, firmas y obligaciones. Aún no es la elaboración completa del núcleo propuesta en A09. No marcar P2, P3, PI05 o PI10–PI14 como completos por tener esta ruta vertical.

## Alcance de ejecución y límites
El parser reconoce muchas construcciones aún no ejecutables. NI01 informa capacidad no implementada.
No se ejecutan aliases, genéricos, registros, listas, match, lambdas, efectos, división, redondeo ni esquemas externos.
Los refinamientos ejecutables usan value y constantes con comparaciones numéricas y conectores. Las relaciones con otros parámetros y los predicados incorporados length/is_integer/is_quantized siguen pendientes.
La CLI admite Number como texto decimal, Boolean y Text; Bytes se utiliza como literal.
Presupuestos iniciales externos: 1000 dígitos por literal, exponente absoluto hasta 1000, coeficiente hasta 8192 bits y 100000 pasos por defecto. Agotarlos no crea un Err numérico.
No hay compilador nativo, garantía de terminación ni aislamiento para programas hostiles.

## Comandos para retomar

```sh
git clone https://github.com/estebanspina/traza.git
cd traza
python --version
python herramientas/verificar.py
python herramientas/probar_d0.py
python herramientas/traza.py analizar ejemplos/contratos/bounded.traza
python herramientas/traza.py verificar ejemplos/contratos/bounded.traza
python herramientas/traza.py ejecutar ejemplos/contratos/bounded.traza --entrada bounded --argumentos '["50"]' --traza
python herramientas/traza.py ejecutar ejemplos/contratos/bounded.traza --entrada bounded --argumentos '["101"]' --traza
```

Salida 0 significa comando correcto, incluso si el programa produce Err esperado. Salida 1: error de programa o NI01; 2: uso, lectura o entrada; 3: recursos externos. No interpretar tokens o AST como aceptación de tipos.

## Evidencia disponible
La ejecución https://github.com/estebanspina/traza/actions/runs/39466594938 del commit b0b235ac1280e69501d4ce6722c8b8b2697754a9 aprobó **64 pruebas y las cuatro expectativas D0 (4/4)**. La primera ejecución falló por clasificar una llamada arbitraria en contrato como NI01 en lugar de D03; se corrigió sin rebajar la expectativa.

Entrega de esta etapa: https://github.com/estebanspina/traza/pull/2, rama tarea/parser-ejecucion-d0. La evidencia citada incluye regresiones de ramas imposibles y conectores constantes. Las actualizaciones posteriores de cierre documental no cambian ese código. Consultar el estado de la PR y la última CI para conocer el commit de integración en main; no confundir este hash de código probado con el merge.

Las expectativas del catálogo permanecen separadas de los informes. El arnés D0 no certifica los 40 casos CF. Las pruebas adicionales de composición y control tampoco acreditan soporte de match, efectos o división.

## Próximo trabajo recomendado
1. Revisar el estado de main y la última CI; conservar D0 como regresión.
2. Completar resolución PI05, incluidos aliases, constructores y ámbitos.
3. Ampliar tipos y núcleo elaborado, empezando por variantes y match exhaustivo para tratar Result explícitamente.
4. Ampliar predicados e implicaciones con evidencia; sustituir parámetros al comparar contratos antes de habilitar relaciones.
5. Completar números PI15–PI16: división, redondeo y oráculos independientes.
6. Ampliar el arnés CF con informes de fase y cobertura real, sin modificar expectativas para esconder fallos.
7. Mantener efectos simulados antes de habilitar adaptadores reales.
8. Normalizar documentación cotejando PDF originales; revisar originalidad con fuentes antes de afirmarla.

No iniciar optimizaciones nativas ni especializaciones visibles sin evidencia de tiempo/ciclos o memoria y preservación de semántica.

## Condiciones operativas del trabajo anterior
El entorno local de ejecución no estaba disponible. Los archivos se publicaron mediante el conector GitHub y se probaron en GitHub Actions. No suponer que se ejecutaron localmente ni que existe un checkout persistente. No guardar ni solicitar credenciales en archivos del repositorio.
