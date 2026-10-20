# 07 · Plan de implementación

Estado: propuesta 0.1, anterior al nombre Traza.

Transcripción textual íntegra del PDF `07-plan-implementacion.pdf`. Se conservan los saltos de línea y la disposición de tablas y código en bloques de texto para evitar una conversión Markdown que cambie su significado. Pendiente de normalización editorial y cotejo con el PDF original; no se incorpora aquí el archivo PDF binario.

Para el índice vigente de la serie y sus cambios, consultar [el índice documental](../README.md).

## Página 1

````text
 Plan de implementación
 Documento 07 · Propuesta 0.1
 Lenguaje funcional en diseño · 20 de octubre de 2026

 Resultado buscado
 Construir un prototipo que permita comprobar la semántica del lenguaje mediante un comprobador
 estático, un intérprete de referencia y un arnés reproducible. El plan transforma la arquitectura del
 documento 06 en trabajo ordenado y verificable; no certifica desarrollo ya realizado ni inicia su
 implementación.

 Criterio de planificación
 Priorizar una ruta completa pequeña y ampliar su cobertura sin debilitar las garantías. Un ejemplo
 aceptado debe atravesar análisis, comprobación, elaboración y ejecución. Un programa inválido
 debe detenerse en la fase correcta. Ninguna entrega obtiene crédito por ocultar una característica
 pendiente.

 Base conservada
 Tipos generales y genéricos; respuestas con garantías verificables; evaluación estricta e inmutable;
 Result explícito; Number decimal exacto; efectos declarados. Las decisiones A01 a A22 del
 documento 06 guían la construcción y siguen identificadas como propuestas arquitectónicas.

 Entregables de este plan
 Se definen 20 paquetes de trabajo, PI01 a PI20, cinco incrementos P1 a P5 y una primera
 demostración integrada D0. Cada paquete tiene dependencia y condición de cierre. Las
 estimaciones se expresan por incertidumbre y tamaño relativo, sin inventar fechas, presupuesto ni
 dedicación de un equipo que todavía no se ha definido.

 Referencias y autoridad
 Documentos 01 a 06 de la serie, propuestas 0.1; en especial, los casos CF01 a CF40 del documento
 05 y los incrementos P1 a P5 del 06. Este plan organiza su cumplimiento: no reemplaza las
 especificaciones ni agrega sintaxis nueva.

 Estado
 Plan preparado para revisión. Todos los paquetes se consideran pendientes hasta que exista
 evidencia verificable de su ejecución. Un analizador auxiliar usado para revisar documentación no
 se considera automáticamente el frontend completo del prototipo.




Documento 07 · Propuesta 0.1 · 20 de octubre de 2026                                                     1
````

## Página 2

````text
 1. Orden de construcción

   Entrega                               Objetivo observable                      Dependencia principal

                                                                                  Entorno, fixtures y
   P1                                    Analizar y resolver una unidad fuente.
                                                                                  diagnósticos.

                                         Ejecutar bounded con éxito y violación   Subconjunto integrado de P1 a
   D0
                                         de contrato.                             P3.

                                         Completar tipos, contratos y efectos
   P2                                                                             P1 y aritmética exacta mínima.
                                         previstos.

                                         Completar control y ejecución del
   P3                                                                             Elaboración y tipos de P2.
                                         núcleo.

   P4                                    Completar números e intercambio.         Núcleo numérico y ejecutor.

                                         Consolidar herramientas, límites e
   P5                                                                             Integración de P1 a P4.
                                         informes.



 Una secuencia con integración temprana
 D0 no es un sexto incremento ni equivale a finalizar P2 o P3. Adelanta una parte de sus tareas para
 comprobar que las fronteras encajan. Después se completa la cobertura de tipos y de ejecución.
 Los identificadores P1 a P5 mantienen el significado del documento 06.

 La aritmética exacta mínima comienza antes de D0: constantes, comparación, suma y
 normalización. El redondeo, la división, las conversiones y las propiedades generativas se
 completan en P4. No se simula Number con float mientras se espera ese incremento.

 Prioridad
 Primero, evitar aceptar garantías falsas. Segundo, conservar valores, errores y orden de
 evaluación. Tercero, mejorar diagnósticos y experiencia de uso. Las mediciones de rendimiento
 acompañan al prototipo conforme exista una ruta ejecutable; no condicionan la semántica al
 resultado de un microbenchmark.

 Trabajo simultáneo posible
 Los oráculos numéricos y los fixtures pueden prepararse mientras avanza el frontend, después de
 acordar sus interfaces. Tipos, elaboración y ejecutor deben integrar cambios pequeños y
 frecuentes. Este documento no asigna agentes ni presupone trabajo paralelo disponible.

 Regla de avance
 Una puerta de aceptación se cumple con pruebas y evidencia de fase. Si falla, se corrige o se
 reduce explícitamente el alcance de la entrega; no se marca un caso omitido como aprobado para
 mantener una fecha.




Documento 07 · Propuesta 0.1 · 20 de octubre de 2026                                                            2
````

## Página 3

````text
 2. Preparación y frontend

   Paquete                               Trabajo y dependencia                    Condición de cierre

                                         Base reproducible del repositorio. Sin   Entorno fijado, comandos de
   PI01
                                         dependencia de código.                   prueba y versiones registradas.

                                         Catálogo de requisitos y fixtures.       Cada fixture indica regla, fase
   PI02
                                         Depende de PI01.                         y resultado esperado.

                                                                                  UTF-8, escapes, bytes y
                                         Fuente, lexer y rangos. Depende de
   PI03                                                                           posiciones válidos e inválidos
                                         PI01–02.
                                                                                  probados.

                                         Parser y precedencias. Depende de        Gramática 04, CF37 y árboles
   PI04
                                         PI03.                                    de precedencia comprobados.

                                                                                  Símbolos únicos, recursión,
   PI05                                  Resolución y aliases. Depende de PI04.   ámbitos y ciclos resueltos o
                                                                                  rechazados.



 Puerta P1
 Aceptar los fixtures sintácticamente válidos y rechazar los inválidos en la fase correcta. Resolver
 referencias posteriores y recursión sin ejecutar cuerpos. Probar nombres reservados, duplicados,
 aliases cíclicos y el sombreado propuesto en A05. Ningún símbolo sin resolver puede llegar a una
 fase ejecutable.

 Contratos de interfaz antes del código
 Acordar rangos de fuente, identidad de símbolos y forma del árbol sintáctico. Registrar ejemplos
 mínimos de entrada y salida de cada fase. La recuperación de errores puede producir diagnósticos
 adicionales, pero nunca un programa ejecutable con nodos inválidos.

 Cobertura que no cabe en un único caso
 CF37 cubre rechazos concretos, no toda la gramática. Agregar casos de precedencia, escapes
 Unicode inválidos, literales bytes, comas finales y distinción entre registros de valor y de tipo. Los
 ejemplos del documento 04 son fixtures de referencia, sujetos a revisión de su resultado esperado.

 Riesgo y respuesta
 Reutilizar el analizador auxiliar sólo tras comparar sus reglas con la gramática completa y sus
 diagnósticos. Si una función falta, mantenerla como pendiente explícito; aceptar ejemplos sencillos
 no demuestra conformidad léxica o sintáctica completa.




Documento 07 · Propuesta 0.1 · 20 de octubre de 2026                                                                3
````

## Página 4

````text
 3. Primera demostración integrada D0
 Paquetes iniciales

   Paquete                               Trabajo y dependencia                   Condición de cierre

                                         Number exacto mínimo. Depende de        Coeficiente/exponente, cero,
   PI06
                                         PI02.                                   suma y comparación sin float.

                                                                                 Number, Boolean y Result
                                         Tipos básicos y firmas. Depende de
   PI07                                                                          tipados; errores de tipo
                                         PI05–06.
                                                                                 localizados.

                                                                                 Estado desconocido genera
                                         Obligación y retorno validado.
   PI08                                                                          control antes de Ok
                                         Depende de PI07.
                                                                                 compatible.

                                                                                 Ejecuta el fixture D0 sin
                                         Núcleo y ejecutor inicial. Depende de
   PI09                                                                          saltarse comprobación
                                         PI08.
                                                                                 estática.



 Fixture conductor
 pub fn bounded(x: Number)
   -> Result<Number where {value >= 0 and value <= 100}, Error> {
    Result::Ok(x)
 }

 Entrada 50: Ok(50). Entradas -1 y 101: Err(ContractViolation), con condition_id, location y boundary
 coherentes. El arnés proporciona los argumentos sin sustituir x por una constante del cuerpo. La
 obligación estática sobre un x general debe permanecer desconocida.

 Evidencia de D0
 Conservar fuente, árbol tipado, obligación, control elaborado y resultado estructural para cada
 entrada. Comprobar que x se evalúa una sola vez y que ningún Ok fuera del intervalo cruza la
 frontera. Ejecutar además un retorno conocido 101 para demostrar rechazo D05 antes de
 ejecución.

 Límite de la demostración
 D0 no acredita genéricos completos, recursión, cierres, efectos ni aritmética completa. La interfaz
 identifica ese subconjunto. El ejecutor inicial debe respetar las fronteras de la máquina de
 continuaciones A12; si todavía no soporta una construcción, la rechaza como no implementada.

 Decisión de continuar
 Si D0 requiere alterar silenciosamente una firma, devolver un valor inválido o usar una excepción
 oculta, detener la ampliación y corregir el diseño de la frontera. La demostración existe para
 detectar esa incompatibilidad temprano.




Documento 07 · Propuesta 0.1 · 20 de octubre de 2026                                                             4
````

## Página 5

````text
 4. Tipos, pruebas y ejecución completos

   Paquete                               Trabajo y dependencia                  Condición de cierre

                                                                                Sustitución, inferencia prevista
                                         Tipos estructurales, genéricos y
   PI10                                                                         y patrones con pruebas
                                         funciones. Depende de PI07.
                                                                                positivas y negativas.

                                                                                Demostrado, refutado y
                                         Motor conservador de refinamientos.
   PI11                                                                         desconocido diferenciados;
                                         Depende de PI08 y PI10.
                                                                                presupuesto probado.

                                                                                Pureza, inclusión de efectos y
                                         Efectos y catálogo simulado. Depende
   PI12                                                                         predicados permitidos
                                         de PI10.
                                                                                verificados.

                                         Elaboración completa. Depende de       Check, retorno y ? explícitos,
   PI13
                                         PI11–12.                               con evidencia y firmas intactas.

                                                                                Orden, alcance léxico, ramas,
                                         Máquina, cierres y control. Depende
   PI14                                                                         recursión y propagación
                                         de PI09 y PI13.
                                                                                conformes.



 Puerta P2
 Cumplir los rechazos y aceptaciones CF06–10 y CF38–40. Agregar sustitución de funciones con
 precondiciones distintas y efectos compatibles. Rechazar predicados fuera de la lista permitida.
 Una obligación que consume el presupuesto pasa a desconocida; nunca se convierte en
 demostrada por falta de tiempo.

 Puerta P3
 Cumplir CF01–15 con sus variantes. Observar que Err ordinario no interrumpe argumentos y que ?
 sí abandona la función correspondiente. Probar ramas descartadas y cortocircuito sin depender
 sólo de un tiempo límite. La sonda fatal de CF14 pertenece al arnés y no al catálogo público.

 Garantías que deben persistir
 Un refinamiento validado debe justificar una llamada posterior más débil. Una transformación que
 puede invalidarlo no hereda la garantía. El informe debe mostrar la diferencia entre prueba
 estática y evaluación de un control dinámico.

 Base de confianza
 Revisar las reglas de transferencia de hechos separadamente de los casos de usuario. El modo de
 auditoría revalida garantías para encontrar defectos del comprobador; sus costos y resultados se
 identifican como auditoría. No se presenta como verificación formal del compilador.




Documento 07 · Propuesta 0.1 · 20 de octubre de 2026                                                             5
````

## Página 6

````text
 5. Números, capacidades y herramientas

   Paquete                               Trabajo y dependencia                  Condición de cierre

                                                                                Operaciones, seis modos,
                                         Modelo numérico completo. Depende
   PI15                                                                         conversiones y prioridades de
                                         de PI06.
                                                                                error del 03.

                                         Oráculo y propiedades numéricas.       CF16–36, semillas y
   PI16
                                         Depende de PI02 y PI15.                contraejemplos reproducibles.

                                                                                Adaptadores simulados,
                                         Capacidades y recursos. Depende de
   PI17                                                                         autoridad explícita y recursos
                                         PI12 y PI14.
                                                                                cerrados.

                                         CLI, entradas e informes. Depende de   Check, run y test distinguen
   PI18
                                         PI13–14.                               fase, valor y fallo externo.

                                                                                Presupuestos, sondas y fallos
                                         Límites y regresión integrada.
   PI19                                                                         externos clasificados sin Err
                                         Depende de PI16–18.
                                                                                inventados.

                                         Paquete de entrega y mediciones.       Versión reproducible, cobertura
   PI20
                                         Depende de PI19.                       y limitaciones publicadas.



 Puerta P4
 Validar toda la batería numérica y ampliar prioridades ante argumentos múltiples inválidos. El
 oráculo racional no reutiliza el algoritmo bajo prueba. Probar signos, empates, exponentes y
 coeficientes grandes. Formatear no redondea y la serialización preserva el valor.

 Puerta P5
 La CLI ejecuta únicamente núcleo comprobado. La entrada externa refinada se valida antes de
 llamar y se distingue del Result que retorna la función. Los informes separan aprobado, fallido,
 bloqueado, omitido e inconcluso. Repetir las pruebas exigidas en una instalación limpia y conservar
 la evidencia.

 Entrada y salida
 Implementar primero adaptadores simulados del catálogo A17. Los adaptadores reales son un
 alcance separado dentro de PI17 y requieren sus propias pruebas de rutas y cierre de recursos. No
 impiden finalizar la conformidad del núcleo si quedan declarados como no disponibles en esa
 entrega.

 Rendimiento
 PI20 mide con trazas desactivadas y documenta plataforma, datos, tamaños y variación. Una
 medición del intérprete no determina la velocidad de un backend futuro. Los resultados podrán
 justificar una propuesta de especialización, nunca su incorporación automática.




Documento 07 · Propuesta 0.1 · 20 de octubre de 2026                                                             6
````

## Página 7

````text
 6. Trazabilidad y cobertura

   Requisito o decisión                  Paquetes responsables           Evidencia mínima

   Gramática y posiciones, A04–05        PI03–05                         Fixtures y rangos; CF37.

                                                                         Aceptaciones y rechazos;
   Tipos y funciones, A06                PI07, PI10
                                                                         CF38–39.

   Obligaciones y evidencia,                                             CF01–10 e informe de
                                         PI08, PI11, PI13
   A07–11                                                                controles.

   Ejecución y memoria, A12–14           PI09, PI14, PI19                CF11–15, límites y cierres.

   Exactitud y oráculo, A15–16           PI06, PI15–16                   CF16–36 y propiedades.

   Efectos y autoridad, A17–18           PI12, PI17                      CF40, catálogo y adaptadores.

   Herramientas y medición,                                              Informes, reproducción y
                                         PI18–20
   A19–22                                                                perfiles.



 Registro vivo
 Cada requisito necesita un identificador de prueba, estado, revisión ejecutada y enlace a evidencia.
 Una prueba puede cubrir varias reglas si el informe identifica qué afirma. La cobertura documental
 no equivale a ejecución. Los casos antiguos C, TC, MN y GR siguen siendo fuentes de requisitos y
 no desaparecen por tener un equivalente CF.

 Definición de terminado de un paquete
 El comportamiento está implementado, revisado y probado en su fase; sus regresiones pasan; los
 diagnósticos y límites están documentados; no hay contradicción abierta que afecte su garantía. La
 evidencia incluye el entorno y la revisión del código. Un paquete parcialmente cumplido se divide o
 permanece abierto.

 Cambios de contrato entre componentes
 Versionar el esquema interno si cambia una interfaz consumida por otra fase. Actualizar fixtures,
 elaborador y ejecutor en la misma entrega o mediante una transición explícita. No serializar un
 árbol interno como formato público estable por conveniencia.

 Criterio de publicación
 Una versión experimental publica exactamente su subconjunto soportado. Sólo puede afirmar que
 supera la batería de esta serie cuando todos sus casos y variantes exigidos estén aprobados, sin
 bloqueados u omisiones. Esa afirmación sigue siendo más limitada que una prueba de conformidad
 completa del lenguaje.




Documento 07 · Propuesta 0.1 · 20 de octubre de 2026                                                     7
````

## Página 8

````text
 7. Organización, incertidumbre y decisiones
 Responsabilidades funcionales
 El responsable del lenguaje resuelve ambigüedades; desarrollo conserva las invariantes de fase;
 revisión comprueba garantías y cambios de contrato; pruebas mantiene oráculos independientes.
 Una persona puede cubrir varios roles, pero la evidencia debe permitir revisión externa. Este plan
 no asigna personas ni presume una dotación.

 Tamaño relativo y riesgo
 PI01–05 concentran incertidumbre en gramática y resolución; PI06–09 en la integración de la
 frontera; PI10–14 en pruebas estáticas y control; PI15–16 en exactitud y costos extremos; PI17–20
 en recursos y reproducibilidad. No se suman estos grupos como si fueran duraciones conocidas.

 Después de D0, estimar el resto usando tiempo real, defectos encontrados y alcance pendiente.
 Registrar supuestos de dedicación y experiencia. Volver a estimar cuando cambie una regla, una
 dependencia o una capacidad del equipo; no usar esta propuesta como compromiso de calendario.

 Decisiones abiertas con responsable lógico

                                                                         Tratamiento mientras está
   Tema                                  Resolver antes de
                                                                         abierto

                                                                         Mantenerlo fuera del
   Longitud de Text                      Habilitar ese predicado
                                                                         subconjunto permitido.

                                                                         Acordar muestras y validar
   Esquema de manifiestos                Integrar PI18
                                                                         versión.

                                                                         Mantener propuesta A17
   Errores de entrada/salida             Publicar adaptadores reales
                                                                         explícita y simulada.

                                                                         No afirmar conformidad de esa
   Decodificación de esquemas            Ofrecer formatos externos
                                                                         frontera.



 Abogado del diablo
 Un prototipo que sólo acepta ejemplos felices puede ocultar un comprobador incorrecto: exigir
 rechazos y auditoría. Un oráculo que comparte el mismo error puede dar una falsa aprobación:
 mantener referencia independiente. Un porcentaje de cobertura puede ocultar casos omitidos:
 publicar su lista. Un benchmark favorable puede depender de trazas o entradas pequeñas: declarar
 condiciones y dispersión.

 Control de cambios
 Registrar problema, alternativas, decisión, impacto en reglas y pruebas y condición para
 reconsiderar. Si cambia la semántica, actualizar primero la especificación y sus expectativas. Los
 arreglos locales del intérprete no autorizan excepciones al lenguaje.




Documento 07 · Propuesta 0.1 · 20 de octubre de 2026                                                  8
````

## Página 9

````text
 8. Inicio y revisión de la entrega
 Primer trabajo ejecutable
 Comenzar por PI01 y PI02: repositorio reproducible, catálogo de reglas y fixtures de D0. Acordar
 rangos, símbolos y resultados de fase. Continuar con PI03–05 y PI06; integrar el subconjunto
 PI07–09 y demostrar bounded. Después completar P2 y P3, y cerrar P4 y P5 con sus puertas de
 aceptación.

 Lista de revisión de D0
 El programa aceptado conserva su firma; Number es exacto; la obligación sobre el parámetro
 general es desconocida; el retorno tiene un control; Ok(50) y Err para -1 y 101 son
 estructuralmente correctos; el retorno constante inválido es rechazado; el informe permite
 localizar la frontera. Estas comprobaciones no se sustituyen por una captura de pantalla de la
 consola.

 Evidencia que acompaña a cada entrega
 Fuente y revisión del prototipo, versión de especificaciones, entorno reproducible, casos
 ejecutados con variantes, resultados por fase, defectos pendientes y pasos para repetir. Para
 rendimiento, agregar configuración de trazas, tamaño de entrada, unidades y dispersión. Para
 límites, registrar presupuesto y clasificación del evento externo.

 Qué se aprueba aquí
 El orden y la descomposición del trabajo, las dependencias, la integración temprana D0 y las
 condiciones de aceptación. Las decisiones arquitectónicas permanecen trazables al documento 06.
 Las cuestiones aún abiertas mantienen su tratamiento provisional visible.

 Estado real de esta edición
 Se revisó la coherencia de los 20 paquetes, sus dependencias y su relación con P1–P5; se generó y
 revisó el PDF. No se implementó el prototipo, no se ejecutaron pruebas CF sobre él ni se estimó una
 fecha de finalización. Toda referencia a aceptación describe una condición futura.

 Punto de control
 Esta entrega se detiene para aprobación o corrección, siguiendo el criterio de la serie. El siguiente
 documento deberá cerrar el conjunto documental con la estrategia de evaluación y evolución del
 lenguaje: cómo juzgar sus resultados, aceptar cambios y decidir cuándo ampliar el alcance. Su
 contenido se preparará tras la revisión de este plan.




Documento 07 · Propuesta 0.1 · 20 de octubre de 2026                                                     9
````

