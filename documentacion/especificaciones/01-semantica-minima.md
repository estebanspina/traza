# 01 · Semántica mínima

Estado: propuesta 0.1, anterior al nombre Traza.

Transcripción textual íntegra del PDF `01-especificacion-semantica-minima.pdf`. Se conservan los saltos de línea y la disposición de tablas y código en bloques de texto para evitar una conversión Markdown que cambie su significado. Pendiente de normalización editorial y cotejo con el PDF original; no se incorpora aquí el archivo PDF binario.

Para el índice vigente de la serie y sus cambios, consultar [el índice documental](../readme.md).

## Página 1

````text
 Especificación semántica mínima
 Nuevo lenguaje funcional · Documento 01 de 08 · Propuesta 0.1

 14 de octubre de 2026

 Propósito y alcance
 Esta especificación propone el significado del subconjunto inicial del lenguaje. Define cómo se
 evalúan expresiones y funciones, cómo se entregan resultados y cómo se conservan sus garantías.
 Es la primera pieza técnica para construir un intérprete de referencia y pruebas de conformidad.

 La base es el documento de contexto versión 1.1 y el Project Brief versión 1.0. Se mantienen las
 directrices del usuario: lenguaje funcional nuevo, tipos generales y retornos que eviten repetir
 validaciones. Las reglas operativas detalladas aquí son propuestas para revisión; no se presentan
 como decisiones previamente aprobadas ni capacidades implementadas.

 El nombre, la gramática, las representaciones numéricas y el modelo físico de memoria no se fijan
 en este documento. La sintaxis de los ejemplos es ilustrativa. La implementación de aritmética y
 sus pruebas completas dependen del documento de modelo numérico.

 Organización del conjunto documental

   Orden                                 Documento                         Propósito

   01                                    Especificación semántica mínima   Significado del programa

                                                                           Reglas de comprobación y
   02                                    Tipos y contratos
                                                                           composición

                                                                           Exactitud representación y
   03                                    Modelo numérico
                                                                           políticas

   04                                    Sintaxis y gramática inicial      Estructura de programas

                                                                           Resultados y rechazos
   05                                    Casos de conformidad
                                                                           esperados

   06                                    Arquitectura del prototipo        Componentes del intérprete

                                                                           Elecciones alternativas y
   07                                    Registro de decisiones
                                                                           pendientes

   08                                    Guía y referencia del lenguaje    Aprendizaje y consulta



 Lectura de las reglas
 Los identificadores S01 a S24 permiten relacionar significado, implementación y pruebas. “Debe”
 expresa un requisito de esta propuesta; su adopción queda sujeta a la revisión del documento. Las
 cuestiones no resueltas se enumeran al final. No se atribuye originalidad a cada mecanismo por
 separado.


Documento 01 · Propuesta 0.1 · 14 de octubre de 2026                                                    1
````

## Página 2

````text
 1 Modelo de valores y evaluación
 S01 Valores generales
 El subconjunto contempla números, booleanos, texto, bytes, colecciones, registros, variantes y
 funciones. Number, Boolean, Text y Bytes son etiquetas conceptuales. Option y Result son
 construcciones generales para ausencia y fallo. Sus nombres definitivos pertenecen a la gramática.

 Un dato de negocio puede organizarse en un registro sin convertirse en un tipo nominal
 especializado. Las condiciones de validez se expresan en contratos. Una restricción lógica no
 implica un formato de memoria distinto.

 S02 Vinculaciones inmutables
 Una vinculación asocia un nombre con un valor y no admite reasignación. Crear otro valor no
 modifica el anterior. El intérprete puede compartir o reutilizar almacenamiento si el programa no
 puede observar una diferencia. Esta regla no selecciona recolector, conteo de referencias ni
 propiedad física.

 S03 Evaluación estricta y orden
 Una llamada evalúa primero la expresión que identifica la función y después sus argumentos de
 izquierda a derecha. Solo invoca el cuerpo si todas esas evaluaciones terminan con valores. Un
 fallo del evaluador o falta de terminación anterior impide evaluar los argumentos siguientes. La
 variante de error de Result sigue siendo un valor: no interrumpe una llamada ordinaria sin una
 operación explícita de propagación.

 Las expresiones secuenciales se evalúan en el orden escrito. El orden forma parte del
 comportamiento especificado, incluyendo qué fallo aparece primero. Una optimización puede
 cambiar la ejecución interna únicamente si preserva lo observable definido por estas reglas.

 S04 Evaluación condicional
 La condición de una elección debe ser Boolean. Solo se evalúa la rama seleccionada. Los
 operadores lógicos AND y OR operan sobre Boolean y cortocircuitan: AND omite el segundo
 operando cuando el primero es falso; OR lo omite cuando el primero es verdadero.

 Esto no contradice la evaluación estricta de llamadas: condicionales y operadores lógicos son
 formas especiales. Una función ordinaria no recibe argumentos sin evaluar por usar el mismo
 nombre de una operación lógica.

 S05 Sin conversiones implícitas entre categorías
 No se interpreta un número como booleano ni un texto como número de manera automática. Una
 conversión explícita devuelve un valor o un fallo definido. Las promociones entre representaciones
 numéricas se resolverán en el modelo numérico, conservando la categoría general elegida.




Documento 01 · Propuesta 0.1 · 14 de octubre de 2026                                                  2
````

## Página 3

````text
 2 Funciones alcance y control
 S06 Funciones y entorno léxico
 Las funciones son valores y pueden recibirse o devolverse. Una función utiliza el entorno léxico de
 su definición, no el entorno de quien la llama. Una clausura conserva las vinculaciones inmutables
 que necesita. Los recursos externos capturados mantienen sus restricciones de duración; no se
 convierten en valores puros por quedar dentro de una clausura.

 S07 Entradas y resultados
 Una función declara parámetros y un contrato de salida. Una expresión final produce su resultado;
 las formas sintácticas concretas se definirán después. La firma pública debe exponer las garantías
 que otros módulos pueden utilizar. El consumidor no puede asumir condiciones que solo estén
 implícitas en el cuerpo.

 Los requisitos de entrada deben ser compatibles con las garantías del argumento. Si se demuestra
 esa compatibilidad, no hace falta otro control. Si no se demuestra, la llamada necesita una
 comprobación definida o debe rechazarse. El documento 02 fijará la inserción de controles y la
 forma de expresar esos requisitos.

 S08 Pureza
 Una función pura calcula exclusivamente a partir de sus argumentos y vinculaciones puras
 capturadas. No puede consultar ni modificar archivos, red, reloj, estado externo o estado mutable
 compartido. Los mismos valores de entrada, bajo la misma semántica, tienen el mismo
 comportamiento de cálculo: valor, fallo o falta de terminación.

 Pureza no demuestra que la regla de negocio sea correcta ni que la función termine. La mutación
 interna exclusiva se permite únicamente cuando conserva esta semántica.

 S09 Control por variantes
 Result distingue éxito y fallo; Option distingue presencia y ausencia. Acceder a su contenido
 requiere seleccionar la variante correspondiente mediante un patrón o una operación comprobada.
 No existe extracción ordinaria que presuma éxito o presencia.

 Una selección de patrones debe cubrir las variantes posibles. Patrones superpuestos, su prioridad y
 su sintaxis pertenecen al documento 04; el subconjunto inicial favorecerá casos disjuntos. Una
 operación como primer elemento devuelve ausencia si la colección puede estar vacía.

 S10 Recursión y diferimiento
 Las funciones pueden ser recursivas. El lenguaje no garantiza terminación general. El subconjunto
 inicial no incluye evaluación diferida implícita. Una capacidad de diferimiento explícito queda para
 una revisión posterior; los flujos de entrada se tratarán como operaciones de procesamiento, sin
 convertir todo el lenguaje en no estricto.




Documento 01 · Propuesta 0.1 · 14 de octubre de 2026                                                    3
````

## Página 4

````text
 3 Establecimiento de contratos de retorno
 S11 Tipo base y condición
 Un contrato especifica una categoría general y puede añadir condiciones sobre el resultado. En
 Result, la condición se aplica al contenido del caso exitoso, no a la variante de fallo. Declarar
 Number solo demuestra la categoría; no demuestra finitud, signo, rango ni representabilidad.

 fn validar(valor: Number)
   -> Result<Number where 0 <= value <= 100, Error>

 value designa el contenido exitoso en este ejemplo. No introduce un tipo nominal de negocio. El
 significado de comparaciones numéricas, incluidos los valores no finitos si existieran, debe quedar
 fijado por el documento 03 antes de implementar esta condición.

 S12 Comprobación estática y dinámica
 La propuesta distingue tres situaciones. Una condición demostrada no necesita comprobación
 dinámica. Una condición que se demuestra falsa para un camino de éxito accesible impide aceptar
 ese programa. Una condición desconocida debe comprobarse antes de entregar el éxito, siempre
 que pertenezca al subconjunto admitido.

   Evidencia disponible                            Tratamiento propuesto

   Condición demostrada                            Aceptar y conservar la garantía

   Condición refutada                              Rechazar el camino de éxito inválido

   Condición no resuelta pero comprobable          Comprobar antes de publicar éxito

   Condición no admitida                           Rechazar el contrato con diagnóstico


 Entregar explícitamente un fallo por una entrada inválida es correcto. Es distinto de intentar
 devolver como éxito un valor que se sabe fuera de contrato. Una comprobación dinámica
 pendiente no puede omitirse mediante una opción de optimización del núcleo seguro.

 S13 Predicados iniciales
 Se recomienda comenzar con comparaciones de rango, conectores booleanos y propiedades
 estructurales simples como longitud y presencia de campos, cuando su significado esté definido.
 Las comprobaciones deben ser puras y terminantes. En esta versión no se admiten como
 predicados llamadas arbitrarias recursivas, entrada y salida ni consultas a estado externo.

 El listado formal de expresiones admitidas y el algoritmo del comprobador corresponden al
 documento 02. Una condición no soportada genera un diagnóstico; no se transforma
 silenciosamente en una afirmación de confianza.




Documento 01 · Propuesta 0.1 · 14 de octubre de 2026                                                   4
````

## Página 5

````text
 4 Conservación y composición de garantías
 S14 Garantías vinculadas al valor
 Al seleccionar el caso exitoso, el consumidor obtiene su contenido junto con las condiciones
 establecidas. Asignar ese valor a otra vinculación inmutable conserva las garantías. Pasarlo a una
 función conserva las propiedades conocidas, sin otorgar a esa función permisos adicionales sobre
 recursos externos.

 La representación exacta de esta evidencia es una decisión de implementación. No se requiere
 almacenar un certificado junto a cada valor; la garantía puede quedar en el análisis estático y en
 los contratos de módulos.

 S15 Transformaciones
 Una transformación produce otro valor. No hereda automáticamente todas las condiciones del
 original. El comprobador puede demostrar propiedades nuevas o conservar las que siguen siendo
 válidas. Cuando falta evidencia, el nuevo contrato requiere una comprobación.

 Un número entre 0 y 100 multiplicado por dos puede alcanzar 200. La conclusión de que queda
 entre 0 y 200 solo es válida bajo operaciones que no alteren ese razonamiento por
 desbordamiento, redondeo o valores especiales. La semántica numérica tiene prioridad sobre
 simplificaciones algebraicas.

 S16 Composición
 Si la salida de una función establece P y la siguiente exige Q, la composición evita controles
 adicionales cuando el comprobador demuestra que P implica Q. Si no puede demostrarlo, se
 comprueba Q o se rechaza la composición según el mecanismo definido en el documento 02.

   Salida establecida                    Requisito siguiente             Consecuencia

   Valor entre 0 y 100                   Valor no negativo               Compatible sin repetir rango

                                                                         Hace falta evidencia o
   Valor entre 0 y 100                   Valor menor que 50
                                                                         comprobación

                                                                         Reutilizar propiedades
   Registro validado por esquema         Mismo esquema y versión
                                                                         conservadas

   Registro validado por esquema         Esquema distinto                No presumir compatibilidad



 S17 Fronteras y vigencia
 Deserialización, entradas externas y fronteras inseguras deben establecer o restablecer las
 garantías pertinentes. Una propiedad de un valor inmutable permanece; una afirmación sobre el
 entorno puede caducar. Existencia de un archivo, saldo disponible y respuesta de un servicio
 requieren condiciones de vigencia o protocolos explícitos.

 Esta especificación no convierte hechos externos en garantías permanentes. La compatibilidad de
 contratos entre versiones de módulos debe definirse antes de introducir compilación separada o
 intercambio de artefactos.




Documento 01 · Propuesta 0.1 · 14 de octubre de 2026                                                    5
````

## Página 6

````text
 5 Fallos y comportamiento numérico
 S18 Fallos representados
 Los fallos esperables son valores de la variante de error de Result. El consumidor debe manejarlos
 o propagarlos. La ausencia en Option no equivale automáticamente a un error. Un éxito validado
 puede utilizarse sin repetir su condición, pero esto no elimina la posibilidad de que una llamada
 devuelva fallo.

 Se propone que una función con retorno restringido que necesite comprobación dinámica utilice
 Result en el subconjunto inicial. Si esa comprobación falla, se entrega un error general de
 incumplimiento de contrato y nunca el éxito inválido. Su nombre, campos y reglas de propagación
 se precisarán en el documento 02. Esta elección es nueva y está pendiente de aprobación.

 S19 Fallos del proceso
 Agotamiento de memoria, fallo del runtime y terminación forzada son fallos del proceso; no se
 garantiza convertirlos siempre en valores Result. La falta de terminación tampoco es un resultado
 de error automático. La arquitectura deberá definir diagnósticos y liberación de recursos cuando
 sean posibles, sin prometer recuperación universal.

   Situación                                       Tratamiento

   Entrada inválida reconocida                     Fallo esperado expresado con Result

   Retorno exitoso refutado                        Rechazo antes de ejecutar

   Contrato dinámico incumplido                    Error de contrato antes de éxito

   Recurso del proceso agotado                     Fallo del proceso con política del runtime

   Función que no termina                          No produce resultado; sin garantía de detección



 S20 Operaciones numéricas
 El lenguaje debe definir exactitud, rango, desbordamiento, división y redondeo antes de habilitar
 una operación numérica. No se admite envolver silenciosamente el resultado en aritmética
 ordinaria. Una reducción de escala exige política explícita. Los literales destinados a cálculo
 decimal no deben perder precisión por una conversión previa a flotante binario.

 El documento 03 decidirá la representación, los tipos o contextos necesarios y los fallos de cada
 operador. Hasta entonces, los ejemplos de enteros pequeños son escenarios de aceptación
 propuestos, no una especificación completa de Number. Un operador sin semántica numérica
 cerrada no puede convertirse en una característica implementada por conveniencia.




Documento 01 · Propuesta 0.1 · 14 de octubre de 2026                                                  6
````

## Página 7

````text
 6 Efectos formatos y optimizaciones
 S21 Efectos y capacidades
 Leer o escribir archivos, acceder a red y consultar un reloj son efectos explícitos. Una función pura
 no puede invocarlos. Las funciones con efectos deben declarar sus dependencias observables; un
 manejador o capacidad restringe sobre qué recurso operan. La forma exacta de los tipos de efectos
 queda abierta.

 La primera implementación limitará los efectos a los necesarios para el caso conductor.
 Transacciones distribuidas, idempotencia y reintentos no se obtienen por declarar efectos y
 quedan a cargo de sus protocolos.

 S22 Esquemas externos
 Decodificar bytes produce Result con un registro cuyas propiedades comprobadas quedan
 expresadas en su contrato. Codificar debe verificar que el valor pueda representarse. El esquema y
 su versión determinan cuáles son esas propiedades.

 La equivalencia semántica no asegura identidad binaria después de decodificar y volver a codificar.
 Si se exige conservar exactamente los bytes, debe conservarse también la información que una
 normalización podría descartar.

 S23 Observaciones y optimización
 El comportamiento observable comprende resultado, variante de fallo, efectos y su orden definido,
 y ausencia de resultado por falta de terminación. Consumo físico de memoria y tiempo se medirán,
 pero esta semántica no les asigna valores exactos universales.

 No se permite eliminar una comprobación pendiente ni cambiar el lugar del redondeo si eso altera
 el resultado. Reagrupar sumas acotadas exige demostrar que preserva fallos y valores. Para
 optimizar una función pura también hay que considerar su posibilidad de fallar o no terminar:
 pureza por sí sola no autoriza omitir su evaluación.

 S24 Ejecución del programa
 El prototipo ejecutará una entrada designada y devolverá un resultado o fallo según las reglas del
 subconjunto. El nombre de la entrada, el protocolo con el sistema operativo y los códigos de salida
 se definirán en la arquitectura. Los registros se procesarán secuencialmente en el alcance inicial.

 No se prometen paralelismo automático, reinicios seguros ni publicación exactamente una vez. La
 ejecución auditable requiere registrar versiones, entradas y políticas relevantes; el formato de ese
 registro corresponde a herramientas y operación.




Documento 01 · Propuesta 0.1 · 14 de octubre de 2026                                                     7
````

## Página 8

````text
 7 Escenarios mínimos de conformidad
 Estos escenarios fijan comportamientos esperados para revisar la propuesta. El documento 05 los
 convertirá en programas completos, datos y resultados reproducibles. Los casos numéricos se
 habilitarán cuando el documento 03 cierre sus operaciones.

   Caso     Escenario                                                   Resultado esperado

   C01      Condición falsa con rama no terminante no seleccionada      Solo evaluar la rama elegida

            Primer argumento falla en el evaluador y el segundo tiene
   C02                                                                  No evaluar el segundo argumento
            efecto

   C03      Reasignar una vinculación existente                         Rechazo del programa

   C04      Función pura intenta leer un archivo                        Rechazo por efecto incompatible

   C05      Selección omite una variante posible                        Rechazo por falta de exhaustividad

   C06      Éxito constante 101 con contrato entre 0 y 100              Rechazo del retorno inválido

   C07      Éxito desconocido que cumple rango en ejecución             Éxito con garantía conservada

   C08      Éxito desconocido que no cumple rango                       Error de contrato; no publicar éxito

   C09      Consumidor exige no negatividad de rango 0 a 100            Composición sin nueva validación

   C10      Consumidor exige menor que 50                               Control adicional o rechazo definido

   C11      Resultado modificado deja de cumplir condición              No conservar la condición inválida

   C12      Predicado contractual recursivo arbitrario                  Rechazo por condición no admitida

   C13      Registro corrupto en decodificación                         Fallo sin registro exitoso inválido

   C14      Reordenar redondeo cambia importe                           Optimización no permitida



 Qué demuestra cada grupo
 C01 a C05 comprueban evaluación y control. C06 a C12 comprueban que una garantía no es una
 anotación opcional y que su consumo no exige controles redundantes. C13 y C14 comprueban las
 fronteras de representación y aritmética.

 Un intérprete correcto debe satisfacer todos los casos de su subconjunto declarado. Eliminar
 controles redundantes necesita evidencia adicional de ejecución o del comprobador; obtener el
 mismo resultado no demuestra por sí solo que un control haya sido eliminado.




Documento 01 · Propuesta 0.1 · 14 de octubre de 2026                                                           8
````

## Página 9

````text
 8 Decisiones propuestas y dependencias
 Las decisiones de esta tabla completan aspectos que el contexto dejaba abiertos. Se presentan
 para aprobación junto con la especificación, sin dar por cerrados los documentos siguientes.

   Propuesta de esta versión             Motivo                                 Documento que la precisa

   Argumentos de izquierda a
                                         Orden y primer fallo previsibles       Sintaxis y arquitectura
   derecha

   Condición exclusivamente
                                         Evitar conversiones ambiguas           Tipos y gramática
   booleana

   Alcance léxico y vinculaciones
                                         Dependencias de funciones estables     Tipos y arquitectura
   inmutables

                                         Comprobación manejable y
   Predicados iniciales restringidos                                            Tipos y contratos
                                         terminante

   Result para retorno restringido       Expresar fallo sin entregar éxito
                                                                                Tipos y contratos
   comprobado en ejecución               inválido

   Rechazo de éxito estáticamente
                                         Detectar defectos antes de ejecución   Tipos y contratos
   refutado

   Recursión sin garantía general
                                         Mantener alcance implementable         Arquitectura
   de terminación



 Asuntos que no se resuelven todavía
 La representación de Number, su rango, los valores no finitos y sus operaciones dependen del
 modelo numérico. La sintaxis de requisitos de entrada, los subtipos por condiciones y la evidencia
 entre módulos dependen de tipos y contratos. La gramática debe fijar precedencia, patrones y
 módulos. El runtime debe fijar política de recursos, fallos de proceso e interfaz de ejecución.

 El objetivo de evitar validaciones repetidas no implica demostrar cualquier propiedad ni reducir
 automáticamente ciclos de reloj. Se medirán controles, tiempo de comprobación, asignaciones y
 memoria. Los tipos especializados solo se justificarán conforme al criterio establecido por el
 usuario.

 Condiciones para pasar al prototipo
 Se necesita revisar esta semántica y resolver en los documentos 02 a 04 las dependencias
 necesarias para el caso conductor. Después se implementarán el parser, la representación del
 programa, el comprobador y el evaluador. Esta especificación no autoriza sustituir decisiones
 pendientes por comportamientos accidentales del lenguaje anfitrión.




Documento 01 · Propuesta 0.1 · 14 de octubre de 2026                                                       9
````

## Página 10

````text
 9 Trazabilidad y revisión

   Bloque semántico                                Base documental

   Tipos generales y ausencia de tipos de
                                                   Contexto 1 y 12; Brief 4 y 6
   negocio

   Estrictitud inmutabilidad y funciones           Contexto 8 y 11; Brief 5 y 6.1

   Contratos y conservación de garantías           Contexto 11.1 a 11.3; Brief 6.2 y 6.3

   Exactitud y políticas numéricas                 Contexto 10 y 12; Brief 6.4

   Esquemas efectos y recursos                     Contexto 13 y 14; Brief 6.5 y 11

   Conformidad y prototipo limitado                Contexto 17 a 20; Brief 7 a 9



 Fuentes del proyecto
 Contexto para diseñar un nuevo lenguaje funcional, versión documental 1.1, 14 de octubre de
 2026. Project Brief del nuevo lenguaje funcional, versión 1.0, 14 de octubre de 2026. La
 terminología y los ejemplos de esta especificación concretan esas fuentes y las directrices de la
 conversación.

 Las referencias a C, COBOL y Haskell explican la inspiración. Ninguna regla de esta propuesta se
 presenta como conclusión obligatoria de esos lenguajes ni como originalidad demostrada.

 Puntos de revisión prioritaria
 1. Confirmar que las restricciones sobre tipos generales cumplen la simplicidad buscada.

 2. Revisar la propuesta de Result para retornos restringidos con controles dinámicos.

 3. Confirmar el rechazo de retornos exitosos que el comprobador demuestra inválidos.

 4. Revisar orden estricto y reglas de cortocircuito.

 5. Confirmar que las garantías externas requieren vigencia y no se confunden con propiedades del
 valor.

 Siguiente documento
 La especificación de tipos y contratos desarrollará reglas formales de compatibilidad, predicados
 admitidos, comprobaciones estáticas y dinámicas, conservación entre funciones y diagnósticos.
 Mantendrá las decisiones abiertas del modelo numérico hasta su documento específico.

 La serie se detiene después de este PDF para revisar el resultado. No se crean los documentos
 restantes hasta recibir la autorización del usuario o sus correcciones.




Documento 01 · Propuesta 0.1 · 14 de octubre de 2026                                                 10
````

