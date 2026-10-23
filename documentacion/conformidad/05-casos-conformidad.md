# 05 · Casos de conformidad

Estado: propuesta 0.1, anterior al nombre Traza.

Transcripción textual íntegra del PDF `05-casos-conformidad.pdf`. Se conservan los saltos de línea y la disposición de tablas y código en bloques de texto para evitar una conversión Markdown que cambie su significado. Pendiente de normalización editorial y cotejo con el PDF original; no se incorpora aquí el archivo PDF binario.

Para el índice vigente de la serie y sus cambios, consultar [el índice documental](../readme.md).

## Página 1

````text
 Casos de conformidad
 Documento 05 · Propuesta 0.1
 Lenguaje funcional en diseño · 20 de octubre de 2026

 Propósito
 Convertir las decisiones de semántica, tipos, contratos, números y sintaxis en resultados
 observables que permitan aceptar o rechazar una implementación. Este documento especifica
 pruebas; no certifica que exista un compilador conforme.

 Criterio de decisión
 Se mantienen los criterios de los documentos anteriores: tipos generales, garantías comprobables
 en las respuestas, errores explícitos, evaluación predecible y especializaciones justificadas por
 mediciones. La facilidad para escribir un ejemplo no justifica introducir una excepción semántica.

 Referencias internas
 01 Especificación semántica mínima; 02 Especificación de tipos y contratos; 03 Especificación del
 modelo numérico; 04 Sintaxis y gramática inicial. Las denominaciones y versiones corresponden a
 las propuestas 0.1 de esta serie.

 Alcance de esta entrega
 Se definen 40 casos identificados CF01–CF40. Una fila parametrizada constituye un caso; sus
 variantes deben ejecutarse todas. Los casos incluyen programas mínimos, vectores numéricos y
 protocolos para pruebas que dependen del futuro ejecutor.

 Estado real
 Se comprueba la sintaxis de los programas completos incluidos mediante el analizador auxiliar del
 documento 04. Esa comprobación no valida tipos, contratos, efectos ni ejecución. Todos los
 resultados de compilación y ejecución aquí especificados quedan pendientes del prototipo.

 Lectura del documento
 Las páginas siguientes separan el protocolo de evaluación, los programas de contratos, la
 semántica observable, los números, los rechazos y los criterios de entrega. Las palabras «debe» y
 «rechaza» expresan requisitos de la propuesta, no resultados ya obtenidos.




Documento 05 · Propuesta 0.1 · 20 de octubre de 2026                                                  1
````

## Página 2

````text
 1. Protocolo de prueba
 Fases y resultados
 Cada ejecución registra versión de la especificación, revisión del ejecutor, caso, entrada, fase
 alcanzada y resultado. Se distinguen análisis léxico/sintáctico, comprobación estática, ejecución y
 fallo del proceso. Un rechazo temprano correcto impide ejecutar el programa.

   Resultado                                       Evidencia requerida

   Aceptación estática                             Programa aceptado sin cambiar su firma pública.

   Rechazo estático                                Familia del diagnóstico y fragmento responsable.

   Valor                                           Variante y contenido estructural; igualdad numérica exacta.

   Error del lenguaje                              Result::Err y código del error esperado.

   Fallo del proceso                               Estado externo; nunca convertirlo en un Err inventado.



 Oráculos
 Los resultados numéricos se comparan como decimales exactos, usando coeficiente entero y
 exponente o una referencia racional independiente. Un float binario no sirve como oráculo. Los
 textos se comparan por contenido, sin depender del formato que use la consola para mostrar las
 variantes.

 ContractViolation exige los campos condition_id, location y boundary. Se comprueban su presencia
 y consistencia con la condición y frontera afectadas; no se fijan rutas ni números de línea que aún
 dependen de la arquitectura.

 Independencia de la implementación
 Los programas reciben los valores de prueba como argumentos del arnés, sin sustituirlos por
 constantes en sus cuerpos. La instrumentación puede observar entradas a funciones y decisiones
 del comprobador; no puede modificar orden, valores ni efectos.

 Un tiempo límite detecta una ejecución inconclusa. No demuestra divergencia. El agotamiento de
 memoria se informa como fallo del proceso y no se confunde con InexactResult o ContractViolation.

 Diagnósticos
 Se exige la familia semántica del documento 02 o la categoría sintáctica del documento 04. El
 texto literal, la cantidad de diagnósticos secundarios y sus posiciones exactas no son contratos de
 compatibilidad en esta versión.




Documento 05 · Propuesta 0.1 · 20 de octubre de 2026                                                             2
````

## Página 3

````text
 2. Respuestas con garantías
 Programa A · Frontera automática
 pub fn bounded(x: Number)
   -> Result<Number where {value >= 0 and value <= 100}, Error> {
    Result::Ok(x)
 }

 CF01: invocar bounded(50). Se acepta y devuelve Ok(50). La propiedad no se demuestra para
 cualquier x; el retorno exitoso requiere comprobación dinámica.

 CF02: invocar bounded(-1) y bounded(101). Ambas ejecuciones devuelven Err(ContractViolation),
 con los tres campos de diagnóstico. Ningún valor inválido puede escapar como Ok.

 Programa B · Composición sin revalidación manual
 fn double(x: Number where {value >= 0}) -> Number {
   x + x
 }
 pub fn pipeline(x: Number) -> Result<Number, Error> {
   let validated = bounded(x)?;
   Result::Ok(double(validated))
 }

 Este programa se compila junto con A. CF03: pipeline(25) produce Ok(50); el comprobador
 reconoce que el intervalo 0..100 implica no negatividad. CF04: pipeline(101) propaga
 ContractViolation; double no llega a ejecutarse.

 No se impone un número de instrucciones máquina. La evidencia exigida es que el compilador
 conserva la prueba que permite consumir validated sin pedir una validación escrita por el
 programador.

 Programa C · Garantía más fuerte explícita
 pub fn below_fifty(x: Number)
   -> Result<Number where {value < 50}, Error> {
    let accepted = (check (x) where {value < 50})?;
    Result::Ok(accepted)
 }

 CF05: entradas 49 y 50 producen respectivamente Ok(49) y Err(ContractViolation). El segundo
 resultado es una validación fallida prevista, no una excepción.




Documento 05 · Propuesta 0.1 · 20 de octubre de 2026                                             3
````

## Página 4

````text
 3. Rechazos y conservación de pruebas
 Cada fragmento de esta página es un programa independiente, salvo donde se indica una
 dependencia. Su sintaxis es válida; el comprobador debe rechazar los casos CF06–CF09 por
 razones diferentes.

 CF06 · Retorno imposible conocido
 pub fn impossible()
   -> Result<Number where {value <= 100}, Error> {
    Result::Ok(101)
 }

 Esperado: rechazo estático D05. No se permite trasladar a ejecución una violación demostrada en
 un retorno alcanzable.

 CF07 · Retorno desconocido sin canal de error
 pub fn unchecked(x: Number) -> Number where {value >= 0} {
   x
 }

 Esperado: D06. El compilador no añade Result ni una excepción oculta a la firma.

 CF08 · Precondición de entrada sin prueba
 fn consume(x: Number where {value >= 0}) -> Number { x }
 pub fn caller(x: Number) -> Number { consume(x) }

 Esperado: D04. No se inserta una validación de entrada que pueda fallar sin estar representada en
 la función llamadora.

 CF09 · Una transformación pierde la garantía
 fn consume(x: Number where {value >= 0}) -> Number { x }
 pub fn transform(x: Number where {value >= 0}) -> Number {
   consume(x - 1)
 }

 Esperado: D04. Con x=0, x-1 es negativo; el refinamiento de x no se transfiere automáticamente a
 expresiones nuevas.

 CF10 · Error fuera del refinamiento de éxito
 pub fn failed()
   -> Result<Number where {value >= 0}, Error> {
    Result::Err(Error::InvalidInput)
 }

 Esperado: aceptación y Err(InvalidInput). La condición restringe el contenido de Ok, no el contenido
 de Err.




Documento 05 · Propuesta 0.1 · 20 de octubre de 2026                                                    4
````

## Página 5

````text
 4. Evaluación y control
 Programa D · Orden observable sin efectos nuevos
 fn first() -> Result<Number, Error> {
   Result::Err(Error::InvalidInput)
 }
 fn second() -> Number { 2 }
 fn take(r: Result<Number, Error>, n: Number) -> Number {
   match (r) {
     Result::Ok(x) => { n },
     Result::Err(e) => { n }
   }
 }
 pub fn ordinary_error() -> Number { take(first(), second()) }

 CF11: valor 2 y entradas observadas en orden first, second, take. Un Err ordinario no detiene la
 evaluación de argumentos. El arnés observa entradas a funciones sin añadir operaciones al
 lenguaje.

 Programa E · Cortocircuito explícito
 pub fn propagated() -> Result<Number, Error> {
   let n = first()?;
   Result::Ok(second() + n)
 }

 Se compila con first y second del programa D. CF12: Err(InvalidInput); second no se ejecuta. La
 salida anticipada corresponde a la función más cercana que contiene ?.

 Programa F · Rama no seleccionada
 fn forever() -> Number { forever() }
 pub fn selected() -> Number {
   if (true) { 7 } else { forever() }
 }

 CF13: selected() termina con 7. La existencia de recursión no obliga a evaluar una rama
 descartada ni a demostrar terminación global.

 Casos adicionales del ejecutor
 CF14: con una sonda del arnés que provoca fallo fatal al evaluar el primer argumento, el segundo
 no se evalúa. Es una prueba del ejecutor, no una función pública nueva. Su mecanismo queda
 pendiente de arquitectura.

 CF15: false and condición y true or condición omiten la condición derecha; usar forever() == 0
 como condición. Se espera false y true respectivamente. No usar un tiempo límite como única
 evidencia: registrar que forever no se invocó.




Documento 05 · Propuesta 0.1 · 20 de octubre de 2026                                                5
````

## Página 6

````text
 5. Aritmética exacta y redondeo
 Los CF16–CF29 son vectores de ejecución. Cada operación se coloca como expresión final de una
 función pública con parámetros Number y respuesta Number, Boolean o Result según la firma del
 documento 03. El arnés suministra los operandos. Los nombres de API son los de aquella
 propuesta.

   Caso     Operación e inputs                                      Resultado estructural esperado

   CF16     a+b; a=0.1, b=0.2                                       Number 0.3 exacto.

   CF17     a==b; a=1, b=1.00                                       Boolean true.

   CF18     a*b; a=125.50, b=0.015                                  Number 1.8825.

   CF19     divide_exact(1,8)                                       Ok(0.125).

   CF20     divide_exact(1,3)                                       Err(InexactResult).

   CF21     divide_exact(0,0)                                       Err(DivisionByZero).

   CF22     divide_round(1,3,2,HalfEven)                            Ok(0.33).

   CF23     divide_round(-1,3,2,TowardNegative)                     Ok(-0.34).

   CF24     quantize(1.225,2,HalfEven)                              Ok(1.22).

   CF25     quantize(-1.225,2,HalfAwayFromZero)                     Ok(-1.23).

   CF26     quantize(1.225,2,Exact)                                 Err(InexactResult).

   CF27     quantize(1.2,2,Exact)                                   Ok(1.2); no escala adherida.

   CF28     divmod(-7,3)                                            Cociente -2; resto -1.

   CF29     quantize(1.2,-1,HalfEven)                               Err(InvalidScale), API validante.


 En código fuente, los modos se escriben Rounding::HalfEven y análogos; se abrevian en la tabla
 por espacio. divmod se compara por sus componentes según la API, sin imponer aquí nombres de
 campos nuevos.

 Si una interfaz especializada exige una escala refinada no negativa, pasar -1 es rechazo estático.
 CF29 verifica la interfaz validante, cuyo argumento admite un Number sin esa prueba; ambas
 interfaces no deben confundirse.

 Para CF24 y CF25 añadir las variantes ±1.225 con HalfEven y HalfAwayFromZero: magnitudes
 esperadas 1.22 y 1.23, conservando el signo. Esto detecta errores en los empates negativos.




Documento 05 · Propuesta 0.1 · 20 de octubre de 2026                                                    6
````

## Página 7

````text
 6. Representación y fronteras

   Caso     Entrada y operación                                       Resultado esperado

   CF30     parse_number con "1,25" y "NaN"                           Err(InvalidNumericText) en ambos.

   CF31     canonical de 12.30 y -0                                   "123e-1" y "0e0".

   CF32     format_fixed de 1.2, escala 2                             Ok("1.20").

            Conversión decimal 1000, P=5, S=2; entero 128 con signo
   CF33                                                               Err(NotRepresentable) en ambos.
            de 8 bits


 CF32 verifica que el formateador comprueba la escala y la compatibilidad del valor con ella. Añadir
 la variante format_fixed(1.225, 2): debe devolver Err(InexactResult). El formateador no redondea
 por su cuenta.

 Propiedades adicionales obligatorias
 CF34: para valores decimales generados, parsear la serialización canónica reconstruye el mismo
 número; serializarlo de nuevo produce idéntico texto. Incluir cero, negativos, exponentes positivos
 y negativos, y coeficientes mayores que 64 bits. Las semillas y cantidades se registran en cada
 ejecución.

 CF35: quantize aplicado dos veces con igual escala y modo da el mismo valor exitoso. Para Exact,
 preservar también el error de una entrada no cuantizada. Incluir seis modos y escalas 0, 2 y 8;
 evitar cualquier conversión intermedia a float.

 Política de cálculo observable
 CF36: dos importes de 0.005, cuantizados individualmente a escala 2 con HalfEven, suman 0.00.
 Sumar primero y cuantizar después produce 0.01. Ambos algoritmos son válidos cuando se
 solicitan explícitamente; el optimizador no puede sustituir uno por otro.

 Qué no se demuestra con estos casos
 La aritmética exacta no implica memoria ilimitada ni un tiempo constante. Las pruebas funcionales
 no justifican un tipo especializado. Las mediciones futuras deben indicar tamaño de entrada,
 plataforma, optimizaciones, asignaciones y dispersión de tiempos antes de adoptar otra
 representación.




Documento 05 · Propuesta 0.1 · 20 de octubre de 2026                                                      7
````

## Página 8

````text
 7. Sintaxis, tipos y efectos
 CF37 · Rechazos sintácticos parametrizados
 Insertar cada fragmento como cuerpo de fn probe() -> Number. Se espera rechazo del analizador:
 «let x = 1;» sin expresión final; «if (true) { 1 }» sin else; «1 < 2 < 3» por comparación encadenada;
 «record {x: 1,}» por coma final no admitida en registros. Se prueban por separado.

 CF38 · Sintaxis válida con incompatibilidad de tipos
 pub fn invalid_product(a: Number, b: Number) -> Number {
   a / b * 2
 }

 Esperado: análisis sintáctico correcto y rechazo D01, porque / produce Result. La variante «(a / b)?
 * 2» sólo es admisible dentro de una función cuyo retorno sea un Result compatible. No modificar
 precedencia para ocultar la incompatibilidad.

 CF39 · Cobertura y ámbito del operador ?
 pub fn incomplete(x: Option<Number>) -> Number {
   match (x) { Option::Some(n) => { n } }
 }

 Esperado: rechazo D07 por Option::None sin cubrir. Variante independiente: «pub fn bad(x:
 Option<Number>) -> Number { x? }» es sintácticamente válida y se rechaza por tipado: ? no
 opera sobre Option ni puede fabricar un Result de retorno.

 CF40 · Efectos y predicados no autorizados
 Prueba A: declarar en el módulo de soporte una función con efecto ReadFile, e invocarla desde una
 función declarada pura. Esperado: D08. Su firma de soporte debe proceder del futuro catálogo de
 capacidades, no de un nombre supuesto de biblioteca.

 Prueba B: usar una llamada recursiva o una operación con efectos como condición where.
 Esperado: D03, aunque la expresión sea sintácticamente válida. La lista permitida de predicados
 no equivale al conjunto de todas las funciones puras.

 Las pruebas de soporte de CF40 quedan bloqueadas hasta fijar el catálogo y el protocolo de
 módulos. Eso no autoriza al prototipo a aceptar efectos ocultos o predicados arbitrarios.




Documento 05 · Propuesta 0.1 · 20 de octubre de 2026                                                     8
````

## Página 9

````text
 8. Cobertura, límites y aprobación

   Fuente                                Cobertura en esta batería       Límite explícito

                                                                         Fallo fatal instrumentado
   Semántica 01                          CF03–05, CF11–15, CF36
                                                                         pendiente.

                                                                         Subtipado de funciones
   Tipos y contratos 02                  CF01–10, CF38–40
                                                                         requiere ampliación.

                                                                         No agota prioridades de
   Números 03                            CF16–36
                                                                         errores múltiples.

                                                                         No sustituye pruebas
   Gramática 04                          Programas y CF37–39
                                                                         completas del lexer.



 Ampliaciones necesarias antes de declarar conformidad completa
 Agregar sustitución de funciones con precondiciones distintas; ámbito léxico y sombreado;
 secuencias UTF-8 y escapes inválidos; bytes mal formados; precedencias restantes; reglas de
 solapamiento de patrones; prioridades ante varios argumentos numéricos inválidos;
 representaciones externas y esquemas de decodificación cuando se definan. Los antiguos C, TC,
 MN y GR siguen siendo requisitos de referencia: esta batería no los elimina.

 Ejecución por niveles
 Nivel 1: analizar todos los programas válidos y rechazar CF37. Nivel 2: comprobar tipos, contratos,
 efectos y rechazos esperados. Nivel 3: ejecutar valores, errores y orden observable. Nivel 4:
 ejecutar propiedades generativas y comparar con una referencia independiente.

 Un resultado omitido, bloqueado o agotado por tiempo no cuenta como aprobado. No se exige que
 el primer prototipo alcance todos los niveles; se exige declarar su cobertura real. La integración
 continua debe separar conformidad funcional de mediciones de rendimiento.

 Evidencia de esta edición
 Se ha ejecutado la comprobación sintáctica de los programas completos reproducidos, incluyendo
 las dependencias indicadas; los ejemplos destinados al rechazo estático se analizan antes de
 comprobar sus tipos. También se comprueba el rechazo sintáctico parametrizado de CF37. No se
 ha ejecutado ninguno de los 40 casos sobre una implementación del nuevo lenguaje.

 Condición para avanzar
 Este documento queda como propuesta revisable. El siguiente, 06 Arquitectura del prototipo,
 deberá definir el arnés, las fases del compilador, la representación de errores y pruebas, y las
 capacidades necesarias para convertir estos requisitos en pruebas ejecutables. La aprobación de
 esta entrega no implica aprobar anticipadamente esa arquitectura.




Documento 05 · Propuesta 0.1 · 20 de octubre de 2026                                                   9
````

