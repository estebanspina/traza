# 03 · Modelo numérico

Estado: propuesta 0.1, anterior al nombre Traza.

Transcripción textual íntegra del PDF `03-especificacion-modelo-numerico.pdf`. Se conservan los saltos de línea y la disposición de tablas y código en bloques de texto para evitar una conversión Markdown que cambie su significado. Pendiente de normalización editorial y cotejo con el PDF original; no se incorpora aquí el archivo PDF binario.

Para el índice vigente de la serie y sus cambios, consultar [el índice documental](../readme.md).

## Página 1

````text
 Especificación del modelo numérico
 Nuevo lenguaje funcional · Documento 03 de 08 · Propuesta 0.1

 20 de octubre de 2026

 Propósito y decisión central
 Esta propuesta define Number como una categoría general de números decimales finitos y
 exactos, sin precisión fija impuesta por el lenguaje. Suma, resta y multiplicación conservan el
 resultado exacto. Dividir exige un resultado decimal exacto o una operación explícita con escala y
 redondeo. La pérdida de información nunca se introduce como una optimización invisible.

 Se mantiene un único tipo numérico general. Rango, escala y condiciones son contratos o políticas
 de operación, no tipos nominales de negocio. El almacenamiento puede especializarse si preserva
 los resultados y aporta ventajas medibles de ejecución o memoria.

 Esta es una elección de diseño nueva para revisar. La autorización de continuar permite
 concretarla; no demuestra que se haya implementado, medido ni establecido su originalidad. La
 principal renuncia es que no todo cociente racional cabe en Number: 1/3 requiere error explícito o
 redondeo solicitado.

 Base y alcance

   Documento                             Versión                        Relación

   Contexto del lenguaje                 1.1                            Tipos generales y exactitud

   Project Brief                         1.0                            Alcance y evidencia de costos

   Semántica mínima                      Propuesta 0.1                  Reglas S05 S12 S15 S20 S23

   Tipos y contratos                     Propuesta 0.1                  Reglas T09 a T26


 Las reglas N01 a N32 cierran las operaciones numéricas del subconjunto inicial. La gramática de
 literales y llamadas se precisará en el documento 04. El runtime y los límites de ejecución se
 desarrollarán en el documento 06. Los ejemplos usan punto decimal y nombres conceptuales.

 Qué queda fuera de esta versión
 No se incorporan flotantes aproximados, NaN, infinitos, aritmética modular, saturación,
 trigonometría, potencias no enteras ni contextos globales de redondeo. Podrán estudiarse después
 como capacidades explícitas, con contratos propios y justificación. No quedan habilitados por
 existir soporte de hardware.




Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                    1
````

## Página 2

````text
 1 Dominio lógico y literales
 N01 Valor de Number
 Todo Number representa un valor c multiplicado por una potencia entera de 10. c es un entero con
 signo y la potencia puede ser positiva, cero o negativa. Esta descripción lógica incluye enteros y
 decimales terminantes; no incluye todos los números racionales ni los reales.

 Por ejemplo, 12.3 puede describirse con coeficiente 123 y exponente -1. 1000 puede describirse
 con coeficiente 1 y exponente 3. No hay límite semántico fijo de dígitos o exponente; toda
 ejecución está limitada por sus recursos físicos.

 N02 Igualdad y normalización
 Se propone una forma lógica canónica: coeficiente no divisible por 10 para valores no nulos; cero
 con coeficiente 0 y exponente 0. Así, 1, 1.0 y 1.00 son el mismo valor. No existe cero negativo
 observable en este subconjunto.

 La implementación no tiene que materializar esa forma a cada paso, pero igualdad, comparación y
 serialización canónica deben comportarse como si la respetaran. La escala escrita no pertenece al
 valor: para presentar 1.20 se solicita un formato de dos decimales.

 N03 Literales exactos
 Un literal decimal se interpreta directamente en base 10, sin pasar por flotante binario. Su
 exponente decimal, cuando la gramática lo admita, tiene significado exacto. La coma de una
 configuración regional no cambia el significado del código fuente.

 Una forma literal mal escrita es un error del programa. Un texto recibido durante la ejecución se
 analiza mediante una conversión que devuelve Result. Los límites de tamaño de fuente o de
 entrada deben declararse como políticas de la herramienta, sin truncar el valor.

 N04 Finitud y propiedades generales
 Todos los Number de esta versión son finitos. Number permite inferir esa propiedad en este
 subconjunto, precisando la incertidumbre que los documentos anteriores dejaban abierta. No
 permite inferir signo, rango, integridad ni escala máxima.

 Se definen dos predicados técnicos adicionales para los contratos: is_integer(x), que comprueba si
 x es entero, e is_quantized(x, s), que comprueba si x es múltiplo exacto de 10 elevado a -s. s debe
 ser un entero no negativo. Son operaciones incorporadas puras y terminantes sobre valores
 válidos; amplían expresamente el catálogo inicial de T13.




Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                   2
````

## Página 3

````text
 2 Operaciones exactas y comparación
 N05 Suma resta y negación
 Suma, resta y negación producen el valor matemático exacto en Number. No redondean ni
 recortan dígitos. La suma alinea exponentes según sea necesario; esa operación lógica no impone
 una estrategia de almacenamiento ni un costo constante.

 N06 Multiplicación y precisión intermedia
 Multiplicar combina coeficientes y exponentes sin redondeo intermedio. No hay un contexto de
 precisión global que cambie el resultado dentro de una función. Todo resultado intermedio
 mantiene su valor exacto salvo que el programa invoque expresamente una operación de
 redondeo.

 N07 Orden e igualdad
 La igualdad es numérica y el orden es total: para a y b, exactamente una de las relaciones a < b, a
 = b o a > b es verdadera. Las comparaciones devuelven Boolean y no requieren epsilon ni
 tolerancia implícita. Valores con exponentes o escalas escritas diferentes pueden ser iguales.

 Un rango se compara con sus límites exactos. El comprobador y el runtime deben utilizar la misma
 semántica. La igualdad estructural de números dentro de registros sigue esta igualdad, no el texto
 ni los bytes originales.

 N08 Operaciones incorporadas y firmas

   Operación conceptual                  Resultado                      Comportamiento

   add subtract multiply                 Number                         Exacto

   negate abs                            Number                         Exacto

   compare                               Orden de tres alternativas     Menor igual o mayor

   equals y comparaciones                Boolean                        Sin aproximación

                                                                        Seleccionar un operando por
   min max                               Number
                                                                        valor

   divide_exact                          Result<Number, Error>          Cociente exacto o error

   divide_round                          Result<Number, Error>          Escala y política explícitas


 Estas firmas describen fallos numéricos esperables, no recuperación de todo fallo físico. Suma y
 multiplicación no necesitan Result por un desbordamiento numérico interno inexistente en el
 dominio lógico; agotamiento de memoria sigue siendo fallo del proceso, como establece S19.




Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                   3
````

## Página 4

````text
 3 División y división entera
 N09 Cociente decimal exacto
 divide_exact(a, b) devuelve error si b es cero. Si el cociente tiene expansión decimal finita,
 devuelve ese valor exacto. En caso contrario devuelve InexactResult. No entrega aproximación,
 infinitos ni un racional de otro tipo oculto.

 Para decidir terminación puede reducirse el cociente de enteros a una fracción irreducible: su
 denominador positivo debe contener solo factores 2 y 5. Esto describe una condición exacta; el
 algoritmo concreto puede ser diferente. Un racional usado internamente para calcular no se
 convierte en categoría pública del lenguaje.

 N10 Cociente redondeado
 divide_round(a, b, scale, rounding) calcula el cociente y lo cuantiza directamente a la escala
 solicitada. No redondea primero a una precisión intermedia. La implementación puede operar con
 cociente y resto enteros para decidir la proximidad exacta.

 Si b es cero devuelve DivisionByZero. Con modo Exact y un resultado que necesita redondeo
 devuelve InexactResult. Con otro modo admitido devuelve el múltiplo correspondiente a la escala,
 incluso si el cociente no tiene expansión decimal terminante.

 N11 División y resto enteros
 divmod(a, b) exige operandos enteros y divisor no nulo. Devuelve Result de un registro con
 quotient y remainder, ambos Number enteros. quotient trunca hacia cero y remainder cumple a =
 b * quotient + remainder; su magnitud es menor que la del divisor y, si no es cero, tiene el signo de
 a.

 Ejemplo: divmod(-7, 3) produce quotient = -2 y remainder = -1. No se adopta el signo del resto del
 lenguaje anfitrión por accidente. Un operando no entero produce InvalidNumericOperand.

 N12 División en la sintaxis
 Si se introduce el operador /, su significado en esta versión será divide_exact y su resultado será
 Result. Los ejemplos que lo encadenen deben manejar o propagar explícitamente el error. La
 gramática puede optar por mantener solo el nombre de función inicial.

 Se rechaza simplificar (1 / 3) * 3 a 1 sin preservar el fallo de la primera división. Aunque las
 operaciones exactas tienen leyes algebraicas, la división parcial expresada mediante Result exige
 respetar sus variantes y orden.




Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                     4
````

## Página 5

````text
 4 Escala y redondeo
 N13 Escala de operación
 scale es un Number entero no negativo. El paso de cuantización es 10 elevado a -scale. Escala 0
 significa enteros y escala 2, múltiplos de 0.01. Esta versión no admite escalas negativas; redondear
 a decenas puede añadirse después con una regla explícita.

 La escala no es un tipo especializado ni una propiedad de formato conservada automáticamente.
 Un éxito de quantize(x, 2, modo) cumple is_quantized(value, 2), aunque su valor canónico se
 escriba 1.2 en lugar de 1.20.

 N14 Modos admitidos

   Modo conceptual                                 Regla

   Exact                                           Solo aceptar si no hay pérdida de valor

   HalfEven                                        Más cercano; empate al coeficiente entero par

   HalfAwayFromZero                                Más cercano; empate alejándose de cero

   TowardZero                                      Truncar hacia cero

   TowardPositive                                  Menor múltiplo de la escala que no sea menor que x

   TowardNegative                                  Mayor múltiplo de la escala que no sea mayor que x


 No hay modo por defecto. Todas las operaciones que pueden perder información reciben una
 política explícita. Los nombres son técnicos y se fijarán en la gramática. No se usa la etiqueta
 ambigua “redondeo comercial” como definición.

 N15 Cuantización
 quantize(x, scale, rounding) devuelve Result<Number, Error>. Elige según N14 entre los múltiplos
 de la escala. Si x ya pertenece a esa retícula, todos los modos devuelven x. Exact devuelve
 InexactResult cuando x no pertenece.

 El empate se decide con el valor exacto, sin epsilon. En HalfEven, “par” se refiere al entero
 resultante de dividir el candidato por el paso de cuantización; funciona de igual manera con
 números negativos.

 N16 Propiedades del resultado
 El éxito siempre cumple is_quantized(value, scale). En los modos al más cercano, la distancia al
 valor matemático no supera la mitad del paso; en los modos dirigidos es menor que un paso. Exact
 conserva el valor o falla. Estas son garantías del operador, no pruebas de corrección de una política
 financiera.




Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                     5
````

## Página 6

````text
 5 Precisión rangos y representación acotada
 N17 Precisión general
 El dominio no fija una cantidad universal de dígitos. Evita elegir un tamaño de máquina como
 semántica de Number. Tampoco promete memoria infinita, operaciones de tiempo constante o
 rendimiento equivalente a enteros nativos.

 Cada implementación debe declarar límites operativos y comportamiento al agotarlos. Un límite de
 recursos no autoriza devolver un valor redondeado, envuelto o saturado. El documento 06
 distinguirá rechazo de entradas por presupuesto y fallo del proceso durante ejecución.

 N18 Fronteras decimales acotadas
 Un esquema externo puede describir precisión P y escala S, con P entero positivo y 0 <= S <= P. P
 cuenta los dígitos del coeficiente entero escalado, sin contar el signo; S fija los decimales. El valor
 debe ser múltiplo de 10 elevado a -S y su magnitud debe ser menor que 10 elevado a P-S.

 Ejemplo: P = 5 y S = 2 admiten desde -999.99 hasta 999.99 en pasos de 0.01. Estas condiciones
 describen un destino; no crean Decimal<P, S> como tipo público de negocio. Un campo sin signo
 añade la condición de no negatividad.

 N19 Conversión al destino
 La conversión es exacta por defecto y devuelve NotRepresentable si no cumple escala o rango. Si
 se desea redondear, el programa cuantiza primero con una política explícita y después comprueba
 representabilidad. El control de rango se aplica al valor redondeado.

 999.995 redondeado a dos decimales mediante HalfEven produce 1000 y ya no cabe en el destino
 anterior. No se conservan los dígitos bajos como sustituto. P y S son parámetros generales del
 esquema, sujetos a contratos de integridad y rango.

 N20 Enteros de tamaño fijo
 Una frontera nativa puede exigir un entero con ancho W y signo, con W entero positivo. Para signo,
 el rango comienza en el negativo de 2 elevado a (W - 1) y termina en 2 elevado a (W - 1) menos 1;
 sin signo, desde 0 hasta 2 elevado a W menos 1. El valor debe ser entero. Si no cabe, la conversión
 falla.

 Ancho, signo y disposición son opciones de representación, no nuevos tipos de negocio. El
 almacenamiento interno compacto puede promoverse a otro exacto antes de desbordar. Una
 especialización no puede cambiar la respuesta del programa para ocultar su límite físico.




Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                       6
````

## Página 7

````text
 6 Contratos fallos y comprobación
 N21 Condiciones numéricas comprobables
 El comprobador conoce la finitud de Number y el significado exacto de comparaciones, is_integer e
 is_quantized. Estos predicados se admiten como operaciones incorporadas del catálogo de
 contratos; scale debe tener su requisito establecido antes de usarse en un predicado.

 Pueden propagarse intervalos de suma, resta y multiplicación cuando los límites y signos estén
 justificados. Dividir exige considerar divisor cero, terminación decimal y la variante de resultado.
 Redondear cambia las obligaciones de rango y debe incorporar el resumen correcto del modo.

 N22 Fallos numéricos generales

   Código conceptual de Error                      Causa

   DivisionByZero                                  Divisor numérico igual a cero

   InexactResult                                   Exactitud solicitada no representable

   InvalidNumericOperand                           Operando fuera del dominio exigido

   InvalidScale                                    Escala negativa o no entera

   InvalidRoundingMode                             Política recibida no admitida

   InvalidNumericText                              Texto que no representa un decimal válido

   NotRepresentable                                Valor fuera de escala o rango del destino


 Son alternativas técnicas de Error, no tipos nominales numéricos. Una llamada incompatible se
 diagnostica según T11; una API de validación devuelve el fallo. No se agregan errores ocultos a una
 firma directa.

 Tras evaluar argumentos en orden, divide verifica divisor cero, escala y modo, en ese orden
 cuando existan; quantize verifica escala y modo. divmod verifica integridad de a, integridad de b y
 divisor cero. La primera condición inválida determina el error. Un P inválido usa
 InvalidNumericOperand; un S inválido usa InvalidScale en la validación del destino.

 N23 Exactitud y contratos de retorno
 Los operadores con fallos esperables retornan Result. Después de seleccionar éxito, las garantías
 del operador quedan disponibles sin repetir su validación. Las condiciones desconocidas de una
 función siguen el control de retorno de T22 y su error ContractViolation.

 Un divide_exact conocido como 1 entre 3 devuelve un error válido y no obliga por sí solo a rechazar
 el programa. Intentar presentarlo como un éxito que el comprobador demuestra inválido sí se
 rechaza. Un error numérico no se convierte automáticamente en fallo de contrato.




Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                    7
````

## Página 8

````text
 7 Texto formatos e intercambio
 N24 Conversión desde texto
 parse_number acepta texto con una especificación decimal independiente de la configuración
 regional: signo opcional, dígitos, parte decimal opcional y exponente decimal opcional. No acepta
 separadores de miles, NaN, infinito, espacios ni contenido sobrante en la forma canónica de
 intercambio.

 La gramática detallará las formas exactas. En esta versión se propone exigir al menos un dígito
 antes del punto y al menos uno después si el punto aparece. Se permiten ceros iniciales en
 entrada; la salida canónica los elimina. El exponente se interpreta en base 10 y exige dígitos.

 N25 Salida canónica
 Para una representación única se usa la forma coeficiente-exponente de N02: coeficiente entero
 sin ceros iniciales, sin signo positivo y sin factores 10, letra e minúscula y exponente entero sin
 signo positivo ni ceros iniciales. El cero se escribe 0e0. Ejemplos: 12.30 se serializa como 123e-1;
 1000 como 1e3.

 Esta salida es para intercambio y comparación reproducible; no pretende ser el formato visual
 habitual. parse_number de esa salida recupera el mismo valor. Los bytes de un texto original
 diferente no se recuperan salvo que se conserven aparte.

 N26 Presentación a escala fija
 format_fixed(x, scale) devuelve Result<Text, Error>. Verifica primero la escala y después que x
 sea múltiplo de ella; si no lo es, devuelve InexactResult. Agrega ceros de presentación y no
 redondea por sí mismo. 1.2 a escala 2 se muestra como 1.20. Para modificar un valor no
 compatible, se cuantiza explícitamente antes de formatear.

 Un adaptador regional puede usar coma u otros separadores mediante política explícita; eso no
 cambia el análisis del código fuente ni el formato canónico. Moneda y unidades son campos o
 reglas del negocio, no inferencias del texto numérico.

 N27 Binario y memoria externa
 Ancho, signo, orden de bytes, codificación decimal y convenciones de campos se declaran en el
 esquema externo. No se serializa la memoria privada de Number suponiendo que sea portable.
 NaN, infinitos y formatos binarios flotantes se rechazan como entradas numéricas de este
 subconjunto hasta que exista un adaptador especificado.




Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                    8
````

## Página 9

````text
 8 Implementación y criterios de costo
 N28 Referencia y especializaciones
 El intérprete de referencia debe calcular coeficientes y exponentes exactos mediante una
 biblioteca o mecanismo verificado. Puede usar enteros nativos para casos pequeños y enteros
 ampliables para los demás. La elección no debe modificar resultados, igualdad, errores de
 operación ni contratos.

 Una rutina binaria flotante solo puede sustituir una operación exacta si se demuestra equivalencia
 para todo el dominio que admite esa ruta. Que dos resultados coincidan en ejemplos no constituye
 esa prueba. No se activa un modo aproximado por una opción genérica de optimización.

 N29 Recursos y límites
 Multiplicar muchos dígitos, alinear exponentes distantes y formatear escalas enormes pueden
 exigir mucha memoria y tiempo. La forma compacta de un literal con exponente no garantiza costo
 pequeño al operarlo. El runtime debe declarar presupuestos y rechazar o detener trabajo que no
 pueda realizar sin pérdida de exactitud.

 El costo de una asignación interna y el agotamiento de memoria son límites físicos. Las
 equivalencias numéricas se establecen para ejecuciones con recursos suficientes; no se promete
 que dos algoritmos agoten memoria en el mismo punto. Un cambio de algoritmo no puede alterar
 fallos numéricos representados como Result.

 N30 Optimización y orden
 No se desplaza redondeo, manejo de errores ni efectos a través de otras operaciones sin prueba de
 equivalencia. La asociatividad de la suma exacta de valores no autoriza reordenar la evaluación de
 expresiones que pueden producir efectos, fallar o no terminar. El alcance inicial conserva la
 ejecución secuencial definida por S03.

 Plan de evidencia
 Se medirán ciclos o tiempo con metodología declarada, asignaciones y memoria máxima para
 tamaños pequeños y crecientes, exponentes separados y divisiones no terminantes. Se
 compararán rutas compactas y de precisión ampliable con los mismos datos, contratos y políticas.

 No hay mediciones todavía. La hipótesis es que la promoción exacta y la eliminación de controles
 demostrados permitan equilibrar simplicidad y costo. Si una representación específica ofrece
 ventajas, se documentarán dominio válido, ahorro y condiciones de conversión antes de exponerla
 al programador.

 La suite verificará también ida y vuelta canónica, ausencia de redondeo intermedio, signos del
 resto y conservación de is_quantized en consumidores. Se incluirán casos generados además de
 ejemplos puntuales.




Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                  9
````

## Página 10

````text
 9 Ejemplos de liquidación y límites
 N31 Políticas de negocio explícitas
 El modelo no decide la moneda, el porcentaje aplicable ni si una comisión se redondea por registro
 o al final. La liquidación recibe esas reglas como datos y decisiones explícitas. Las mismas entradas
 y políticas deben producir los mismos valores y errores numéricos.

 Para un importe 125.50 y una tasa 0.015, multiply produce exactamente 1.8825. Con escala 2,
 HalfEven produce 1.88. El campo de salida se valida luego contra el esquema y format_fixed
 produce el texto 1.88. Si el importe fuera 100 y la tasa 0.01225, el resultado exacto sería 1.225 y la
 elección de modo sí cambia el resultado.

   Valor exacto                Escala       Modo                         Valor numérico

   1.225                       2            HalfEven                     1.22

   1.225                       2            HalfAwayFromZero             1.23

   -1.225                      2            HalfEven                     -1.22

   -1.225                      2            HalfAwayFromZero             -1.23

   -1.225                      2            TowardPositive               -1.22

   -1.225                      2            TowardNegative               -1.23



 Momento del redondeo
 Dos importes exactos de 0.005, cuantizados individualmente a escala 2 con HalfEven, producen
 cero cada uno. Su suma es cero. Sumar primero y cuantizar después produce 0.01. El compilador
 no puede intercambiar esas políticas como si fueran equivalentes.

 Límite externo después de redondear
 999.995 cuantizado a escala 2 con HalfEven produce 1000. El destino de precisión 5 y escala 2
 admite como máximo 999.99: la conversión devuelve NotRepresentable. Ningún truncado
 silencioso, cambio de signo ni promoción del esquema externo está permitido.

 El esquema puede ser más amplio, pero cambiarlo es una decisión explícita. Number interno puede
 representar 1000 sin que eso vuelva compatible cualquier destino.




Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                  10
````

## Página 11

````text
 10 Escenarios de conformidad numérica
 La tabla define entradas exactas y resultados verificables. La notación Ok o Err identifica variantes
 conceptuales. Los casos formarán parte de la suite del documento 05; comprobar estos ejemplos
 no equivale a haber implementado el lenguaje.

   Caso     Operación                                                Resultado esperado

   MN01     add(0.1, 0.2)                                            0.3 exacto

   MN02     equals(1, 1.00)                                          TRUE

   MN03     multiply(125.50, 0.015)                                  1.8825 exacto

   MN04     divide_exact(1, 8)                                       Ok(0.125)

   MN05     divide_exact(1, 3)                                       Err(InexactResult)

   MN06     divide_exact(0, 0)                                       Err(DivisionByZero)

   MN07     divide_round(1, 3, 2, HalfEven)                          Ok(0.33)

   MN08     divide_round(-1, 3, 2, TowardNegative)                   Ok(-0.34)

   MN09     quantize(1.225, 2, HalfEven)                             Ok(1.22)

   MN10     quantize(-1.225, 2, HalfAwayFromZero)                    Ok(-1.23)

   MN11     quantize(1.225, 2, Exact)                                Err(InexactResult)

   MN12     quantize(1.2, 2, Exact)                                  Ok(1.2)

   MN13     divmod(-7, 3)                                            Ok({quotient: -2, remainder: -1})

   MN14     parse_number("1,25")                                     Err(InvalidNumericText)

   MN15     parse_number("NaN")                                      Err(InvalidNumericText)

   MN16     canonical(12.30)                                         "123e-1"

   MN17     format_fixed(1.2, 2)                                     Ok("1.20")

   MN18     fit_decimal(1000, 5, 2)                                  Err(NotRepresentable)

   MN19     fit_signed_integer(128, 8)                               Err(NotRepresentable)

   MN20     quantize(1.2, -1, HalfEven) en API de validación         Err(InvalidScale)


 fit_decimal y fit_signed_integer son nombres de validaciones conceptuales, no tipos nuevos. Una
 llamada directa con un parámetro refinado refutado se rechaza según T11; MN20 prueba una API
 que admite escala general y la valida.



Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                     11
````

## Página 12

````text
 11 Decisiones alternativas y trazabilidad
 N32 Decisiones para revisión

   Decisión propuesta                    Ventaja buscada                          Costo o renuncia

   Un Number decimal exacto y            Tipo general y resultados                Precisión ampliable consume
   finito                                reproducibles                            recursos

   División exacta o redondeo                                                     1/3 no devuelve Number
                                         Evitar pérdida silenciosa
   explícito                                                                      exacto

                                                                                  Formato se conserva por
   Escala como política y contrato       Evitar familias de tipos
                                                                                  separado

                                                                                  Adaptadores aproximados se
   Sin NaN ni infinito                   Comparación total y contratos simples
                                                                                  difieren

   Promoción interna exacta              Optimización sin cambio de significado   Rendimiento debe medirse

   Rango externo validado después
                                         Compatibilidad real con el destino       Puede fallar tras el redondeo
   de cuantizar


 La alternativa de racionales exactos simplifica algunos cocientes pero introduce otra
 representación y costos que deben evaluarse. El flotante binario puede favorecer hardware, pero
 no sustituye automáticamente esta semántica. El decimal fijo simplifica almacenamiento a costa
 de límites y contextos. No se afirma que una opción sea universalmente superior.

 Relación con los documentos anteriores
 N01 a N08 concretan S05 y S20 y la categoría general de T01. N09 a N23 precisan los fallos y
 contratos de S12, S18 y T21 a T24. N04 y N21 amplían explícitamente los predicados incorporados
 de T13. N24 a N27 desarrollan esquemas de S22. N28 a N30 mantienen las restricciones de
 optimización de S23.

 El contexto 1.1 y el Brief 1.0 son la base de objetivos. Las decisiones de representación y
 operaciones de esta propuesta todavía no se incorporaron mediante edición a esos archivos; este
 documento las concreta para la revisión de la serie.

 Próximo paso
 El documento 04 fijará sintaxis y gramática inicial con Number, Result, contratos, llamadas y
 manejo explícito de fallos. La arquitectura definirá presupuestos, biblioteca numérica y rutas de
 especialización. Los formatos concretos de archivo se seleccionarán para el caso conductor.

 La serie se detiene aquí para autorización de continuidad o correcciones del modelo numérico. No
 se afirma ejecución del lenguaje ni resultados de benchmarks; los ejemplos se contrastan como
 aritmética de referencia durante la preparación del documento.




Documento 03 · Propuesta 0.1 · 20 de octubre de 2026                                                              12
````

