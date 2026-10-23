# 04 · Sintaxis y gramática inicial

Estado: propuesta 0.1, anterior al nombre Traza.

Transcripción textual íntegra del PDF `04-sintaxis-gramatica-inicial.pdf`. Se conservan los saltos de línea y la disposición de tablas y código en bloques de texto para evitar una conversión Markdown que cambie su significado. Pendiente de normalización editorial y cotejo con el PDF original; no se incorpora aquí el archivo PDF binario.

Para el índice vigente de la serie y sus cambios, consultar [el índice documental](../readme.md).

## Página 1

````text
 Sintaxis y gramática inicial
 Nuevo lenguaje funcional · Documento 04 de 08 · Propuesta 0.1

 20 de octubre de 2026

 Propósito y alcance
 Definir una notación concreta para el subconjunto inicial: funciones, tipos generales, contratos,
 expresiones, variantes y manejo explícito de errores. Las reglas G01 a G32 y la gramática EBNF
 permiten preparar el lexer, el parser y los casos de aceptación sintáctica.

 Se mantienen evaluación estricta, valores inmutables y Number decimal exacto. Esta propuesta fija
 cómo escribir esas reglas; no convierte una expresión bien formada en un programa correcto.
 Tipos, efectos, exhaustividad y obligaciones de contratos se comprueban después de analizar la
 sintaxis.

 Base documental

   Documento                             Versión                         Uso

   Semántica mínima                      Propuesta 0.1                   Evaluación funciones y control

   Tipos y contratos                     Propuesta 0.1                   Tipos generales y evidencia

   Modelo numérico                       Propuesta 0.1                   Literales operaciones y fallos

   Contexto y Project Brief              1.1 y 1.0                       Objetivo alcance y decisiones


 Los detalles nuevos de esta notación son propuestas para revisión. No constituyen una
 implementación completa ni una demostración de originalidad. No se crean tipos nominales
 numéricos por moneda, tasa o escala.

 Decisiones principales
 Los contratos se escriben where { predicado }; las llaves delimitan la condición y evitan confundir
 sus comparaciones con el cierre de tipos genéricos. Las llamadas genéricas explícitas usan ::<...>
 para distinguirlas de comparaciones. Las variantes usan nombres calificados como Result::Ok(x). El
 operador ? propaga únicamente un error declarado.

 No se usan rangos de comparación encadenados: 0 <= value <= 100 se escribe 0 <= value and
 value <= 100. Los ejemplos conceptuales de documentos previos se interpretan con esta notación
 concreta para el prototipo; no se modifican sus reglas semánticas.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                      1
````

## Página 2

````text
 1 Texto fuente y reglas léxicas
 G01 Codificación y posiciones
 El fuente utiliza UTF-8 válido. Se admiten finales de línea LF o CRLF; las posiciones diagnósticas
 identifican archivo, línea y columna. La unidad de columna y desplazamiento binario se fijará en la
 arquitectura y deberá mantenerse consistente.

 G02 Identificadores y palabras reservadas
 Un identificador usa letras ASCII, dígitos y guion bajo; no comienza con dígito. El nombre formado
 solo por _ se reserva como patrón comodín. Hay distinción entre mayúsculas y minúsculas. No se
 normalizan nombres para hacerlos equivalentes.

 Son reservadas fn, pub, type, variant, record, let, if, else, match, where, value, check, and, or, not,
 true y false. value solo designa el contenido al que se aplica el contrato o la comprobación.
 Number, Boolean, Text, Bytes, List, Option, Result, Error y Rounding son nombres predefinidos que
 no pueden redefinirse.

 G03 Espacios comentarios y tokens
 Espacios, tabulaciones y saltos separan tokens, pero no instrucciones. // inicia comentario hasta el
 fin de línea. No hay comentarios de bloque en esta versión. Se reconoce el token válido más largo:
 <= precede a <, != a ! y ::< a ::.

 G04 Números
 NUMBER es una secuencia de dígitos, una parte decimal opcional y un exponente decimal opcional.
 Si aparece punto exige dígitos a ambos lados; si aparece e o E exige exponente entero con signo
 opcional. El signo inicial pertenece al operador unario del fuente, no al token.

 NUMBER = DIGIT+ ("." DIGIT+)? ([eE] [+-]? DIGIT+)?
 IDENT = [A-Za-z_] [A-Za-z0-9_]*    excepto "_"

 G05 Texto y bytes
 STRING usa comillas dobles. Permite texto Unicode escalar y escapes de comilla, barra inversa, n,
 r, t y u{HEX}. El último contiene de uno a seis dígitos hexadecimales y debe representar un escalar
 válido, no un sustituto UTF-16. No se permiten saltos de línea literales dentro de STRING.

 BYTES usa b seguido inmediatamente de comillas y pares hexadecimales: b"00FF". No admite
 escapes ni separadores; b"" es vacío. Estos bytes no son una codificación textual implícita.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                       2
````

## Página 3

````text
 2 Declaraciones ámbitos y bloques
 G06 Unidad de programa
 Una unidad contiene declaraciones de funciones y alias transparentes de tipos. pub marca una
 interfaz pública. El prototipo comprueba todas las unidades como un programa completo; no
 incluye importaciones, módulos compilados por separado ni carga dinámica.

 G07 Resolución de nombres
 Las declaraciones superiores se registran antes de comprobar cuerpos; esto permite llamadas
 adelantadas y recursión con firma. No se permite duplicar nombres en el mismo ámbito. Un ámbito
 anidado puede ocultar vinculaciones exteriores, excepto palabras reservadas y nombres
 predefinidos.

 G08 Funciones y clausuras
 Las funciones declaran parámetros y tipo de retorno. Una función anónima usa la misma forma sin
 nombre ni pub y captura el entorno léxico. Sus parámetros y retorno también se anotan
 inicialmente; no se introducen dos notaciones distintas para lambdas.

 pub fn identity<T>(x: T) -> T { x }
 let twice = fn(x: Number) -> Number { x * 2 };

 La segunda línea ilustra una vinculación dentro de un bloque, no una declaración global admitida.
 Los nombres de parámetros son únicos; value no puede utilizarse como parámetro.

 G09 Bloques y vinculaciones
 Un bloque contiene cero o más vinculaciones let, seguidas por una expresión final obligatoria. Cada
 let termina con punto y coma; la expresión final no. No existe bloque vacío ni valor Unit implícito en
 este subconjunto.

 fn total(x: Number, y: Number) -> Number {
   let subtotal = x + y;
   let result: Number = subtotal * 2;
   result
 }

 let vincula un nombre inmutable y puede incluir anotación. No permite reasignación ni patrones
 refutables. Las expresiones intermedias con efectos deben vincular su resultado y tratar sus
 errores. La política de uso de Result se comprueba estáticamente; un punto y coma no descarta un
 fallo.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                      3
````

## Página 4

````text
 3 Tipos contratos y efectos
 G10 Tipos generales y genéricos
 Un tipo es un nombre con argumentos opcionales, un registro cerrado, una variante estructural o
 un tipo de función. List<Number> y Result<Number, Error> son construcciones generales. Los
 parámetros genéricos se declaran como <T> en funciones o alias; la instancia explícita de una
 llamada se escribe identity::<Number>(x).

 G11 Registros y alias
 Los tipos de registros usan campos entre llaves: {total: Number, valid: Boolean}. Los valores
 requieren record {total: 10, valid: true}, evitando confundir un registro con un bloque. Los campos
 son únicos y se accede con punto.

 type declara un alias transparente y termina con punto y coma. No agrega identidad nominal,
 validaciones ni disposición física. No se admiten ciclos de alias en esta versión. Un nombre de alias
 no puede utilizarse para omitir un contrato.

 G12 Variantes y funciones como tipos
 variant {First(T), Second(T)} describe etiquetas con una carga opcional. Un alias permite
 calificarlas, como Choice::First(x). Es una estructura general; no incorpora reglas de negocio a la
 representación numérica. Las etiquetas deben ser únicas.

 Un tipo de función se delimita por paréntesis completos: (fn(x: Number) -> Number). Los nombres
 permiten expresar relaciones con parámetros. Los paréntesis separan sus efectos de los de una
 función que la devuelve.

 G13 Contratos delimitados
 Number where { value >= 0 }
 Result<Number where { is_quantized(value, 2) }, Error>

 where aplica la condición al tipo inmediatamente anterior. Para restringir el éxito, se escribe dentro
 de Result, no después del contenedor. El parser acepta una expresión entre las llaves; el
 comprobador aplica el subconjunto de predicados de T13 y N04. Sintaxis válida no autoriza
 llamadas arbitrarias en contratos.

 G14 Efectos
 La firma puede terminar con !{ReadFile, WriteFile}. Sin cláusula, o con !{}, la función es pura. Las
 etiquetas se validan contra el vocabulario que implemente el runtime; escribir una etiqueta no
 concede acceso a un recurso. Para funciones devueltas, la cláusula interna queda dentro del tipo
 parentetizado.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                      4
````

## Página 5

````text
 4 Expresiones y precedencia
 G15 Orden de precedencia

   Nivel de mayor a menor                Formas                                 Asociación

   1                                     llamada campo instancia genérica y ?   Sufijos de izquierda a derecha

   2                                     + - not unarios                        Derecha

   3                                     */                                     Izquierda

   4                                     + - binarios                           Izquierda

   5                                     == != < <= > >=                        Una sola comparación

   6                                     and                                    Izquierda y cortocircuito

   7                                     or                                     Izquierda y cortocircuito


 Los paréntesis agrupan expresiones. if, match, check y funciones anónimas son expresiones
 completas; para utilizarlas como operando o aplicarle sufijos, se parentetizan. No hay
 multiplicación implícita, asignación como expresión, incremento ni operador de potencia.

 G16 Aritmética y división
 Los operadores +, - y * siguen el modelo exacto de Number. / equivale a divide_exact y devuelve
 Result. Así, a / b * c se analiza como (a / b) * c, pero se rechaza por tipos; dentro de una función
 Result compatible se escribe (a / b)? * c.

 No se aplica elevación implícita de operaciones sobre Result. Las funciones quantize y divide_round
 conservan parámetros de escala y modo explícitos. La sintaxis inicial admite solo argumentos
 posicionales.

 G17 Condicionales
 if (condición) { expresión } else { expresión } exige Boolean y ambas ramas. Solo se evalúa la
 elegida. Los bloques pueden incluir let. La compatibilidad de resultados y efectos de ramas
 corresponde al comprobador.

 G18 Llamadas y estructuras
 Las llamadas y sus argumentos se evalúan según S03. Se admiten listas [1, 2, 3], listas vacías con
 tipo inferible, registros explícitos y acceso a campos. No se introduce indexación parcial mediante
 corchetes ni extracción insegura; las operaciones de colección usan contratos y Option cuando
 corresponda.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                             5
````

## Página 6

````text
 5 Patrones comprobación y propagación
 G19 Selección de variantes
 match (expresión) contiene brazos patrón => bloque separados por comas. Puede tener una coma
 final. Se evalúa el sujeto una vez. Los patrones iniciales admiten nombres, _, literales y
 constructores calificados con una carga opcional.

 match (result) {
   Result::Ok(x) => { x },
   Result::Err(e) => { 0 }
 }

 Este ejemplo elige explícitamente recuperar un error con cero; no define una recuperación
 automática del lenguaje. Los patrones de registro, listas y guardas se difieren para limitar el parser
 y el análisis inicial.

 G20 Exhaustividad y superposición
 El comprobador exige exhaustividad y rechaza patrones superpuestos o brazos inaccesibles. Un
 comodín o nombre capturador final actúa como caso por defecto y recibe solo alternativas
 restantes; es la excepción explícita al análisis de disyunción. No puede preceder a otros brazos.
 Para variantes cerradas se favorecen brazos explícitos, como Ok y Err. El orden no resuelve
 superposiciones entre los demás patrones.

 G21 Propagación explícita
 El sufijo ? exige Result<T, E>. Si obtiene éxito, produce T con sus garantías. Si obtiene error,
 termina inmediatamente la función contenedora devolviendo ese error mediante un Result
 compatible. No introduce una excepción, no atraviesa otra clausura y no opera sobre Option.

 Si la función no declara un Result compatible, se rechaza ?. Un Err sin ? sigue siendo un valor
 ordinario; no evita evaluar por sí mismo los argumentos siguientes de una llamada.

 G22 Comprobación de condiciones
 check (expresión) where { predicado } evalúa una vez el candidato. value dentro del predicado se
 refiere a ese candidato. La operación produce Result con el valor validado o
 Error::ContractViolation. Puede omitirse el control dinámico cuando su condición ya esté
 demostrada. La validación explícita de entradas desconocidas utiliza esta forma antes de una
 llamada restringida.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                      6
````

## Página 7

````text
 6 Gramática de declaraciones y tipos
 G23 Convenciones EBNF
 Las comillas delimitan terminales; [ ] indica opcional, { } repetición y | alternativa. IDENT, NUMBER,
 STRING y BYTES son tokens definidos por G01 a G05. EOF indica fin de entrada. Las listas no
 admiten coma final salvo donde se indique. Los espacios no forman parte de los terminales
 compuestos ::<, :: y ->.

 program      = { declaration }, EOF ;
 declaration = ["pub"], (function_decl | alias_decl) ;
 function_decl = "fn", IDENT, [type_params],
                 "(", [params], ")", "->", type,
                 [effects], block ;
 alias_decl   = "type", IDENT, [type_params], "=", type, ";" ;
 type_params = "<", IDENT, {",", IDENT}, ">" ;
 params       = param, {",", param} ;
 param        = IDENT, ":", type ;
 effects      = "!", "{", [names], "}" ;
 names        = IDENT, {",", IDENT} ;
 type         = type_atom, ["where", "{", expression, "}"] ;
 type_atom    = IDENT, ["<", types, ">"]
              | "{", [type_fields], "}"
              | "variant", "{", variants, "}"
              | "(", "fn", "(", [params], ")", "->",
                type, [effects], ")" ;
 types        = type, {",", type} ;
 type_fields = type_field, {",", type_field} ;
 type_field   = IDENT, ":", type ;
 variants     = variant_item, {",", variant_item} ;
 variant_item = IDENT, ["(", type, ")"] ;
 block        = "{", {let_stmt}, expression, "}" ;
 let_stmt     = "let", IDENT, [":", type],
                "=", expression, ";" ;

 El tipo de un registro vacío se escribe {} y su valor record {}. Una variante debe tener al menos
 una alternativa. No hay declaraciones de variables globales. Las funciones y los alias pueden
 ordenarse libremente; los ciclos de alias se rechazan después del análisis sintáctico.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                      7
````

## Página 8

````text
 7 Gramática de expresiones y patrones
 expression   = if_expr | match_expr | check_expr
              | lambda | or_expr ;
 if_expr      = "if", "(", expression, ")", block,
                "else", block ;
 match_expr   = "match", "(", expression, ")", "{",
                arm, {",", arm}, [","], "}" ;
 arm          = pattern, "=>", block ;
 check_expr   = "check", "(", expression, ")",
                "where", "{", expression, "}" ;
 lambda       = "fn", "(", [params], ")", "->", type,
                [effects], block ;
 or_expr      = and_expr, {"or", and_expr} ;
 and_expr     = comparison, {"and", comparison} ;
 comparison   = addition, [cmp_op, addition] ;
 cmp_op       = "==" | "!=" | "<" | "<=" | ">" | ">=" ;
 addition     = product, {("+" | "-"), product} ;
 product      = unary, {("*" | "/"), unary} ;
 unary        = ("+" | "-" | "not"), unary | postfix ;
 postfix      = primary, {suffix} ;
 suffix       = "(", [arguments], ")" | ".", IDENT
              | "::<", types, ">" | "?" ;
 arguments    = expression, {",", expression} ;
 primary      = NUMBER | STRING | BYTES | "true" | "false"
              | "value" | path | "(", expression, ")"
              | "[", [arguments], "]"
              | "record", "{", [value_fields], "}" ;
 path         = IDENT, ["::", IDENT] ;
 value_fields = value_field, {",", value_field} ;
 value_field = IDENT, ":", expression ;
 pattern      = "_" | IDENT | NUMBER | "-", NUMBER
              | STRING | "true" | "false"
              | IDENT, "::", IDENT, ["(", pattern, ")"] ;

 G24 Separación de análisis y significado
 La gramática admite primary value, pero su uso fuera del alcance de un contrato es error estático.
 Admite llamadas en condiciones que el comprobador puede rechazar. También admite dos ?
 sucesivos; solo serán válidos si los tipos y la función contenedora permiten ambas propagaciones.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                  8
````

## Página 9

````text
 8 Restricciones adicionales y biblioteca inicial
 G25 Resolución de ambigüedades
 La distinción type y expression está determinada por el contexto. Las llaves de where cierran el
 predicado antes del > del genérico. El token ::< inicia una instancia explícita y nunca se interpreta
 como :: seguido de comparación. Los constructores exigen alias o tipo predefinido y etiqueta, como
 Result::Ok.

 Un IDENT solo en un patrón captura un valor; no busca una constante. Los literales negativos en
 patrones usan - seguido de NUMBER. Para evitar precedencia confusa, not (x < 5) es la forma
 recomendada; not x < 5 se analiza como (not x) < 5 y se rechaza si x es Number.

 G26 Predicados admitidos
 El comprobador limita predicados a constantes booleanas, conectores, comparaciones simples de
 valores o campos conocidos, length para Bytes o colecciones, is_integer e is_quantized con sus
 precondiciones satisfechas. Las comparaciones numéricas siguen Number finito y exacto.

 No se permiten operaciones con efectos, recursión, lambdas, check anidado ni propagación ?
 dentro de un predicado. Tampoco llamadas a funciones arbitrarias aunque sean puras. La longitud
 de Text sigue sin habilitarse hasta fijar su unidad en la biblioteca; no se infiere como bytes.

 G27 Construcciones predefinidas

   Nombre                                          Alternativas o función

   Result<T, E>                                    Result::Ok(T) y Result::Err(E)

   Option<T>                                       Option::Some(T) y Option::None

                                                   Exact HalfEven HalfAwayFromZero TowardZero TowardPositive
   Rounding
                                                   TowardNegative

   Error                                           Códigos generales de N22 más InvalidInput y ContractViolation

   Operaciones numéricas                           Nombres y contratos del documento 03


 Las políticas se califican, por ejemplo Rounding::HalfEven. Los códigos simples de Error no tienen
 carga; ContractViolation lleva un registro técnico con condition_id, location y boundary, todos Text.
 El runtime conserva estos datos sin incluir necesariamente el valor rechazado. Las firmas de
 constructores se verifican; escribir una etiqueta desconocida es error estático.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                               9
````

## Página 10

````text
 9 Ejemplos de contratos y composición
 G28 Validación y reutilización
 pub fn validate_percentage(x: Number)
   -> Result<Number where {
        value >= 0 and value <= 100
      }, Error> {
   if (x >= 0 and x <= 100) {
     Result::Ok(x)
   } else {
     Result::Err(Error::InvalidInput)
   }
 }

 fn consume(x: Number where { value >= 0 }) -> Number {
   x + x
 }

 pub fn pipeline(x: Number) -> Result<Number, Error> {
   let validated = validate_percentage(x)?;
   Result::Ok(consume(validated))
 }

 La rama exitosa establece el rango; ? conserva la garantía del contenido. consume recibe una
 condición más débil y no necesita otra validación. El ejemplo se comprueba semánticamente
 conforme a los documentos anteriores; el parser solo verifica su estructura.

 Validación adicional cuando no alcanza la evidencia
 pub fn below_fifty(x: Number)
   -> Result<Number where { value < 50 }, Error> {
   let validated = (check (x) where { value < 50 })?;
   Result::Ok(validated)
 }

 check es una expresión completa: para propagar su resultado se parentetiza antes del sufijo ?. La
 variante sin esos paréntesis es un error sintáctico; el parser no la reinterpreta silenciosamente.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                  10
````

## Página 11

````text
 10 Ejemplos numéricos estructuras y funciones
 G29 Cuantización explícita
 pub fn commission(amount: Number, rate: Number)
   -> Result<Number where {
        is_quantized(value, 2)
      }, Error> {
   let raw = amount * rate;
   let rounded = quantize(raw, 2, Rounding::HalfEven)?;
   Result::Ok(rounded)
 }

 El modo de redondeo está a la vista. El éxito de quantize establece is_quantized, que se conserva
 al retornar. La función no impone moneda ni rango de negocio. Estos deben declararse mediante
 datos o contratos si el caso de uso los requiere.

 G30 Alias y funciones como valores
 type Choice<T> = variant { First(T), Second(T) };
 type Pair = { left: Number, right: Number };

 fn choose() -> Choice<Number> {
   Choice::First(2)
 }

 fn add_pair(x: Pair) -> Number { x.left + x.right }

 pub fn demo() -> Number {
   let pair: Pair = record { left: 2, right: 3 };
   let twice: (fn(x: Number) -> Number) =
     fn(x: Number) -> Number { x * 2 };
   twice(add_pair(pair))
 }

 Choice y Pair son alias transparentes de estructuras generales, no tipos nominales ni
 representaciones especializadas. Las instancias de constructores pueden resolverse mediante el
 contexto de retorno. Una instancia explícita de identity puede escribirse identity::<Number>(2).




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                 11
````

## Página 12

````text
 11 Diagnósticos y escenarios sintácticos
 G31 Categorías de diagnóstico

   Código     Capa                                          Situación

   SG01       Léxica                                        UTF-8 literal o escape inválido

   SG02       Sintáctica                                    Token o delimitador inesperado

   SG03       Sintáctica                                    Falta expresión final o punto y coma

   SG04       Sintáctica                                    Comparación encadenada

   SG05       Nombres                                       Identificador duplicado o reservado

   SG06       Tipos                                         Constructor llamada o ? incompatibles

   SG07       Contratos                                     Predicado fuera del subconjunto

   SG08       Patrones                                      Falta de cobertura o superposición



 Orden de las comprobaciones
 La fase léxica produce tokens o errores de codificación y literales. El parser produce estructura o
 diagnósticos de forma. La resolución de nombres comprueba ámbitos y declaraciones. El
 comprobador de tipos, efectos y contratos determina si la estructura puede ejecutarse. Que un
 ejemplo llegue a esta última fase no significa que haya sido aceptado.

 La recuperación de errores no crea programas válidos: puede continuar para mostrar otros
 diagnósticos, pero no ejecutar un árbol reconstruido con información inventada. Los ejemplos
 rechazados deben indicar la fase y el token o requisito correspondiente.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                   12
````

## Página 13

````text
 Casos que deberá contener la suite

   Caso     Entrada o situación                                     Resultado

   GR01     Función identity y llamada ::<Number>                   Sintaxis aceptada

   GR02     Contrato dentro de Result con > numérico                Sintaxis aceptada

   GR03     Función commission de G29                               Sintaxis aceptada

   GR04     record {} y tipo {}                                     Sintaxis aceptada

   GR05     0 <= x <= 100                                           SG04

   GR06     Función con bloque vacío                                SG03

   GR07     Punto y coma después de expresión final                 SG03

   GR08     Comparación x < y y llamada f::<T>(x)                   Árboles diferentes y únicos

   GR09     1/8*2                                                   Sintaxis válida; error de tipos

   GR10     (1 / 8)? * 2 en función Number                          Sintaxis válida; SG06

   GR11     Constructor desconocido                                 Sintaxis válida; SG06

   GR12     value fuera de contrato                                 Sintaxis válida; error de alcance

   GR13     Predicado llama a función arbitraria                    Sintaxis válida; SG07

   GR14     match sin Err y sin cobertura equivalente               Sintaxis válida; SG08


 Estos casos distinguen parseo y comprobación. El documento 05 los convertirá en pruebas de
 conformidad con resultados completos. La revisión estructural de preparación aceptó 12
 programas, rechazó 8 formas inválidas y comprobó 5 árboles de precedencia mediante un
 analizador de apoyo. No verificó tipos ni ejecutó el lenguaje, y no constituye una prueba formal de
 ausencia de ambigüedad de toda la gramática.




Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                    13
````

## Página 14

````text
 12 Decisiones y trazabilidad
 G32 Alcance de la notación propuesta

   Elección                              Motivo                             Base

   Contratos where con llaves            Delimitar comparación y tipo       S11 T09

   Instancia explícita ::<...>           Separar genéricos de comparación   T06

   record para valores de registro       Separar registro y bloque          T02

                                         Fallos explícitos y garantías
   ? solo sobre Result                                                      S18 T24
                                         conservadas

   Tipos de función parentetizados       Evitar ambigüedad de efectos       T20 T28

                                         Nombres legibles sin identidad
   Alias transparentes                                                      T01 T02
                                         nominal

   Bloque con expresión final
                                         Resultado y secuencia explícitos   S07
   obligatoria



 Precisiones frente a ejemplos anteriores
 Se concretan and or not y true false en minúsculas, constructores calificados y argumentos
 posicionales. Las restricciones ilustradas sin llaves en documentos previos se escriben ahora where
 { ... }. Las comparaciones encadenadas conceptuales se expanden con and. No se altera el modelo
 numérico ni la política de contratos por estas decisiones de escritura.

 Pendientes de arquitectura y conformidad
 La arquitectura elegirá implementación del lexer y parser, posiciones exactas, mensajes y límites
 de fuente. También fijará vocabulario implementado de efectos y gestión de recursos. La suite
 deberá verificar árboles de precedencia, formas válidas e inválidas y recuperación diagnóstica sin
 aceptar programas incorrectos.

 No hay módulos separados, macros, argumentos nombrados, sobrecarga definida por el usuario,
 indexación parcial, asignación mutable, guardas de patrones ni inferencia de cualquier predicado.
 Ampliar la gramática exigirá actualizar sus reglas y pruebas; no se hereda sintaxis del lenguaje
 anfitrión.

 Revisión y siguiente documento
 La base son los documentos 01 a 03 propuesta 0.1, el contexto 1.1 y el Brief 1.0. Esta notación se
 propone para revisión y no demuestra originalidad. Las construcciones transparentes no
 introducen tipos numéricos específicos de negocio.

 El siguiente documento es Casos de conformidad. Integrará escenarios semánticos, contratos,
 números y gramática, diferenciando aceptación sintáctica, rechazo estático y resultado en
 ejecución. La serie se detiene aquí hasta recibir autorización para continuar o correcciones.



Documento 04 · Propuesta 0.1 · 20 de octubre de 2026                                                  14
````

