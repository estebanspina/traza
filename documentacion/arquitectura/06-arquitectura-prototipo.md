# 06 · Arquitectura del prototipo

Estado: propuesta 0.1, anterior al nombre Traza.

Transcripción textual íntegra del PDF `06-arquitectura-prototipo.pdf`. Se conservan los saltos de línea y la disposición de tablas y código en bloques de texto para evitar una conversión Markdown que cambie su significado. Pendiente de normalización editorial y cotejo con el PDF original; no se incorpora aquí el archivo PDF binario.

Para el índice vigente de la serie y sus cambios, consultar [el índice documental](../README.md).

## Página 1

````text
 Arquitectura del prototipo
 Documento 06 · Propuesta 0.1
 Lenguaje funcional en diseño · 20 de octubre de 2026

 Objetivo
 Definir una arquitectura implementable para comprobar las decisiones del lenguaje antes de
 invertir en generación de código nativo. El producto inicial será un comprobador estático y un
 intérprete de referencia con pruebas reproducibles. Esta entrega es un diseño; no presenta
 componentes ya implementados.

 Principios conservados
 Tipos generales y genéricos; evaluación estricta de izquierda a derecha; valores inmutables;
 errores como valores Result; contratos comprobados antes de entregar éxito; Number decimal
 exacto; efectos declarados. Las representaciones especializadas requieren evidencia de memoria o
 tiempo, sin alterar la semántica.

 Decisión principal A01
 Implementar el prototipo de referencia en Python, con estructuras internas explícitas para tipos,
 números y control. Es una elección para facilitar la revisión del diseño y sus pruebas, no una
 promesa de rendimiento ni el lenguaje obligatorio de una futura implementación industrial.

 Alcance A02
 Analizar un programa completo en una unidad fuente; resolver nombres; comprobar tipos,
 refinamientos y efectos; producir una representación intermedia tipada; ejecutarla con
 capacidades controladas. No se introduce sintaxis de importación en esta etapa.

 Fuera del primer incremento
 Generación nativa, compilación separada, interfaz binaria con C o COBOL, ejecución paralela,
 optimizaciones agresivas y verificación de terminación. Estas exclusiones no eliminan las reglas del
 lenguaje: una característica sin implementar se informa como tal y no se acepta silenciosamente.

 Base documental
 Documentos 01 a 05 de esta serie, propuestas 0.1. En especial: tipos y contratos del 02, modelo
 numérico del 03, gramática del 04 y los 40 casos CF del 05. Ante contradicciones, registrar una
 decisión y corregir la especificación afectada; la implementación no redefine el lenguaje por
 accidente.




Documento 06 · Propuesta 0.1 · 20 de octubre de 2026                                                    1
````

## Página 2

````text
 1. Componentes y fronteras

   Componente                            Responsabilidad                           Producto verificable

   Fuente y analizador                   UTF-8, tokens, precedencia, posiciones    Árbol sintáctico con rangos.

                                         Ámbitos, símbolos, aliases,
   Resolución                                                                      Referencias inequívocas.
                                         constructores

   Comprobador                           Tipos, efectos, patrones y obligaciones   Árbol tipado y evidencia.

                                         Hacer explícitos controles y
   Elaboración                                                                     Núcleo tipado ejecutable.
                                         propagación

   Ejecutor                              Orden, valores, cierres y llamadas        Valor o fallo externo.

   Arnés                                 Entradas, oráculos, trazas y límites      Informe reproducible.



 Dependencias A03
 El analizador desconoce operaciones del sistema. El comprobador consulta firmas y hechos
 numéricos, nunca ejecuta funciones arbitrarias del usuario para demostrar contratos. El ejecutor
 consume únicamente el núcleo tipado validado; el arnés no puede saltarse esa frontera en una
 ejecución normal.

 Los adaptadores de capacidades dependen del ejecutor mediante un registro explícito. El núcleo
 numérico es puro respecto del entorno y se prueba por separado. Los informes reciben eventos ya
 estructurados; no reinterpretan mensajes de consola como pruebas.

 Contrato de las fases
 Cada fase produce un resultado correcto o una lista de diagnósticos. Se puede recuperar de errores
 sintácticos para mostrar más de uno, pero no construir un programa ejecutable con nodos
 inválidos. Una falla interna del compilador se clasifica separadamente de un rechazo del programa.

 Invariantes
 Ninguna referencia queda sin resolver al terminar resolución. Ninguna llamada sin firma llega al
 núcleo. Ningún retorno exitoso con obligación pendiente sale al usuario. Ningún adaptador anfitrión
 obtiene autoridad a partir de una cadena de texto del programa.

 Compromiso
 Separar fases agrega estructuras y trabajo inicial. Permite localizar si un error pertenece a sintaxis,
 prueba, elaboración o ejecución, y conservar un intérprete de referencia al incorporar otro
 backend.




Documento 06 · Propuesta 0.1 · 20 de octubre de 2026                                                              2
````

## Página 3

````text
 2. Fuente, nombres y tipos
 Fuente A04
 Conservar bytes originales y una tabla de líneas. Usar rangos internos de bytes con inicio incluido y
 fin excluido; presentar línea y columna contando valores escalares Unicode desde 1. El
 identificador de fuente es relativo al proyecto. Una herramienta puede presentar otra unidad de
 columna si la declara en su adaptador.

 El lexer valida UTF-8, escapes y literales conforme al documento 04. Los identificadores mantienen
 las restricciones ASCII de aquella gramática. No normalizar textos ni interpretar separadores
 numéricos regionales.

 Resolución A05
 Recolectar las firmas superiores antes de comprobar cuerpos, permitiendo recursión y referencias
 posteriores. Rechazar nombres superiores duplicados, redefiniciones reservadas y ciclos de aliases.
 Cada variable recibe un símbolo único; un entorno léxico persistente representa las capturas de un
 cierre.

 Dentro de un mismo ámbito se rechazan enlaces duplicados; un ámbito anidado puede sombrear
 un enlace exterior, salvo nombres reservados. Este detalle se propone para cerrar el
 comportamiento del prototipo y requiere casos adicionales a los CF existentes.

 Tipos A06
 Representar Number, Boolean, Text, Bytes, listas, registros cerrados, variantes, funciones,
 parámetros genéricos y refinamientos como nodos distintos. Los aliases son transparentes. Los
 tipos internos no incorporan Money, Rate ni otros tipos de negocio.

 Comprobar polimorfismo de primer nivel conforme al documento 02. El intérprete puede compartir
 una representación para instancias genéricas; antes de borrar información de tipos debe haber
 resuelto todas las obligaciones. No usar el tipo dinámico del anfitrión como sustituto del tipo del
 lenguaje.

 Patrones y funciones
 Comprobar cobertura y solapamientos antes de ejecutar match. Para funciones, verificar
 parámetros, resultado y conjunto de efectos según las reglas de sustitución del documento 02.
 Aceptar una función no implica demostrar su terminación.

 Evidencia de fase
 Guardar por nodo su tipo, efecto y rango de fuente; por llamada, la firma resuelta; por obligación,
 hipótesis y conclusión. Estos datos permiten explicar los controles eliminados sin depender del
 código máquina futuro.




Documento 06 · Propuesta 0.1 · 20 de octubre de 2026                                                     3
````

## Página 4

````text
 3. Motor de contratos
 Obligaciones A07
 Una obligación contiene identificador, frontera, expresión objetivo, predicado normalizado e
 hipótesis disponibles. El comprobador devuelve Demostrado, Refutado o Desconocido. No
 confundir «no logré demostrar» con «demostré falso».

 El subconjunto inicial admite conjunciones, comparaciones exactas, intervalos, hechos sobre
 campos y predicados permitidos del documento 02. is_integer e is_quantized requieren sus
 dominios válidos. length se admite para Bytes y List; la unidad de longitud de Text continúa
 pendiente y no se supone equivalente a bytes.

 Procedimiento conservador
 Normalizar constantes con el núcleo exacto. Incorporar refinamientos de entrada, hechos de la
 rama y propiedades de un check exitoso. Calcular intervalos y hechos simples con reglas finitas y
 explícitas. Sólo declarar Refutado cuando las hipótesis impliquen la negación de la condición en
 esa ruta alcanzable; la existencia de un contraejemplo aislado no basta.

 Establecer un presupuesto de trabajo por obligación. Agotarlo produce Desconocido, no un fallo de
 prueba favorable. No usar llamadas arbitrarias ni búsquedas sin límite para decidir un predicado.

   Frontera                              Demostrado                     Refutado o desconocido

   Argumento refinado                    Llamada permitida.             Rechazo; exigir check explícito.

                                                                        Refutado: D05; desconocido:
   Retorno de éxito                      Conservar garantía.            control si Result compatible, o
                                                                        D06.

                                                                        Evalúa y produce Ok refinado o
   check explícito                       Puede simplificarse.
                                                                        Err.



 Evidencia A08
 El informe registra regla aplicada, dependencias y estado. Cada regla de transferencia tiene
 pruebas propias. Una ruta imposible sólo se descarta si hay evidencia; no basta que el motor no
 encuentre entradas.

 Límite de confianza
 El motor y sus reglas forman parte de la base de confianza. El prototipo no certifica
 matemáticamente su propia corrección. Un modo de auditoría puede revalidar garantías en
 ejecución para detectar fallos del comprobador; ese modo debe identificarse y no representa el
 costo normal del programa.




Documento 06 · Propuesta 0.1 · 20 de octubre de 2026                                                      4
````

## Página 5

````text
 4. Núcleo y controles explícitos
 Representación A09
 El núcleo conserva expresiones tipadas para constantes, variables, let, llamadas, cierres, registros,
 variantes, ramas y match. Agrega operaciones internas para comprobación de contrato,
 propagación de Result y frontera de retorno. No son palabras nuevas del lenguaje fuente.

 Elaboración de un retorno desconocido
 Fuente: Result::Ok(x), respuesta Result<Number where P, Error>
 1. Evaluar x una vez y conservar su valor.
 2. Comprobar P sobre ese valor antes del éxito de la función.
 3. Si P es verdadero, entregar Ok con la garantía P.
 4. Si P es falso, entregar Err(ContractViolation).

 Un Err ya existente pasa sin comprobar P. Un Result intermedio no validado no se marca como
 refinado: la garantía sólo aparece después del control. Si el resultado llega desde una rama o
 llamada, la frontera de retorno discrimina su variante antes de validar.

 Propagación A10
 El nodo interno para ? recibe exactamente un Result. Ok continúa con el contenido; Err abandona
 la función más cercana, preservando el error compatible. No se implementa como una excepción
 pública. El ejecutor mantiene un estado de control distinto del valor Result ordinario.

 Identidad del control A11
 condition_id será el identificador de obligación dentro de la revisión del programa; location será
 una referencia textual al rango de fuente; boundary indicará la función y la clase de frontera, por
 ejemplo return o check. Los tres son Text, conforme al tipo de ContractViolation ya definido.

 La estabilidad se garantiza dentro de la misma revisión y versión del comprobador. Cambiar el
 fuente puede cambiar los identificadores. No prometer compatibilidad permanente de rutas o
 números de línea.

 Caso conductor
 En bounded(x), el comprobador no conoce el intervalo de un x general: inserta control antes de Ok.
 En pipeline, ? conserva el refinamiento de ese éxito. La llamada a double usa la implicación hacia
 no negatividad, sin exigir otra validación manual. Debe poder inspeccionarse esta secuencia en el
 informe de elaboración.




Documento 06 · Propuesta 0.1 · 20 de octubre de 2026                                                     5
````

## Página 6

````text
 5. Ejecutor, valores y memoria
 Ejecución A12
 Usar una máquina con pila explícita de continuaciones y marcos de llamada. Así la recursión del
 programa no depende directamente de la profundidad de la pila del anfitrión. Seleccionar una rama
 antes de evaluarla; evaluar argumentos de izquierda a derecha; implementar el cortocircuito de
 and y or como control.

 Una variante Err ordinaria sigue siendo un valor. El fallo fatal del proceso, la salida por ? y el
 retorno normal son estados distintos del ejecutor. Las excepciones internas del anfitrión no se
 convierten indiscriminadamente en Error del lenguaje.

 Valores A13
 Number conserva coeficiente y exponente enteros exactos. Boolean tiene etiqueta propia; no
 hereda conversiones numéricas del anfitrión. Text conserva secuencias de valores escalares sin
 normalización implícita; Bytes conserva octetos. List y los campos de registros son inmutables
 desde el programa. Las variantes usan etiqueta y contenido; los cierres capturan valores y
 símbolos léxicos.

 Compartir estructuras internas es admisible si no cambia identidad o mutabilidad observable. Los
 refinamientos se representan como evidencia del comprobador, sin envolver cada valor en un
 objeto de validación obligatorio.

 Recursos A14
 El prototipo se apoya en la gestión de memoria del anfitrión, sin prometer tiempos de liberación.
 Las capacidades no exponen descriptores vivos al programa: cada operación lee o escribe y cierra
 su recurso antes de retornar. Con ello, un Err propagado no requiere una regla nueva de
 finalización de recursos del usuario.

 Límites
 El arnés fija presupuesto de pasos, tiempo y memoria por proceso. Superarlo produce un resultado
 externo inconcluso o de recurso agotado. No se agrega ese evento a Result ni se usa para
 demostrar divergencia. No se promete recuperación tras agotamiento de memoria.

 Costos y observabilidad
 La pila explícita y las etiquetas pueden ser costosas. Son decisiones del ejecutor de referencia;
 deberán medirse. Las trazas de pruebas no otorgan acceso a identidad física de objetos, pila o
 direcciones de memoria desde el lenguaje.




Documento 06 · Propuesta 0.1 · 20 de octubre de 2026                                                  6
````

## Página 7

````text
 6. Núcleo numérico
 Representación A15
 Representar un decimal finito como coeficiente entero y exponente decimal entero. Canonicalizar
 cero como 0e0 y retirar factores 10 del coeficiente no nulo. Conservar precisión lógica arbitraria,
 sujeta a recursos físicos. No usar float ni un contexto decimal de precisión fija como representación
 semántica.

 Operaciones
 Para suma y resta, alinear exponentes con aritmética entera; para producto, multiplicar
 coeficientes y sumar exponentes. Para comparación, usar magnitudes y exponentes antes de
 materializar grandes potencias cuando sea posible. La estrategia física puede cambiar
 manteniendo el valor exacto.

 Para división exacta, reducir la razón de enteros y comprobar que el denominador residual
 contiene sólo factores 2 y 5. Si no es así, InexactResult. El divisor cero se detecta primero. Para
 división redondeada y quantize, usar cociente y resto enteros y decidir el empate según el modo,
 con tratamiento explícito del signo.

 Escalas y conversiones
 El núcleo valida escala entera no negativa y modo conforme al documento 03. Las conversiones a
 anchos fijos ocurren después del redondeo explícito solicitado. Un desbordamiento del destino es
 NotRepresentable; una falta de recursos del anfitrión sigue siendo un fallo externo.

 format_fixed comprueba escala y cuantización y sólo agrega presentación. canonical usa la
 representación normalizada. parse_number valida la gramática decimal de intercambio sin aceptar
 NaN, infinito ni convenciones regionales.

 Oráculo A16
 El arnés mantiene una referencia racional independiente y vectores calculados manualmente. No
 reutiliza la función bajo prueba para producir su resultado esperado. Generar coeficientes
 pequeños, grandes, signos y exponentes diversos; registrar semillas y reducir los contraejemplos.

 Riesgo principal
 Un exponente compacto puede requerir una expansión enorme al sumar o formatear. Aplicar
 presupuestos externos y reportar recursos agotados. No sustituir el cálculo por redondeo,
 saturación o un límite numérico silencioso. El costo de estas entradas será una medición explícita
 del prototipo.




Documento 06 · Propuesta 0.1 · 20 de octubre de 2026                                                     7
````

## Página 8

````text
 7. Efectos y frontera anfitriona
 Registro A17
 El compilador recibe un catálogo versionado de funciones intrínsecas con nombre, firma, efectos y
 adaptador. El usuario no puede registrar código anfitrión desde el programa. El catálogo se carga
 antes de resolver nombres y no exige agregar imports a la gramática.

 Para concretar CF40, proponer estas firmas de soporte del prototipo:

 read_bytes(path: Text) -> Result<Bytes, Error> !{ReadFile}
 write_bytes(path: Text, data: Bytes)
   -> Result<Boolean, Error> !{WriteFile}

 Son firmas del catálogo, no declaraciones sin cuerpo admitidas en fuente. write_bytes devuelve
 true sólo cuando la operación solicitada finaliza correctamente; no promete atomicidad ni
 durabilidad. Un fallo de entrada/salida se adapta al Error ya disponible InvalidInput, con detalle en
 el informe externo. Ampliar la taxonomía de errores exige revisar la especificación, no crear
 variantes privadas.

 Autoridad A18
 La firma declara qué efecto puede usar una función; el registro de ejecución concede las
 capacidades efectivas. Un programa puro no adquiere autoridad porque el proceso tenga acceso a
 archivos. Las pruebas usan adaptadores en memoria que registran solicitudes y respuestas
 deterministas.

 Si falta una capacidad requerida, rechazar la configuración antes de iniciar. Para adaptadores
 reales, definir una raíz permitida, resolver rutas y enlaces, verificar el destino efectivo y cerrar los
 recursos. Estas operaciones no constituyen una sandbox de seguridad para ejecutar programas
 hostiles; esa función requerirá aislamiento específico.

 Pureza y sustitución
 Los efectos de las llamadas deben estar incluidos en el conjunto declarado por la función. Un
 intrínseco con ReadFile no puede entrar en un predicado where. Los adaptadores no pueden
 devolver un valor etiquetado con una garantía sin pasar por el mecanismo de validación de
 frontera.

 Compromiso
 Usar InvalidInput limita la clasificación de fallos de entrada/salida en esta versión. Se acepta
 provisionalmente para no inventar errores incompatibles; una biblioteca de producción necesitará
 una propuesta de errores más expresiva. El detalle externo nunca reemplaza al código observable
 devuelto al programa.




Documento 06 · Propuesta 0.1 · 20 de octubre de 2026                                                        8
````

## Página 9

````text
 8. Arnés y herramientas
 Interfaz A19
 Proponer comandos check, run y test bajo un ejecutable provisional lang-proto. No se fija nombre
 definitivo, extensión de archivo ni formato de paquete del nuevo lenguaje. check termina tras
 elaboración; run sólo ejecuta un programa aceptado; test aplica casos y oráculos.

 Entradas externas se decodifican según el tipo de cada parámetro. Number viaja como texto
 decimal, nunca como número JSON convertido a float. Registros y variantes conservan etiquetas.
 Un argumento refinado externo se valida una vez antes de invocar la función; un fallo se informa
 como rechazo de entrada del arnés, no se inventa un Result de la función.

 Manifiesto de caso
 id: CF02
 spec_version: 0.1
 source: fixtures/contracts.lang
 entry: bounded
 arguments: Number("101")
 expected_phase: execution
 expected: Err(ContractViolation)

 Es una notación de diseño; el esquema definitivo del manifiesto se fijará al implementar el arnés.
 No es sintaxis del lenguaje. El informe real incluirá revisión del ejecutor, configuración, semilla,
 resultado, duración y razón de omisión cuando corresponda.

 Trazas A20
 Registrar entrada a función, rama seleccionada, control ejecutado y efecto solicitado. Los eventos
 distinguen obligaciones demostradas de controles dinámicos; no contabilizan una prueba estática
 como una evaluación de predicado. La observación de llamadas se realiza antes de aplicar inlining;
 los benchmarks usan trazas desactivadas.

 Para CF14, una sonda interna aborta al entrar en una función elegida del fixture. Corre sólo en el
 arnés, en un proceso separado, y verifica que el segundo argumento no comenzó. No se incorpora
 al registro público ni permite provocar fallos desde un programa normal.

 Resultados separados
 Aprobado, fallido, bloqueado, omitido e inconcluso son estados diferentes. El informe conserva la
 fase responsable. Un proceso que termina correctamente puede haber devuelto Err como resultado
 previsto; el código de salida de la herramienta no sustituye al valor del lenguaje.




Documento 06 · Propuesta 0.1 · 20 de octubre de 2026                                                    9
````

## Página 10

````text
 9. Construcción y aceptación

   Incremento                            Entrega                         Puerta de aceptación

                                                                         Gramática 04 y CF37; rangos
   P1                                    Lexer, parser, resolución
                                                                         reproducibles.

                                                                         CF06–10, CF38–40; evidencia
   P2                                    Tipos, efectos y obligaciones
                                                                         revisable.

   P3                                    Núcleo y máquina de ejecución   CF01–15 con trazas y sondas.

                                                                         CF16–36 y propiedades
   P4                                    Aritmética e intercambio
                                                                         independientes.

                                                                         Casos previos, límites y errores
   P5                                    Herramientas y endurecimiento
                                                                         externos.


 El orden expresa dependencias principales: la aritmética exacta necesaria para constantes y
 pruebas se desarrolla desde P2. P4 completa su superficie y sus oráculos. P2 puede comprobar
 efectos con adaptadores simulados antes de habilitar acceso real a archivos.

 Organización del repositorio A21
 Separar spec, frontend, checker, core, runtime, numeric, capabilities, cli y tests. Las carpetas son
 una propuesta de organización, no módulos visibles del lenguaje. Conservar fixtures de aceptación
 y rechazo, manifiestos CF y pruebas de regresión para cada defecto corregido.

 Reproducibilidad
 Fijar versión del anfitrión y dependencias en el entorno de construcción. Registrar plataforma y
 configuración en los informes. La integración continua ejecuta análisis, pruebas de fase y
 conformidad; los ensayos de rendimiento se publican aparte para no convertir una variación
 temporal en cambio semántico.

 Rendimiento A22
 Medir tiempo y memoria en aritmética, listas, registros, llamadas y contratos, con entradas y
 tamaños declarados. Comparar controles demostrados y dinámicos en el mismo ejecutor. No
 extrapolar la velocidad de Python a una futura implementación nativa ni usarla como prueba para
 crear tipos especializados.

 Backend futuro
 Mantener el núcleo tipado como frontera de un backend adicional. Un backend nativo deberá pasar
 la misma batería y pruebas diferenciales frente al intérprete. Sólo eliminar controles o cambiar
 representaciones cuando preserve errores, orden observable y política de redondeo.




Documento 06 · Propuesta 0.1 · 20 de octubre de 2026                                                   10
````

## Página 11

````text
 10. Riesgos y decisiones pendientes

   Riesgo                                Tratamiento inicial                    Evidencia para reconsiderar

                                                                                Contraejemplo mínimo
   Prueba estática incorrecta            Reglas pequeñas y modo de auditoría.
                                                                                reproducible.

                                                                                Perfiles por tamaño y
   Consumo numérico extremo              Presupuestos externos y exactitud.
                                                                                exponente.

   Efectos anfitriones ocultos           Registro cerrado y adaptadores.        Trazas y pruebas de pureza.

   Dependencia del intérprete            Núcleo y pruebas independientes.       Backend diferencial conforme.



 Decisiones nuevas que requieren revisión
 A01–A22 son propuestas arquitectónicas de esta entrega. En particular, revisar la elección del
 anfitrión, el sombreado léxico, los identificadores de controles, la máquina de continuaciones, las
 firmas read_bytes y write_bytes y la adaptación provisional de sus errores. No se presentan como
 acuerdos tomados en entregas anteriores.

 Pendientes expresos
 Definir unidad de longitud de Text; ampliar errores de entrada/salida; especificar decodificación de
 esquemas y formatos externos; fijar esquema de manifiestos e informes; completar casos de
 sustitución de funciones y escapes. No es necesario resolver la interfaz binaria ni la distribución de
 paquetes para iniciar P1.

 Criterio de listo para comenzar
 La implementación puede iniciar cuando se aprueben las fronteras de fases, el modelo de
 evidencia y el alcance P1–P5. El primer objetivo es una ruta vertical pequeña: aceptar bounded,
 insertar su control, ejecutarlo con 50 y 101 y producir el valor y el informe esperados.

 Estado y validación de esta entrega
 Se ha revisado la consistencia documental y la presentación del PDF. No se construyó el intérprete
 ni se ejecutaron los casos CF sobre él. La arquitectura permite preparar esas pruebas; no
 demuestra que ya se satisfagan.

 Continuidad
 Esta propuesta queda para aprobación o corrección antes de producir el documento siguiente de la
 serie. El siguiente paso documental debe convertir los incrementos y las puertas de aceptación en
 trabajo planificado, conservando la separación entre requisitos del lenguaje y decisiones
 reemplazables del prototipo.




Documento 06 · Propuesta 0.1 · 20 de octubre de 2026                                                          11
````

