# Contexto histórico · Versión documental 1.1

Transcripción textual del documento de contexto anterior al nombre Traza. Conserva su contenido histórico; las especificaciones posteriores concretan decisiones abiertas. No es una nueva revisión semántica.

## PARSED TEXT FOR PAGE: 1 / 16

````text
Contexto para diseñar un nuevo lenguaje
funcional
C COBOL y Haskell como referencias de arquitectura
Fecha: 14 de octubre de 2026 · Versión del documento: 1.1

1 Propósito y estado del proyecto
El objetivo establecido es crear un lenguaje de programación funcional nuevo y original que aproveche las
fortalezas de C, COBOL y Haskell. Este documento conserva los fundamentos explicados, la razón para elegir el
tercer lenguaje, el análisis comparativo con enfoque de abogado del diablo y las bases de diseño propuestas.
La orientación recomendada es un lenguaje funcional para reglas de negocio y procesamiento de datos, con
semántica numérica explícita, recursos controlados y ejecución auditable. Esta orientación es una propuesta
arquitectónica; el objetivo de crear un lenguaje nuevo sí proviene del usuario. El público centrado en equipos
financieros, integraciones y procesamiento de registros continúa siendo una hipótesis. Las decisiones más
recientes establecen tipos generales y contratos de retorno comprobados para evitar repetir validaciones de
información ya garantizada.
La comparación toma como referencias conceptuales C clásico, COBOL procedural y Haskell 2010. Las
características de una implementación, como las opciones aritméticas de IBM Enterprise COBOL, no deben
generalizarse a todos los compiladores. Las propuestas del nuevo lenguaje no están implementadas ni
validadas. Su originalidad tampoco está demostrada.
Combinar características no constituye una especificación. Control de recursos, abstracción funcional y
mantenimiento empresarial plantean tensiones. El diseño debe establecer qué promete, qué sacrifica y cómo
se verificará cada garantía.

1 1 Distinción entre contexto y decisiones

 Categoría                 Contenido                                    Estado

                           Crear un lenguaje funcional nuevo y
 Objetivo del usuario                                                   Establecido
                           original inspirado en los tres lenguajes

                           Comparación profunda y examen de
 Método del usuario                                                     Establecido
                           fortalezas y debilidades

 Tercer lenguaje           Haskell por su distancia conceptual
                                                                        Referencia usada en el análisis
 recomendado               respecto de C y COBOL

                           Reglas de negocio y procesamiento de
 Enfoque de producto                                                    Propuesto
                           datos

                           Evitar tipos específicos de negocio y
 Tipos generales           justificar especializaciones por ejecución   Criterio establecido por el usuario
                           o memoria

                           Resultados tipados con condiciones
 Retornos de funciones                                                  Dirección incorporada por el usuario
                           verificadas y reutilizables


                                                                                                               Página 1
````

## PARSED TEXT FOR PAGE: 2 / 16

````text
    Categoría                 Contenido                                    Estado

                              Demostración estática cuando sea posible
                                                                           Recomendación adoptada para documentar el
    Mecanismo de garantías    y comprobación al retornar en los demás
                                                                           diseño
                              casos

                              Evaluación estricta, errores como valores,
    Semántica restante                                                     Propuestas por validar
                              decimal explícito y efectos declarados

    Nombre y sintaxis final   No definidos                                 Abiertos

                              Intérprete pequeño antes de un
    Implementación                                                         Ruta recomendada
                              compilador completo

                              Integración coherente de contratos de
    Originalidad                                                           Hipótesis pendiente de investigación
                              dominio y ejecución




2 Principios del lenguaje C
C es un lenguaje de propósito general que permite controlar de forma directa cómo se almacenan y procesan
los datos. Resulta relevante para sistemas operativos, dispositivos embebidos y programas donde importan los
recursos y el rendimiento.
Sus fundamentos explicados son los siguientes:
      Programación estructurada y procedural. El programa se organiza en funciones y utiliza condiciones como if
       y switch, y ciclos como for y while.
      Tipos explícitos. int, double y char determinan representaciones y operaciones admisibles.
      Compilación. En el proceso habitual, el preprocesador resuelve directivas, el compilador traduce el código y
       el enlazador integra las partes necesarias.
      Punteros. Permiten referirse a direcciones de memoria, modificar datos y construir estructuras dinámicas.
      Gestión de memoria dinámica. Las reservas realizadas con malloc deben liberarse con free cuando
       corresponda. Las variables locales comunes tienen duración gestionada automáticamente.
      Responsabilidad del programador. No se comprueban automáticamente todos los límites y usos de
       memoria; determinadas operaciones incorrectas producen comportamiento indefinido.
      Biblioteca estándar y portabilidad. El estándar define servicios comunes, aunque existen detalles
       dependientes del sistema. [1]




                                                                                                                  Página 2
````

## PARSED TEXT FOR PAGE: 3 / 16

````text
2 1 Ejemplo introductorio de C
#include <stdio.h>

int sumar(int a, int b)
{
    return a + b;
}

int main(void)
{
    int resultado = sumar(3, 4);

    if (resultado > 5) {
        printf("Resultado: %d\n", resultado);
    }

    return 0;
}

stdio.h declara funciones como printf. sumar recibe y devuelve enteros. main es el punto de entrada de un
programa C común en un entorno alojado. if decide si se imprime el resultado; %d representa un int y return 0
indica finalización correcta. La salida es Resultado: 7.
La idea central es combinar operaciones simples, funciones y control de memoria. Esa libertad exige cuidar
tipos, límites y validez de los punteros. C define una máquina abstracta; no debe entenderse simplemente
como ensamblador portable. [1]

3 Principios del lenguaje COBOL
COBOL significa Common Business Oriented Language. Está orientado al procesamiento de datos de negocio y
se utiliza en banca, seguros, administración y procesos por lotes.
Sus fundamentos explicados son los siguientes:
   Orientación a registros y transacciones. Trabaja con archivos, cuentas, importes y grandes volúmenes de
    datos estructurados.
   Sintaxis descriptiva. MOVE, ADD, READ y PERFORM expresan operaciones con vocabulario cercano al inglés.
   Organización por divisiones. IDENTIFICATION identifica el programa; ENVIRONMENT describe su relación
    con el entorno; DATA define los datos y PROCEDURE contiene las instrucciones.
   Descripción mediante PIC. PIC 9(5) describe cinco dígitos y PIC X(20), veinte caracteres. USAGE especifica
    aspectos de la representación interna.
   Aritmética decimal. PIC 9(5)V99 describe cinco posiciones enteras y dos decimales. V representa un
    separador implícito.
   Programación procedural y estructurada. Párrafos y secciones organizan instrucciones; IF y EVALUATE
    permiten decisiones y PERFORM, ejecución y repetición.
   Procesamiento de archivos. OPEN, READ, WRITE y CLOSE permiten recorrer registros y producir salidas.
   Compilación e integración. En mainframe, un JCL puede preparar archivos y ejecutar un programa COBOL.
    JCL y COBOL son lenguajes distintos.




                                                                                                        Página 3
````

## PARSED TEXT FOR PAGE: 4 / 16

````text
3 1 Ejemplo introductorio de COBOL
           IDENTIFICATION DIVISION.
           PROGRAM-ID. CALCULAR-TOTAL.

           DATA DIVISION.
           WORKING-STORAGE SECTION.
           01 WS-PRECIO       PIC 9(5)V99 VALUE 125.50.
           01 WS-CANTIDAD     PIC 9(3)     VALUE 4.
           01 WS-TOTAL        PIC 9(8)V99.
           01 WS-TOTAL-SALIDA PIC Z(7)9.99.

           PROCEDURE DIVISION.
               COMPUTE WS-TOTAL = WS-PRECIO * WS-CANTIDAD

                 IF WS-TOTAL > 0
                     MOVE WS-TOTAL TO WS-TOTAL-SALIDA
                     DISPLAY "Total: " WS-TOTAL-SALIDA
                 END-IF

                 STOP RUN.

PROGRAM-ID identifica el programa. WORKING-STORAGE declara datos de trabajo. COMPUTE calcula 502,00;
el campo de salida prepara una representación con punto decimal visible. STOP RUN termina la ejecución. El
ejemplo asume la convención decimal mostrada.
La idea central es combinar estructuras precisas, operaciones explícitas y procesamiento de registros. Para
comprender el programa hay que estudiar la lógica, los datos y los archivos que utiliza. La representación
decimal no elimina límites de precisión ni decisiones de redondeo. [4]

4 Elección de Haskell como tercera referencia
Haskell fue recomendado por su distancia conceptual respecto del enfoque principalmente imperativo de C y
COBOL. Es funcional puro, con tipos estáticos, inmutabilidad y evaluación no estricta. Incluye funciones de
orden superior, tipos algebraicos y coincidencia de patrones. [2, 3]
La comparación arquitectónica busca explorar estado y efectos, modelado del dominio y composición de reglas.
Elegir Haskell para este análisis no determina el lenguaje en que deba implementarse el proyecto.

 Aspecto                C                             COBOL clásico                Haskell

 Enfoque                Recursos y memoria            Datos de negocio             Composición de funciones

                                                                                   Expresiones que producen
 Lógica                 Instrucciones sobre estado    Operaciones sobre campos
                                                                                   valores

 Datos habituales       Variables modificables        Registros modificables       Valores inmutables

 Repetición             Ciclos                        PERFORM                      Recursión y map o fold

                                                                                   Acciones representadas
 Entorno                Puede mezclarse con cálculo   Puede mezclarse con reglas
                                                                                   mediante tipos

                        Cómo se ejecuta y cuánto                                   Cómo se compone y qué
 Pregunta útil                                        Qué datos y reglas procesa
                        cuesta                                                     expresa el modelo




                                                                                                            Página 4
````

## PARSED TEXT FOR PAGE: 5 / 16

````text
4 1 Una suma expresada en los tres lenguajes
/* C: actualizar un acumulador */
int total = 0;
for (int i = 0; i < cantidad; i++) {
    total += valores[i];
}
        *> COBOL: actualizar un campo de trabajo
             MOVE ZERO TO WS-TOTAL
             PERFORM VARYING WS-I FROM 1 BY 1
                 UNTIL WS-I > WS-CANTIDAD
                 ADD WS-VALOR(WS-I) TO WS-TOTAL
             END-PERFORM
-- Haskell: definir una transformación
total :: [Int] -> Int
total valores = sum valores

Estos fragmentos ilustran estilos; no son implementaciones completas ni un benchmark. Los dos primeros
describen cambios en un acumulador; el tercero expresa el resultado mediante una función. La brevedad no
demuestra superioridad, ni la firma Int garantiza ausencia de desbordamiento.

5 Comparación arquitectónica central
 Pregunta                 C                                COBOL                         Haskell

 Perspectiva              Objetos y memoria                Registros y campos            Evaluación de funciones

 Hace visible             Representación y direcciones     Forma de datos y pasos        Dependencias y tipos

 Exige disciplina en      Memoria y límites                Estado y formatos             Abstracciones y recursos

 Expresa
                          Instrucciones                    Procedimientos                Expresiones
 transformación

 Orienta búsqueda de
                          Accesos y conversiones           Campos y movimientos          Patrones y evaluación
 defectos

                                                           Confundir formato con         Confundir elegancia con
 Tentación de diseño      Optimizar antes del dominio
                                                           significado                   operación


La regla de diseño recomendada es expresar el negocio mediante transformaciones de valores y declarar por
separado efectos, formatos externos y políticas numéricas. Ser funcional no obliga a adoptar evaluación
perezosa.

6 C bajo el enfoque de abogado del diablo
El aporte principal de C para el proyecto es la conciencia del costo y de la representación. Toda transformación
implica asignaciones, copias, accesos, llamadas o liberaciones. El nuevo lenguaje debería permitir investigar
estos costos sin imponer manipulación de memoria a toda regla de negocio.

 Defensa                       Objeción                                     Propuesta

 Control de recursos           Responsabilidad difícil de verificar         Propiedad y duración comprobables

 Representación externa        Convenciones de plataforma                   Esquemas explícitos


                                                                                                                    Página 5
````

## PARSED TEXT FOR PAGE: 6 / 16

````text
 Defensa                     Objeción                                 Propuesta

 Núcleo pequeño              Complejidad desplazada a convenciones    Contratos uniformes

 Integración nativa          Fallos que cruzan la frontera            Encapsulación y marcado

 Operaciones de bajo nivel   Riesgo en código ordinario               Capa restringida


Tomaríamos representación explícita, interoperabilidad y control de recursos. Rechazaríamos punteros sin
restricciones en código normal, conversiones peligrosas silenciosas y comportamiento indefinido en
operaciones del núcleo seguro. En C, el desbordamiento de enteros con signo es una de las situaciones que
puede producir comportamiento indefinido. [1]
La crítica a nuestra propuesta es que verificar tiene costo y que la propiedad de recursos añade complejidad. La
respuesta recomendada es eliminar comprobaciones cuando su innecesariedad pueda demostrarse y
conservarlas en los demás casos. Seguridad, libertad absoluta y costo cero no son promesas simultáneamente
defendibles.

7 COBOL bajo el enfoque de abogado del diablo
El aporte principal es tratar los datos de negocio como elementos que necesitan estructura, precisión y
contratos. Sin embargo, dos campos con la misma cantidad de dígitos pueden representar monedas,
porcentajes o cantidades. Compatibilidad física no implica compatibilidad semántica.

 Defensa                     Objeción                                 Propuesta

 Campos precisos             La forma no garantiza validez            Datos generales y contratos comprobados

 Aritmética decimal          Sigue habiendo límites y redondeo        Semántica formal

 Sintaxis verbal             Verbosidad no elimina ambigüedad         Pocas formas equivalentes

 Trabajo con registros       El formato condiciona la lógica          Decodificar al dominio

 Procesos extensos           Estado compartido y dependencias         Entradas y salidas explícitas


Tomaríamos centralidad de los datos, decimal y atención a formatos externos. Rechazaríamos estado global
como mecanismo habitual, acoplamiento de almacenamiento y significado, y pérdida inadvertida de
información. La propuesta inicial de tipos específicos de dominio se reemplaza por tipos generales y
validaciones explícitas, conforme a la actualización del usuario.
La precisión de resultados intermedios en IBM Enterprise COBOL depende de reglas y opciones aritméticas. La
exactitud de una representación decimal no garantiza por sí sola el resultado financiero esperado. [4]
La crítica a la propuesta inicial era que tipos demasiado específicos podían volver pesado un cálculo sencillo. La
simplificación elimina esa exigencia. Se conserva la recomendación de inferencia local y cambios explícitos
cuando se pierde información.

8 Haskell bajo el enfoque de abogado del diablo
El aporte principal es razonar sobre una regla por sus entradas y su resultado, separando acciones sobre el
entorno. IO representa acciones externas, pero IO a no distingue por sí solo archivos, red y otros recursos. [5]


                                                                                                           Página 6
````

## PARSED TEXT FOR PAGE: 7 / 16

````text
 Defensa                    Objeción                                 Propuesta

 Funciones puras            No garantizan terminación                Errores explícitos y propiedades

 Tipos expresivos           El modelo puede ser incorrecto           Casos reales de dominio

 Evaluación perezosa        Costos y retención menos visibles        Estricta por defecto

 Abstracción                Puede esconder comportamiento            Diagnósticos comprensibles

 Inmutabilidad              No resuelve conflictos externos          Concurrencia y transacciones aparte


Tomaríamos funciones como valores, composición, tipos algebraicos, patrones e inmutabilidad observable.
Rechazaríamos funciones parciales como conveniencia cotidiana y evaluación diferida implícita como regla
general.
Pureza y totalidad son propiedades distintas. La semántica de Haskell contempla valores indefinidos
relacionados con errores o falta de terminación. [6]
La crítica a nuestra propuesta es que demasiados tipos y contratos pueden hacer más difícil el lenguaje que el
problema. Una regla común debería poder leerse sin teoría avanzada de tipos.

9 Tensiones que requieren decisiones explícitas
 Tensión                    Costo                                    Posición inicial

 Inmutabilidad y                                                     Reutilización interna semánticamente
                            Copias y asignaciones
 rendimiento                                                         equivalente

 Seguridad y control        Restricciones y comprobaciones           Núcleo seguro y frontera insegura

 Decimal y velocidad        Costo aritmético                         Políticas numéricas explícitas

 Inferencia y claridad      Dependencias menos visibles              Inferencia local y firmas públicas

 Diferimiento y
                            Retención y costo oculto                 Estricta por defecto
 previsibilidad

 Tipos y facilidad          Complejidad de compilación               Tipos generales y especialización justificada

 Portabilidad y
                            Diferencias de plataforma                Formatos externos independientes
 representación

 Auditoría y optimización   Volumen y restricciones                  Fronteras y operaciones seleccionadas


Ninguna elección es gratuita. Los costos deben corresponder al público objetivo. La hipótesis inicial de equipos
financieros, integraciones y registros debe validarse antes de convertirse en restricción de producto.

10 Liquidación como caso conductor
El caso propuesto procesa movimientos y calcula comisiones. Obliga a discutir fallos, formatos, memoria,
reinicios y políticas numéricas, evitando una comparación basada solamente en sumas pequeñas.




                                                                                                              Página 7
````

## PARSED TEXT FOR PAGE: 8 / 16

````text
 Situación                          Pregunta obligatoria

 Registro inválido                  Rechazar, detener o acumular errores

 Moneda diferente                   Conversión explícita y condiciones

 Resultado fuera de rango           Error, ampliación o saturación

 Decimales adicionales              Momento y política de redondeo

 Archivo enorme                     Procesamiento sin carga completa

 Fallo de escritura                 Resultados ya publicados

 Reinicio                           Prevención de duplicados

 Paralelismo                        Resultado y orden de salida

 Nueva regla                        Reproducción de resultados anteriores



10 1 Redondeo y orden de operaciones
Redondear la suma puede producir un resultado distinto de sumar cada valor redondeado. Con redondeo al
más cercano y empates al par, 0,005 a dos decimales produce 0,00; la suma 0,005 + 0,005 redondeada produce
0,01.
Una optimización que cambie el lugar del redondeo puede modificar el negocio. La semántica debe prohibirla
cuando no preserve el resultado especificado. Una suma acotada tampoco puede tratarse automáticamente
como suma matemática: si cada paso puede desbordar, reagrupar cambia dónde aparece el error.

11 Bases propuestas del nuevo lenguaje
 Elemento                   Propuesta                                    Límite

 Evaluación                 Estricta y con orden definido                No garantiza tiempo constante

 Valores                    Inmutables por defecto                       Mutación interna encapsulada posible

                            Estáticos generales con registros y
 Tipos                                                                   No prueban por sí solos reglas de negocio
                            variantes

                                                                         Nuevas transformaciones pueden invalidar
 Retornos                   Tipo base y condiciones comprobadas
                                                                         condiciones

 Ausencia                   Option<T>                                    Requiere decidir tratamiento

 Fallos esperables          Result<T, E>                                 Fallos de proceso necesitan política

 Efectos                    Declarados en firmas                         No son aislamiento de seguridad

                            Modelo general y representaciones
 Números                                                                 Exactitud y rango siguen requiriendo reglas
                            justificadas

 Recursos                   Duración y propiedad comprobables            Implementación compleja



                                                                                                                Página 8
````

## PARSED TEXT FOR PAGE: 9 / 16

````text
 Elemento                     Propuesta                                    Límite

 Formatos                     Esquemas independientes                      Necesitan versionado

 Patrones                     Exhaustividad comprobada                     Evolución afecta consumidores


La inmutabilidad observable permitiría actualizar internamente un buffer exclusivo cuando ningún observador
pueda distinguirlo de una transformación pura. La reutilización no debe quedar como requisito de corrección
del programa. Linear Haskell ya estudia datos mutables con interfaces puras y protocolos de recursos; esta idea
no debe atribuirse como invención del proyecto. [7]
Para una primera versión se permitirían funciones que no terminan. Demostrar terminación general
aumentaría mucho el alcance. En cambio, el acceso al primer elemento de una colección posiblemente vacía
debería devolver una alternativa, en lugar de constituir una operación parcial ordinaria.

11 1 Contratos de retorno comprobados
La nueva dirección establece que el programador no deba validar en cada uso la información que maneja. Cada
función entrega un resultado con un tipo general y, cuando corresponde, condiciones explícitas que ya fueron
verificadas. El consumidor puede reutilizar esas garantías mientras el valor y su contexto pertinente no
cambien.
Tipar un resultado como Number no demuestra que sea positivo, finito o esté dentro de un rango. Para
expresar estas propiedades se recomiendan restricciones sobre el tipo base, cercanas al concepto de tipos
refinados. No se exige crear tipos nominales de negocio como Porcentaje o Dinero. Una restricción expresa una
garantía lógica y no implica, por sí sola, una representación de memoria diferente.
fn porcentaje(valor: Number)
    -> Result<Number where 0 <= value <= 100, Error>
{
    ...
}

La sintaxis es conceptual. value representa el resultado exitoso al que se aplica la condición. La definición final
debe fijar cómo se expresan restricciones, cómo se propagan y qué sucede con valores numéricos no finitos. La
función debe rechazar valores que no satisfagan el contrato; declarar la condición sin verificarla no establece
una garantía.

 Momento                             Responsabilidad

 Entrada externa                     Validar información que todavía no tiene garantías

 Retorno de función                  Demostrar condiciones estáticamente o comprobarlas antes de entregar éxito

 Consumo de éxito                    Usar el valor sin repetir las condiciones ya establecidas

 Transformación posterior            Demostrar o comprobar las condiciones exigidas por el nuevo resultado

 Frontera insegura o cambio
                                     Restablecer garantías que hayan dejado de ser válidas
 externo




                                                                                                             Página 9
````

## PARSED TEXT FOR PAGE: 10 / 16

````text
11 2 Conservación de garantías y manejo de fallos
Validar el resultado exitoso no garantiza que la operación tenga éxito. Cuando una función devuelve Result, el
consumidor sigue siendo responsable de manejar o propagar el fallo. Al obtener el caso exitoso, el sistema
conserva sus restricciones sin exigir que el programador compruebe otra vez el rango o la estructura.
Las garantías pertenecen al valor y a las condiciones que las justifican. Multiplicar por dos un resultado entre 0
y 100 no conserva ese rango; puede establecer, bajo una aritmética adecuada, otro intervalo. Una operación
con desbordamiento o redondeo debe considerar su propia semántica antes de propagar conclusiones.
La inmutabilidad facilita mantener propiedades del valor. Las garantías sobre el entorno necesitan tratamiento
distinto: haber comprobado que existe un archivo o que una cuenta tiene saldo no asegura que esas
condiciones sigan siendo ciertas después. Esas propiedades requieren una instantánea, una transacción o un
protocolo de vigencia definido.
La regla de diseño es validar al establecer una garantía, conservarla durante su uso y comprobar nuevamente
cuando una transformación o frontera pueda invalidarla. Dos funciones pueden componer sus contratos si las
garantías de la primera satisfacen los requisitos de la segunda. Si esa relación no puede demostrarse, se
necesita una comprobación adicional; no se presume compatibilidad.

11 3 Límites y costo de los contratos
El compilador no puede demostrar cualquier condición de un programa general. Se recomienda comenzar con
restricciones simples, como intervalos y propiedades estructurales, y definir un subconjunto que el
comprobador pueda manejar. Las condiciones evaluadas en ejecución deben ser puras y tener un
comportamiento de terminación y fallo definido. No se permite prometer validez a partir de una comprobación
que puede omitir el fallo o no llegar a completarse.
Una condición no demostrada se comprueba en la frontera que entrega el resultado. Si falla, no se entrega un
éxito que incumpla el contrato. La política concreta de Error y las reglas de propagación siguen abiertas. El
diagnóstico debería identificar la función, la condición incumplida y el punto de comprobación.
Eliminar validaciones repetidas es un objetivo, no una promesa automática de ahorro. Debe medirse el costo
de las comprobaciones restantes, el tiempo de compilación y la conservación de garantías entre módulos. El
compilador puede eliminar controles redundantes cuando disponga de evidencia; una llamada externa o una
transformación no justificada puede exigir restablecerlos.

12 Simplificación de tipos y semántica numérica
El usuario establece que los tipos sean generales y que no existan tipos específicos salvo cuando favorezcan los
ciclos de reloj o el uso de memoria. Se interpreta generales como categorías reutilizables de datos, no como
una exigencia de parametrizar todos los tipos. Option<T> y Result<T, E> pueden seguir siendo contenedores
generales sin representar conceptos particulares de negocio.
La propuesta anterior de Money<C, P, S>, Rate<P, S> y tipos nominales de negocio queda reemplazada.
Moneda, tasa y escala pueden expresarse como datos o políticas de operación, sin crear familias de tipos para
cada concepto. Las restricciones de retorno añaden garantías al tipo general sin reintroducir esas familias. No
se ha medido todavía ninguna ventaja de rendimiento que justifique una especialización.
El criterio de simplicidad no elimina las diferencias semánticas entre entero, decimal y flotante.
Representación, rango y redondeo pueden cambiar resultados incluso con tamaños de almacenamiento



                                                                                                           Página 10
````

## PARSED TEXT FOR PAGE: 11 / 16

````text
similares. Estas diferencias deben especificarse; todavía no se decide si se exponen como tipos separados o
como representaciones y políticas explícitas del modelo numérico general.

    Tipo conceptual                        Uso

    Number                                 Categoría numérica general con reglas de exactitud y rango por definir

    Boolean                                Valores de verdad

    Text                                   Datos textuales con codificación definida

    Bytes                                  Datos binarios

    Colecciones y registros                Estructuras generales sin semántica de negocio incorporada

    Option y Result                        Ausencia y fallos expresados mediante contenedores generales

    Representaciones numéricas             Solo si se justifica su exposición por costo o memoria; nombres y mecanismos
    especializadas                         pendientes


Las reglas recomendadas son:
      Los literales decimales no pasan primero por flotante binario.
      Reducir escala exige política de redondeo explícita.
      Cambiar moneda requiere conversión explícita.
      La aritmética ordinaria no envuelve silenciosamente al desbordar.
      Dividir exige precisión de salida o política para resultados no representables.
      La precisión intermedia debe estar especificada.

12 1 Diseño numérico pendiente

    Diseño                       Ventaja                                       Problema

    Representación inferida
    bajo reglas numéricas        Código simple y optimización posible          La optimización no puede alterar resultados
    definidas

    Representación o
    contexto explícito por       Control de memoria y exactitud                Requiere políticas comprensibles
    operación o bloque


La propagación de precisión y escala en firmas parametrizadas deja de ser la dirección recomendada. El diseño
debe mantener firmas simples y justificar cualquier especialización con mediciones comparables. Ciclos de
reloj, asignaciones y memoria máxima son criterios de evaluación; ningún ahorro se presume antes de medirlo.

13 Separación de dominio y representación
Un registro externo puede usar texto fijo, decimal empaquetado o una codificación concreta. El modelo puede
usar registros generales con campos de cuenta, importe y fecha, sin exigir tipos nominales para cada concepto.
La frontera propuesta tendría contratos como estos, todavía exploratorios:
decode : Bytes -> Result<Record, Error>
encode : Record -> Result<Bytes, Error>



                                                                                                                    Página 11
````

## PARSED TEXT FOR PAGE: 12 / 16

````text
La decodificación validaría la estructura y las condiciones necesarias para construir el valor. El contrato de
retorno debe conservar las propiedades comprobadas del registro exitoso para que los consumidores no
repitan esas mismas validaciones. Los bytes inválidos no deberían convertirse inadvertidamente en un
movimiento válido. El esquema que justifica esas propiedades debe formar parte del contrato aunque la
sintaxis todavía esté pendiente.
Codificar después de decodificar no garantiza reproducir los bytes originales. Puede haber normalización,
espacios, variantes de signo o información descartada. Debemos distinguir equivalencia semántica e identidad
binaria. La segunda requiere preservar información adicional cuando sea necesaria.

14 Efectos recursos y responsabilidades de ejecución
Las firmas propuestas distinguirían leer archivos, escribir resultados, consultar un reloj y acceder a servicios. Un
efecto describe qué puede hacer una función. Para limitar sobre qué recurso puede hacerlo se necesitan
capacidades concretas, como un manejador autorizado para una entrada determinada.
Los tipos de efectos no garantizan transacciones distribuidas, ausencia de duplicados, recuperación tras una
caída ni reproducción de consultas externas. Estas propiedades requieren protocolos y plataforma de
ejecución.

 Responsabilidad                    Lugar principal

 Pureza tipos y evaluación          Lenguaje

 Operaciones numéricas y
                                    Semántica y biblioteca estándar
 esquemas

 Cierre de recursos y tareas        Runtime

 Checkpoints reintentos y
                                    Plataforma de procesamiento
 publicación

 Idempotencia                       Protocolo de aplicación

 Historial de reglas y entradas     Herramientas y operación


Incorporar funciones de un JCL a la sintaxis no resolvería estos problemas. Una plataforma de procesos puede
integrarse con el lenguaje conservando responsabilidades diferenciadas.

15 Sintaxis exploratoria de una comisión
El siguiente fragmento ilustra contratos deseados. No es código ejecutable ni especificación cerrada. También
están pendientes las reglas exactas de multiplicación, propagación de errores y cuantización.




                                                                                                           Página 12
````

## PARSED TEXT FOR PAGE: 13 / 16

````text
type Error =
    InvalidInput
  | NumericOverflow

fn commission(
    amount: Number,
    rate: Number,
    rounding: Rounding
) -> Result<Number, Error> {

     let raw = multiply_exact(amount, rate)?

     quantize(raw, scale: 2, rounding: rounding)
}

Los argumentos numéricos tienen el mismo tipo general. Sus nombres y las validaciones expresan sus funciones
en el negocio; el compilador no distingue una tasa de un importe solo por sus tipos. El redondeo y la escala de
salida se expresan en la operación, y los fallos esperables aparecen en el resultado. Rounding representa aquí
una política mediante una variante general, no una especialización numérica. Error ilustra variantes de fallo
generales. La regla no consulta archivos, reloj ni variables globales.
Este ejemplo sigue mostrando el tipo base. Con la nueva dirección, quantize debe declarar las propiedades
comprobadas de su resultado y commission debe conservarlas en su contrato público cuando sean necesarias
para los consumidores. La sintaxis exacta para escala y representabilidad está pendiente; no se atribuyen esas
garantías a Number sin un contrato que las establezca.
Para reproducir una prueba bastan entradas explícitas bajo la misma semántica. Para reproducir un proceso
completo también se necesitan versión de regla, datos externos y políticas utilizadas. Una firma no conserva
por sí sola ese historial.

16 Originalidad y alternativa de no crear un lenguaje
La objeción más fuerte es que muchas piezas tienen antecedentes. Koka incorpora seguimiento de efectos y
estrategias de gestión de memoria; Linear Haskell aborda linealidad y recursos. [7, 8]
Antes de justificar un lenguaje independiente hay que contrastarlo con biblioteca, DSL embebido y DSL
independiente. Un DSL es un lenguaje orientado a un dominio específico.

 Alternativa               Qué permite validar                      Condicionante

 Biblioteca                Operaciones y utilidad                   Semántica del anfitrión

 DSL embebido              Composición y contratos                  Diagnósticos e integración

 DSL independiente         Sintaxis y reglas propias                Implementación y herramientas

 Lenguaje general nuevo    Control semántico amplio                 Ecosistema y adopción


La recomendación conserva el objetivo de crear un lenguaje nuevo y propone validar primero su semántica
mediante un intérprete pequeño. Cambiar palabras reservadas no demostraría originalidad.
La hipótesis de diferenciación es integrar contratos numéricos, estructuras generales de datos,
representaciones externas y efectos en un sistema funcional coherente, con herramientas para explicar cómo
se obtuvo un resultado. No se ha demostrado que esta combinación sea inédita ni que requiera un lenguaje
general.



                                                                                                        Página 13
````

## PARSED TEXT FOR PAGE: 14 / 16

````text
17 Validación comparativa y criterios de evidencia
Las implementaciones comparadas deben resolver el mismo problema con políticas y validaciones
equivalentes. No corresponde asignar un puntaje general de mejor lenguaje ni comparar una versión
comprobada con otra que omite errores.

 Experimento                         Evidencia buscada

 Comisión en límites numéricos       Resultados y errores según política

 Mezcla de monedas                   Validación explícita y rechazo según la regla de negocio

 Retorno que incumple un rango       Rechazo estático o fallo comprobado antes de entregar éxito

 Reuso de un resultado validado      Garantía conservada y ausencia de controles redundantes verificable

 Transformación que rompe una
                                     Nueva comprobación o diagnóstico de contrato incompatible
 condición

 Operación que devuelve fallo        Manejo o propagación sin confundirlo con validación del éxito

 Condición sobre estado externo      Vigencia o protocolo explícito en lugar de confianza permanente

 Registro corrupto                   Error localizado sin valor válido

 Lote creciente                      Memoria medida y streaming

 Uso tras cierre de recurso          Rechazo o protección definida

 Ejecución secuencial y paralela     Equivalencia con condiciones documentadas

 Reinicio tras publicación parcial   Cumplimiento del protocolo

 Cambio de esquema                   Diagnósticos de incompatibilidad

 Optimización activada y
                                     Misma semántica observable
 desactivada

 Lectura por desarrollador nuevo     Comprensión y resolución medibles


El conjunto de conformidad debe incluir programas correctos y pruebas negativas que deban rechazarse. El
rendimiento debe medirse con controles equivalentes y datos representativos. Ninguna medición ha sido
realizada todavía.

18 Alcance recomendado para una primera versión
1.   Funciones puras y evaluación estricta.
2.   Tipos generales, registros y variantes sin tipos específicos de negocio.
3.   Contratos de retorno con restricciones simples y comprobación estática o en ejecución.
4.   Coincidencia de patrones exhaustiva.
5.   Option y Result.
6.   Modelo numérico general con rango, exactitud y redondeo definidos.
7.   Una familia limitada de esquemas externos.
8.   Procesamiento secuencial de registros.


                                                                                                           Página 14
````

## PARSED TEXT FOR PAGE: 15 / 16

````text
9. Efectos mínimos para entrada y salida.
10. Intérprete de referencia y diagnósticos.
11. Pruebas de conformidad semántica.
Concurrencia distribuida, metaprogramación avanzada, demostración de terminación y múltiples estrategias de
memoria se recomiendan para etapas posteriores. Estas exclusiones pertenecen a la propuesta de alcance; no
son decisiones aprobadas.
El primer entregable técnico recomendado es una especificación semántica mínima acompañada de la
liquidación como caso de prueba. Debe permitir discutir ejemplos y contraejemplos antes de comprometerse
con una sintaxis o un compilador.

19 Decisiones abiertas para continuar
 Decisión                   Posición discutida                        Qué falta resolver

 Dominio inicial            Reglas de negocio y registros             Validar público y problemas

 Alcance del lenguaje       Objetivo de lenguaje nuevo                General o especializado

 Evaluación                 Estricta por defecto                      Orden y diferimiento explícito

                            Generales salvo ventajas de ejecución o
 Tipos                                                                Categorías finales y especialización medible
                            memoria

 Aritmética                 Exactitud y conversiones explícitas       Representación y contexto numérico

 Memoria                    Propiedad y mutación encapsulada          Modelo concreto y costo

 Retornos                   Tipo general y condiciones comprobadas    Sintaxis y subconjunto de restricciones

 Garantías                  Reutilizar sin validación redundante      Propagación entre funciones y módulos

 Errores                    Result y Option                           Fallos de contrato de proceso y propagación

 Efectos                    Declarados en firmas                      Forma del sistema y capacidades

 Interoperabilidad          Frontera nativa restringida               Contratos y garantías

 Representación             Esquemas separados                        Formatos iniciales y versionado

 Auditoría                  Fronteras seleccionadas                   Qué preservar y cómo explicarlo

 Originalidad               Integración como hipótesis                Comparación amplia con antecedentes

 Implementación             Intérprete primero                        Plataforma y herramientas

 Sintaxis y nombre          Ejemplo exploratorio                      Definición posterior




20 Guía para retomar el trabajo
Al continuar, el objetivo debe seguir siendo un lenguaje funcional nuevo inspirado en C, COBOL y Haskell, con
revisión crítica de cada elección. Las propuestas de este documento deben tratarse como hipótesis hasta que
una especificación y pruebas permitan validarlas.


                                                                                                                Página 15
````

## PARSED TEXT FOR PAGE: 16 / 16

````text
La siguiente fase recomendada es definir la semántica del subconjunto inicial. Debe cubrir valores, evaluación,
tipos, contratos de retorno, conservación de garantías, errores, aritmética y efectos mínimos, usando una
liquidación y casos límite como evidencia. Toda garantía nueva debe indicar qué comprueba el compilador, qué
comprueba el runtime y qué depende de protocolos externos. El consumidor no debe repetir condiciones que
ya fueron establecidas y siguen siendo válidas.
La sintaxis exploratoria no debe convertirse accidentalmente en diseño aprobado. Tampoco debe atribuirse
originalidad a ideas con antecedentes ni prometer costo cero, exactitud financiera automática o ejecución
exactamente una vez por incorporar tipos o funciones puras.

21 Referencias técnicas del análisis
Las referencias permiten rastrear las propiedades técnicas discutidas. Las tablas de propuestas y las
recomendaciones arquitectónicas son razonamiento de diseño, no conclusiones atribuidas a estas fuentes.
[1] WG14. N1570, borrador de comité de C11, 12 de abril de 2011. Referencia para máquina abstracta, tipos,
almacenamiento y comportamiento indefinido. No se presenta como el estándar más reciente de C.
www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
[2] Haskell.org. Presentación del lenguaje, pureza, inmutabilidad y evaluación perezosa.
www.haskell.org/
[3] Haskell 2010 Language Report. Capítulo 1, introducción y características del lenguaje.
www.haskell.org/onlinereport/haskell2010/haskellch1.html
[4] IBM Enterprise COBOL for z/OS 6.5. Intermediate results and arithmetic precision, y Programming Guide.
Referencias a reglas de precisión de una implementación concreta.
www.ibm.com/docs/en/cobol-zos/6.5.0
www.ibm.com/docs/en/SS6SG3_6.5/pdf/pgmvs.pdf
[5] Haskell 2010 Language Report. Capítulo 6, tipos y clases predefinidos, IO y IOError.
www.haskell.org/onlinereport/haskell2010/haskellch6.html
[6] Haskell 2010 Language Report. Capítulo 3, expresiones y errores.
www.haskell.org/onlinereport/haskell2010/haskellch3.html
[7] Bernardy y colaboradores. Linear Haskell Practical linearity in a higher order polymorphic language.
Antecedentes de tipos lineales, interfaces puras y protocolos de recursos.
arxiv.org/abs/1710.09756
[8] The Koka Programming Language. Documentación del lenguaje, efectos y gestión de memoria.
koka-lang.github.io/koka/doc/book.html




                                                                                                           Página 16
````

