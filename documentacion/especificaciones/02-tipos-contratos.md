# 02 · Tipos y contratos

Estado: propuesta 0.1, anterior al nombre Traza.

Transcripción textual íntegra del PDF `02-especificacion-tipos-contratos.pdf`. Se conservan los saltos de línea y la disposición de tablas y código en bloques de texto para evitar una conversión Markdown que cambie su significado. Pendiente de normalización editorial y cotejo con el PDF original; no se incorpora aquí el archivo PDF binario.

Para el índice vigente de la serie y sus cambios, consultar [el índice documental](../README.md).

## Página 1

````text
 Especificación de tipos y contratos
 Nuevo lenguaje funcional · Documento 02 de 08 · Propuesta 0.1

 14 de octubre de 2026

 Propósito y alcance
 Definir cómo se representan los tipos generales, cómo se expresan las condiciones de las funciones
 y cómo se comprueban y reutilizan sus garantías. Este documento desarrolla las reglas S01, S05,
 S07, S09 y S11 a S18 de la especificación semántica mínima.

 La directriz es mantener categorías reutilizables y evitar tipos nominales específicos de negocio.
 Las restricciones añaden propiedades al tipo base sin imponer una representación de memoria
 nueva. Solo se considerarán especializaciones físicas cuando se justifiquen por ejecución o
 memoria.

 Las reglas T01 a T28 constituyen propuestas operativas para revisión. La autorización para
 continuar permite desarrollarlas con el mismo criterio de simplicidad, seguridad comprobada y
 costo medible. No demuestra que exista una implementación ni que el diseño sea original.

 Base y dependencias

   Documento                             Versión                          Relación

                                                                          Objetivo tipos generales y
   Contexto del lenguaje                 1.1
                                                                          garantías

   Project Brief                         1.0                              Alcance y criterios de éxito

                                                                          Significado de evaluación y
   Semántica mínima                      Propuesta 0.1
                                                                          retornos

                                                                          Operadores rangos y valores
   Modelo numérico                       Pendiente
                                                                          especiales

   Sintaxis y gramática                  Pendiente                        Notación definitiva


 La notación del documento es conceptual. No fija palabras reservadas ni gramática. Number
 conserva su carácter general; los resultados de operaciones y las demostraciones numéricas
 dependen del documento 03. Las firmas de efectos se expresan aquí como conjuntos abstractos,
 sin decidir su sintaxis.

 Criterio de comprobación
 El comprobador acepta propiedades demostradas, rechaza caminos exitosos refutados y exige
 comprobaciones para condiciones admitidas que no puede resolver. Nunca sustituye una prueba
 por confianza en una anotación. Una comprobación no puede entregar éxito inválido ni eliminarse
 sin evidencia.




Documento 02 · Propuesta 0.1 · 14 de octubre de 2026                                                     1
````

## Página 2

````text
 1 Categorías generales y estructuras
 T01 Catálogo conceptual
 El subconjunto incluye Number, Boolean, Text, Bytes, funciones, colecciones inmutables, registros
 y variantes. Las categorías y nombres son provisionales. No se incorporan Money, Rate ni tipos
 distintos por cada concepto de negocio.

 Option<T> representa presencia o ausencia. Result<T, E> representa éxito o error. Sus
 parámetros son tipos generales reutilizables, no etiquetas financieras. Error es una estructura
 técnica común para fallos; no especializa la representación de un número.

 T02 Registros estructurales
 Un registro se describe por nombres de campos y sus tipos. Dos descripciones equivalentes de
 campos son compatibles sin exigir un nombre nominal común. El orden de escritura de campos no
 modifica el tipo lógico; su disposición física se decidirá aparte.

 Se propone comenzar con registros cerrados: el conjunto de campos debe coincidir para su
 asignación directa. Acceder a un campo conocido es válido. Obtener un registro menor se realiza
 mediante una proyección explícita; no se introducen conversiones implícitas por descartar campos.

 T03 Colecciones y variantes
 Las colecciones tienen un tipo de elemento común y son inmutables. Su longitud puede formar
 parte de un contrato. Una colección vacía necesita contexto para determinar el tipo de sus
 elementos. No se propone una colección dinámica que omita comprobaciones.

 Las variantes identifican alternativas mediante etiquetas y cargas tipadas. Seleccionar una
 alternativa introduce únicamente las propiedades asociadas a esa alternativa. Una selección debe
 cubrir todas las posibilidades; agregar una variante puede exigir actualizar consumidores.

 T04 Ausencia y categorías incompatibles
 La ausencia se expresa mediante Option; no existe un valor nulo universal compatible con
 cualquier categoría en el subconjunto inicial. Number no se convierte implícitamente en Boolean ni
 Text en Number. Una conversión admitida tiene contrato y política de fallo explícitos.

 Esta regla no decide si distintos almacenamientos numéricos requieren conversión. Esa decisión
 corresponde al documento 03 y debe preservar los resultados definidos.




Documento 02 · Propuesta 0.1 · 14 de octubre de 2026                                                  2
````

## Página 3

````text
 2 Inferencia y parametrización
 T05 Inferencia local
 El comprobador puede inferir tipos de vinculaciones locales a partir de expresiones, patrones y
 contexto. Una firma pública debe declarar parámetros, resultado y efectos observables. Las
 restricciones del resultado que un consumidor necesita deben aparecer en esa firma.

 Si falta información para resolver un tipo o existen alternativas incompatibles, se solicita una
 anotación o se rechaza el programa con diagnóstico. No se selecciona silenciosamente una
 categoría por conveniencia del intérprete anfitrión.

 T06 Parámetros de tipo
 Se propone parametrización de primer nivel: una función puede operar uniformemente sobre un
 parámetro T, como identidad o una transformación de colecciones. El prototipo no incluirá clases
 de tipos, selección implícita de implementaciones ni cuantificación de tipos dentro de argumentos.

 identity<T>(value: T) -> T
 first<T>(values: List<T>) -> Option<T>

 T permite reutilización; no expresa un tamaño físico. Una operación exclusiva de Number no puede
 aplicarse a T sin un requisito que la habilite. El subconjunto inicial favorece declarar ese parámetro
 como Number en lugar de introducir un sistema adicional de restricciones sobre parámetros
 genéricos.

 T07 Inferencia de condiciones
 El sistema distingue categoría y condiciones conocidas. El tipo base puede inferirse aunque no se
 pruebe un contrato de rango. Inferir Number no habilita a concluir que el valor es finito o positivo.

 Un valor local puede conservar condiciones más fuertes que las publicadas por una función. Fuera
 del módulo, el consumidor solo utiliza el contrato exportado y evidencia obtenida legítimamente.
 No examina un cuerpo privado para asumir garantías ausentes de la interfaz.

 T08 Funciones recursivas
 Las funciones recursivas deben declarar sus firmas. El cuerpo se comprueba frente al contrato
 declarado y los retornos exitosos quedan sujetos a las mismas verificaciones. Una llamada
 recursiva puede reutilizar ese contrato, pero no constituye una prueba de terminación ni garantiza
 que exista algún retorno exitoso.

 No se permiten anotaciones para saltar comprobaciones ni declarar arbitrariamente propiedades
 falsas. Las optimizaciones por especialización deben conservar contratos y medirse después de
 existir una implementación.




Documento 02 · Propuesta 0.1 · 14 de octubre de 2026                                                      3
````

## Página 4

````text
 3 Forma de los contratos
 T09 Restricción sobre el tipo base
 Se escribe conceptualmente B where P para un tipo general B y un predicado P sobre su valor.
 value designa el valor al que se aplica P. En Result<B where P, E>, P corresponde al contenido
 exitoso; no condiciona al contenido del error.

 Una restricción forma parte del contrato lógico. No exige un objeto adicional ni un tipo nominal de
 dominio. El mecanismo físico para conservar evidencia corresponde al comprobador y a la
 arquitectura.

 T10 Referencias a parámetros
 Un contrato de salida puede relacionar value con parámetros inmutables de entrada cuando la
 expresión pertenece al subconjunto admitido. Los nombres se vinculan léxicamente y no pueden
 referirse a variables externas mutables. Las comparaciones entre firmas deben renombrar sus
 parámetros para evitar confundir nombres distintos con propiedades distintas.

 identity<T>(input: T) -> T
 validate(x: Number)
   -> Result<Number where 0 <= value AND value <= 100, Error>

 Las relaciones aritméticas más complejas se posponen hasta disponer de semántica numérica y
 reglas de demostración. Una relación no admitida genera diagnóstico, no una condición ignorada.

 T11 Requisitos de entrada
 Una función puede exigir una condición en su parámetro general. Su cuerpo puede asumirla
 porque el comprobador impide llamadas incompatibles. Cuando no existe evidencia suficiente, el
 consumidor debe establecer la condición mediante una operación explícita de comprobación antes
 de llamar.

 Esta propuesta evita introducir fallos de entrada invisibles dentro de funciones cuyo retorno no los
 declara. La comprobación explícita devuelve Result y permite manejar el fallo. Si el consumidor ya
 tiene la garantía requerida, llama directamente sin repetir controles.

 T12 Contratos verificables
 Los predicados deben ser puros, terminantes y bien tipados. El contrato no puede consultar reloj,
 red, archivos ni estado mutable. Esas propiedades necesitan protocolos de vigencia externos.

 El prototipo rechazará contratos que estén fuera de su subconjunto expresivo. No admite promesas
 sin prueba, conversiones inseguras ni llamadas arbitrarias a funciones dentro de una condición.




Documento 02 · Propuesta 0.1 · 14 de octubre de 2026                                                    4
````

## Página 5

````text
 4 Predicados y procedimiento de demostración
 T13 Subconjunto inicial de predicados

   Forma conceptual                      Uso admitido                    Restricción

   TRUE y FALSE                          Condiciones constantes          Boolean

   AND OR NOT                            Composición y negación          Operandos booleanos

                                                                         Comparación numérica
   x comparado con una constante         Rango o igualdad
                                                                         definida

   x comparado con otro parámetro        Relación simple                 Misma categoría comparable

   length(x) comparado con                                               Bytes o colección con unidad
                                         Longitud
   constante                                                             definida

   Campo conocido y su predicado         Propiedad estructural           Acceso bien tipado

   Variante seleccionada                 Presencia o éxito               Caso demostrado por patrón


 La longitud de Text queda pendiente de definir unidad, por ejemplo bytes o caracteres. No se
 reutiliza la longitud de Bytes como si fuera longitud textual. Presencia de campo de un registro
 cerrado se resuelve estáticamente; para entradas externas se comprueba al decodificar.

 T14 Evidencia disponible
 El comprobador reúne tipos, condiciones de parámetros admitidos, resultados exitosos validados y
 hechos de ramas seleccionadas. Una prueba debe ser válida bajo esa evidencia y bajo la semántica
 de cada operación. No incorpora hechos procedentes de un servicio externo como verdades
 permanentes.

 T15 Procedimiento inicial
 Se propone normalizar nombres y condiciones, resolver constantes, propagar intervalos y usar
 relaciones simples disponibles en la evidencia. AND permite acumular hechos. OR requiere que la
 conclusión sea válida en todas las alternativas que continúan; si eso no puede establecerse, el
 resultado es desconocido.

 El comprobador devuelve demostrada, refutada o desconocida. Refutada requiere demostrar que
 el contrato falla en un camino alcanzable; la falta de prueba no es refutación. Los caminos
 imposibles no obligan a validar un retorno inaccesible. Si el análisis no puede resolver alcance o
 implicación, mantiene desconocida.

 T16 Conservación de exactitud lógica
 El procedimiento debe ser conservador: puede dejar de demostrar una propiedad verdadera, pero
 no afirmar una propiedad falsa. Los resúmenes de operadores deben validarse frente al documento
 03. No se permite trasladar algebra de números reales a operaciones con redondeo o
 desbordamiento sin justificación.




Documento 02 · Propuesta 0.1 · 14 de octubre de 2026                                                    5
````

## Página 6

````text
 5 Reglas de compatibilidad y composición
 T17 Compatibilidad de valores
 B where P satisface un requisito B where Q si las categorías coinciden y la evidencia permite
 demostrar que P implica Q. Un valor restringido puede usarse como su categoría base, aunque una
 interfaz que publique solo B no comunica P a otros consumidores.

 Si las categorías son incompatibles se rechaza la operación. Si la categoría coincide pero la
 condición es desconocida se necesita comprobarla. El comprobador puede conservar hechos
 locales aunque no se anoten en el nombre de una vinculación.

 T18 Composición directa y comprobación explícita
 source() -> Result<Number where 0 <= value AND value <= 100, Error>
 consume(x: Number where 0 <= value) -> Number

 Al obtener éxito de source, consume admite ese contenido sin comprobar nuevamente la no
 negatividad. Si consume exige value < 50, la evidencia anterior no alcanza: el programa debe
 verificar esa condición y tratar su posible fallo.

 Se propone una operación conceptual check(value, condition) que devuelve Result con el mismo
 valor validado. La condición está restringida por T12 y T13. Si ya se demuestra, el control dinámico
 puede omitirse; si no se cumple, devuelve Error. La sintaxis de esta operación se definirá en el
 documento 04.

 T19 Colecciones registros y variantes
 Como los valores son inmutables, las propiedades comprobadas de elementos pueden conservarse
 al leerlos. Sin embargo, el prototipo solo permite compatibilidad directa de contenedores cuando
 sus descripciones coinciden o cuando una regla de refinamiento ha sido expresamente definida.

 No se incorporan en esta versión reglas generales de covarianza, conversiones de listas ni
 subtipado por descarte de campos. Una transformación o proyección explícita produce otro valor y
 establece su contrato. Esto limita complejidad sin impedir datos generales.

 T20 Funciones como valores
 Para sustituir una función, la candidata debe aceptar al menos las entradas que espera el
 consumidor, entregar resultados que satisfagan su contrato y no añadir efectos no autorizados. No
 puede exigir una precondición más fuerte ni prometer una salida más débil.

 El prototipo comienza con categorías estructurales coincidentes y compara las restricciones de
 entrada y salida mediante T15. Una relación desconocida requiere un adaptador explícito
 comprobado o rechazo; no genera envoltorios ocultos. Las condiciones relativas a parámetros se
 comparan después de renombrarlos.




Documento 02 · Propuesta 0.1 · 14 de octubre de 2026                                                    6
````

## Página 7

````text
 6 Retornos y fallos de contrato
 T21 Retorno demostrado o refutado
 Un retorno exitoso demostrado satisface el contrato sin otro control. Un retorno exitoso que se
 demuestra inválido en un camino accesible se rechaza. La firma no autoriza a sustituir el valor por
 otro ni a convertir ese defecto silenciosamente en éxito.

 Entregar un error esperado para una entrada inválida es correcto. El predicado de éxito no se
 verifica sobre esa variante de error. Las ramas de una función deben respetar el tipo declarado,
 incluidos sus fallos.

 T22 Retorno desconocido
 Cuando un contrato admitido no se demuestra, se inserta una comprobación en la frontera de
 éxito. Primero se evalúa el contenido candidato una vez; después se comprueba su condición. Se
 entrega éxito solo si la condición es verdadera.

 En el subconjunto inicial, las funciones con esta necesidad deben retornar Result cuyo tipo de error
 admita el fallo de contrato. Un retorno restringido directo, sin Result, exige demostración estática;
 si no existe, se rechaza y se sugiere declarar el fallo. No se convierte automáticamente la firma.

 T23 Estructura general de error
 Se propone Error como una variante técnica común. Los fallos de entrada y de operación pueden
 representarse mediante categorías generales, y ContractViolation identifica un incumplimiento de
 la condición en una frontera.

 ContractViolation debe registrar un identificador de condición, ubicación y clase de frontera,
 entrada o retorno. No requiere guardar el dato completo que incumplió la condición. Un registro de
 auditoría puede añadir contexto bajo política definida.

 Result<T, E> sigue siendo general. Si E no puede representar ContractViolation, no se introduce
 ese fallo a escondidas: se demuestra el contrato o se exige cambiar explícitamente la firma o el
 adaptador. La representación concreta de Error corresponde a gramática y arquitectura.

 T24 Propagación explícita
 La variante de error de Result es un valor. No interrumpe por sí misma una llamada ordinaria,
 conforme a S03. El consumidor selecciona el caso o utiliza una operación explícita de propagación
 que respeta el tipo de error de su propio retorno. No existe extracción de éxito sin comprobación ni
 fallo descartado implícitamente.




Documento 02 · Propuesta 0.1 · 14 de octubre de 2026                                                     7
````

## Página 8

````text
 7 Garantías en ramas transformaciones y módulos
 T25 Evidencia en patrones y ramas
 Seleccionar éxito introduce las condiciones de ese contenido; seleccionar error no las introduce.
 Seleccionar presencia en Option habilita usar el contenido. Una rama que exige x >= 0 puede
 añadir ese hecho mientras siga esa rama, si la comparación tiene semántica válida.

 Cuando confluyen ramas, solo se publican garantías que sean válidas en todos los caminos
 exitosos que continúan. La información específica de una rama no se conserva como afirmación
 universal. Un retorno con fallo no se confunde con un éxito para calcular estas obligaciones.

 T26 Transformación e inmutabilidad
 Otra vinculación del mismo valor conserva evidencia. Una transformación produce otro valor:
 conserva únicamente condiciones demostradas por la operación y la evidencia disponible. Si falta
 un resumen válido del operador, no se propaga automáticamente un rango.

 La inmutabilidad observable impide que otra parte cambie el contenido y vuelva falsa su
 propiedad. Una frontera insegura o una representación externa requiere restablecer las garantías.
 Ninguna propiedad de saldo actual o archivo existente se conserva indefinidamente por haberse
 validado una vez.

 T27 Contratos entre módulos
 El consumidor comprueba una interfaz que incluye tipos generales, predicados exportados, efectos
 y versión de semántica pertinente. Cambiar un requisito de entrada a uno más fuerte puede
 romper consumidores; debilitar una garantía de salida también.

 Se propone comprobar el programa completo en el prototipo. La compilación separada y los
 certificados de interfaces quedan fuera del alcance inicial. Un artefacto externo no obtiene
 confianza solo por incluir una firma: requiere comprobación compatible o una frontera validada.

 T28 Efectos y recursos
 Una función pura no admite llamadas con efectos. Una función con efectos no puede exceder los
 autorizados por su interfaz. El conjunto exacto de etiquetas está pendiente; el comprobador debe
 impedir que se oculten bajo un retorno general.

 Las propiedades de recursos no sustituyen garantías sobre valores. La duración de manejadores y
 las clausuras que los capturan requieren un modelo específico en la arquitectura. Estas
 restricciones técnicas no reintroducen tipos nominales de negocio ni prometen recuperación de
 fallos del proceso.




Documento 02 · Propuesta 0.1 · 14 de octubre de 2026                                                 8
````

## Página 9

````text
 8 Diagnósticos y escenarios de conformidad
 Cada diagnóstico debe indicar ubicación, categoría encontrada, requisito esperado, condición y
 evidencia relevante. Debe distinguir refutación de falta de prueba y sugerir anotación,
 comprobación explícita o declaración del fallo cuando corresponda.

   Código     Situación                                        Respuesta

   D01        Categorías incompatibles                         Rechazo de operación

   D02        Información de tipo insuficiente                 Solicitar anotación

   D03        Predicado no admitido o impuro                   Rechazar contrato

   D04        Llamada sin precondición demostrada              Exigir comprobación explícita

   D05        Éxito demostrado inválido                        Rechazar retorno

   D06        Retorno desconocido sin fallo representable      Exigir Result compatible o demostración

   D07        Variante no cubierta                             Rechazar selección

   D08        Efecto fuera del contrato                        Rechazar función o llamada



 Pruebas específicas del documento

   Caso     Escenario                                                    Evidencia esperada

   TC01     Rango 0 a 100 usado como no negativo                         Llamada sin control repetido

   TC02     Mismo rango usado como menor que 50                          D04 hasta verificar condición

   TC03     Retorno desconocido con Result y Error                       Comprobar antes de éxito

   TC04     Mismo retorno sin Result                                     D06

   TC05     Retorno exitoso constante fuera de rango                     D05

   TC06     Error esperado en lugar de éxito                             No aplicar predicado al error

   TC07     Condición de una sola rama exportada como universal          Rechazo o control pendiente

   TC08     Función sustituta exige entrada más fuerte                   Rechazo de compatibilidad

   TC09     Firma recursiva usada como prueba de terminación             Garantía no disponible

   TC10     Text y Bytes usan longitud sin unidad común                  No presumir compatibilidad


 Los casos numéricos dependen del documento 03. Los controles eliminados requieren evidencia
 del comprobador o instrumentación, no solo resultados correctos.



Documento 02 · Propuesta 0.1 · 14 de octubre de 2026                                                     9
````

## Página 10

````text
 9 Decisiones y trazabilidad

   Decisión propuesta                    Criterio                                    Base semántica

   Registros estructurales cerrados      Simplicidad sin tipos de negocio            S01 S05

   Genéricos de primer nivel             Reutilización y alcance limitado            S06 S07

   Comprobación explícita de
                                         Fallos visibles y sin controles repetidos   S07 S16
   entradas desconocidas

   Restricciones directas solo si
                                         No agregar un fallo oculto                  S12 S18
   demostradas

   Retornos desconocidos mediante
                                         Éxito validado o error declarado            S12 S18
   Result compatible

   Comprobador conservador de
                                         Evitar confianza en condiciones falsas      S13 S15
   intervalos y hechos simples

   Programa completo antes de
                                         Reducir fronteras de confianza              S14 S17
   compilación separada



 Decisiones pendientes
 El modelo numérico debe definir Number, comparaciones, valores especiales y resúmenes de
 operadores. La gramática debe fijar contratos, patrones, declaración de genéricos y check. La
 arquitectura debe definir efectos, duración de recursos, formato de diagnósticos y medición de
 controles. La longitud de Text requiere una unidad explícita.

 La propuesta no incorpora tipos dependientes generales, predicados arbitrarios, coerciones
 ocultas, clases de tipos ni especializaciones físicas sin evidencia. Puede ampliarse el subconjunto si
 casos concretos justifican su costo y sus reglas de comprobación.

 Base documental y revisión
 Se utilizan el contexto 1.1, el Project Brief 1.0 y la especificación semántica mínima propuesta 0.1.
 Las reglas aquí concretadas no alteran la evaluación estricta ni convierten una variante de error en
 interrupción automática.

 La revisión debe concentrarse en la simplicidad de registros y genéricos, el control explícito de
 entradas, Result para retornos no demostrados, la distinción entre refutado y desconocido, y la
 política de garantías entre módulos.

 El siguiente documento es el modelo numérico. Cerrará exactitud, representación, rango,
 desbordamiento, división y redondeo sin trasladar comportamientos accidentales del anfitrión. La
 serie se detiene aquí hasta recibir autorización para continuar o correcciones de este documento.




Documento 02 · Propuesta 0.1 · 14 de octubre de 2026                                                  10
````

