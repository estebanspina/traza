# 08 · Evaluación y evolución

Estado: propuesta 0.1, anterior al nombre Traza.

Transcripción textual íntegra del PDF `08-evaluacion-evolucion.pdf`. Se conservan los saltos de línea y la disposición de tablas y código en bloques de texto para evitar una conversión Markdown que cambie su significado. Pendiente de normalización editorial y cotejo con el PDF original; no se incorpora aquí el archivo PDF binario.

Para el índice vigente de la serie y sus cambios, consultar [el índice documental](../readme.md).

## Página 1

````text
 Evaluación y evolución del lenguaje
 Documento 08 · Propuesta 0.1
 Lenguaje funcional en diseño · 20 de octubre de 2026

 Propósito
 Definir cómo evaluar el prototipo, contrastar las hipótesis del lenguaje y decidir cambios con
 evidencia. Este documento cierra la serie documental inicial y conecta los casos de conformidad
 del 05, la arquitectura del 06 y el plan de implementación del 07.

 Resultado que se quiere demostrar
 Que las respuestas con garantías reducen validaciones manuales repetidas sin permitir éxitos
 inválidos, sin ocultar errores y con costos observables. Que los tipos generales permiten expresar
 los programas objetivo y que la especialización física, cuando se proponga, aporta beneficios
 medibles conservando el significado.

 Lo que no constituye evidencia suficiente
 Un ejemplo correcto, un porcentaje aislado de pruebas o un benchmark favorable no demuestra
 seguridad general, facilidad de uso ni superioridad del lenguaje. La combinación de ideas tampoco
 prueba originalidad. Cada afirmación deberá delimitar el corpus, la implementación, las
 condiciones y el resultado observado.

 Base conservada
 Evaluación estricta de izquierda a derecha, inmutabilidad, funciones con resultados tipados,
 contratos explícitos y comprobables, errores Result, efectos declarados y Number decimal exacto.
 Los tipos de negocio no pasan al núcleo por conveniencia de una aplicación.

 Alcance
 Se proponen doce reglas de evaluación y evolución, EV01 a EV12, seis experimentos E01 a E06 y
 cuatro puertas de decisión. Son un protocolo futuro; no se presentan mediciones ni pruebas de una
 implementación que todavía no existe.

 Autoridad documental
 Documentos 01 a 07 de esta serie, propuestas 0.1. Los requisitos semánticos se modifican
 mediante una decisión explícita y actualización de sus pruebas. La arquitectura y la elección del
 anfitrión pueden evolucionar sin cambiar el lenguaje cuando preservan sus resultados observables.




Documento 08 · Propuesta 0.1 · 20 de octubre de 2026                                                  1
````

## Página 2

````text
 1. Hipótesis y evidencia

   Hipótesis                             Evidencia buscada                        Qué la debilita

                                         Una validación establece hechos útiles   Revalidaciones manuales
   H1: garantías reutilizables
                                         para consumidores posteriores.           exigidas sin nueva frontera.

                                         Violaciones producen rechazo o Err
   H2: fallos visibles                                                            Éxitos inválidos o fallos ocultos.
                                         declarado según la fase.

                                         Programas objetivo sin tipos de          Complejidad que impide
   H3: tipos generales suficientes
                                         negocio incorporados.                    expresar requisitos esenciales.

                                         Controles y exactitud con perfiles       Crecimiento incompatible con
   H4: costos controlables
                                         reproducibles.                           los presupuestos objetivo.

                                         Usuarios predicen fase y resultado y     Confusión persistente entre
   H5: modelo comprensible
                                         corrigen errores.                        Err, ? y contrato.



 EV01 · Afirmaciones acotadas
 Cada conclusión identifica hipótesis, versión de la especificación, revisión del ejecutor, corpus y
 límites. Una hipótesis puede quedar apoyada, contradicha o inconclusa. No se convierte una
 ausencia de fallos encontrados en demostración universal de corrección.

 EV02 · Corrección antes de agregación
 Un éxito que viola un contrato, un control eliminado sin prueba o una alteración del redondeo
 bloquean la aceptación del alcance afectado. No compensar esos defectos con mejores tiempos,
 menos líneas o buena experiencia de uso.

 Referencias de comparación
 Usar C, COBOL y Haskell como referencias de diseño y, cuando haya implementaciones de los
 ejercicios, como comparadores delimitados. No asignar ganadores por reputación ni confundir el
 costo del intérprete en Python con el de una implementación nativa futura.

 Preguntas del abogado del diablo
 ¿La garantía se conserva porque fue demostrada o porque el caso no la ejercitó? ¿El programa
 evita validaciones o las desplazó a otra biblioteca? ¿El costo procede de la semántica, del
 intérprete o de una decisión de representación? El informe debe responder estas preguntas antes
 de recomendar cambios.




Documento 08 · Propuesta 0.1 · 20 de octubre de 2026                                                               2
````

## Página 3

````text
 2. Corpus y comparación justa
 EV03 · Misma tarea y mismo significado
 Especificar entrada, dominio, precisión, redondeo, salida y política de fallos antes de escribir
 versiones comparables. Las implementaciones pueden ser idiomáticas, pero deben satisfacer el
 mismo contrato externo. Cuando una versión omita una garantía, reportarla como variante de
 alcance distinto.

   Familia de ejercicios                 Variantes obligatorias                  Aspecto observado

                                         Entrada válida, inválida y garantía     Fronteras y reutilización de
   Validar y componer funciones
                                         más fuerte.                             pruebas.

                                         Empates, signos, división inexacta y
   Cálculo decimal                                                               Exactitud y política de error.
                                         cero.

                                         Vacío, datos grandes y error
   Transformar registros y listas                                                Expresividad y memoria.
                                         intermedio.

                                         Adaptador simulado, error y autoridad
   Procesar entrada/salida                                                       Efectos y recursos.
                                         ausente.



 Dos clases de comparación
 La comparación semántica usa adaptaciones que igualan el contrato externo, incluso si requieren
 bibliotecas o validaciones adicionales. Una comparación de configuraciones habituales puede ser
 informativa, pero declara sus diferencias y no respalda por sí sola una afirmación de equivalencia o
 superioridad.

 Preparación
 Publicar los ejercicios, casos adversos, semillas y resultados esperados. Separar un conjunto de
 desarrollo y otro reservado para evaluación; cualquier caso reservado usado para corregir el diseño
 pasa a ser parte del conjunto de desarrollo en la siguiente ronda. Conservar sus regresiones.

 Costos que deben incluirse
 Contar validación inicial, construcción y conversión de datos, errores y formato cuando formen
 parte de la tarea. Medir el núcleo de cálculo por separado si se desea, identificándolo como otra
 métrica. No excluir sólo de una versión el trabajo que garantiza el contrato.

 Límite actual
 No hay comparadores implementados ni relevamiento bibliográfico de originalidad en esta entrega.
 Las versiones concretas de compiladores y bibliotecas se fijarán y verificarán al preparar cada
 experimento, sin inferir resultados a partir de esta propuesta.




Documento 08 · Propuesta 0.1 · 20 de octubre de 2026                                                              3
````

## Página 4

````text
 3. Métricas e interpretación

   Métrica                               Definición operativa                    Límite de interpretación

                                         Casos y variantes aprobados sobre los   No demuestra corrección
   Conformidad
                                         exigidos, con estados separados.        universal.

                                         Obligaciones demostradas; controles     No equivalen a instrucciones
   Controles estáticos y dinámicos
                                         elaborados y ejecutados.                máquina.

                                         Sitios escritos por el usuario para     Menos sitios no implica mejor
   Validación manual
                                         establecer o recuperar garantías.       comprensión.

                                         Comprobación, ejecución y extremo a     Depende de entorno y
   Tiempo
                                         extremo por separado.                   tamaños.

                                         Pico del proceso y asignaciones si      No es tamaño aislado de los
   Memoria
                                         pueden medirse.                         valores.

                                         Predicciones correctas y tareas         Depende de experiencia y
   Comprensión
                                         completadas con ayuda registrada.       corpus.



 EV04 · Denominadores visibles
 Publicar el número de casos principales, variantes exigidas y estados por separado. CF01 a CF40
 son cuarenta identificadores, no necesariamente cuarenta ejecuciones. No sumar bloqueados,
 omitidos o inconclusos a aprobados ni excluirlos silenciosamente del total previsto.

 EV05 · Medir costos completos
 Comparar la misma máquina y configuración cuando corresponda; registrar versiones,
 optimizaciones, límites, carga y estado de trazas. Separar arranque, preparación, compilación o
 comprobación y ejecución. Si hay calentamiento del entorno, declarar su procedimiento.

 Repetir por proceso y variar el orden de los comparadores. Publicar cantidad de repeticiones,
 mediana y dispersión; conservar resultados individuales. Para percentiles, indicar método y
 tamaño de muestra. No extraer conclusiones fuertes de diferencias menores que la variabilidad
 observada.

 Ciclos y memoria
 Si se miden ciclos, registrar disponibilidad del contador, configuración y unidades; no convertir
 segundos a ciclos con una frecuencia nominal sin justificarlo. Si sólo se dispone de memoria total
 del proceso, decirlo: no atribuirla enteramente a Number o a los contratos.

 Umbrales
 Antes de cada campaña, fijar presupuestos de la tarea y diferencia mínima relevante. Esta
 propuesta no inventa un porcentaje universal de mejora. Los umbrales deben preceder a los
 resultados y no ajustarse después para favorecer una alternativa.




Documento 08 · Propuesta 0.1 · 20 de octubre de 2026                                                             4
````

## Página 5

````text
 4. Experimentos funcionales
 E01 · Frontera y composición
 Ejecutar bounded con entradas válidas y fuera del intervalo; encadenar pipeline y consumidores de
 garantías más débiles. Añadir el caso que exige una garantía más fuerte y el caso que transforma
 el valor. Base: CF01–10; paquetes PI08, PI11 y PI13–14.

 Aprobación: no escapa Ok inválido; el retorno conocido imposible se rechaza; el consumidor
 aprovecha la garantía demostrada; check explícito establece la propiedad más fuerte. Conservar
 fuente, obligación, elaboración, control ejecutado y valor. No deducir controles eliminados mirando
 únicamente el resultado final.

 E02 · Control y errores
 Ejecutar CF11–15 y variantes de anidamiento. Observar llamadas, ramas y propagación con
 instrumentación de prueba. Forzar un fallo del proceso con la sonda del arnés, conservando la
 separación respecto de Err y de ?.

 Aprobación: argumentos en orden; Err ordinario permite continuar; ? abandona la función
 adecuada; la rama descartada y el argumento posterior al fallo fatal no comienzan. Un tiempo
 límite aislado no prueba que un tramo no fue evaluado.

 E03 · Exactitud y fronteras numéricas
 Ejecutar CF16–36 y prioridades de múltiples argumentos inválidos. Comparar con referencia
 racional independiente. Incluir coeficientes grandes, exponentes extremos bajo presupuesto,
 signos y todos los modos de redondeo.

 Aprobación: igualdad exacta de valores y errores; serialización reproducible; formateo sin
 redondeo implícito; ausencia de transformación que mueva el redondeo. Un agotamiento externo
 se registra como tal y no como InexactResult.

 EV06 · Regresiones y pruebas adversas
 Todo defecto reproducible agrega un caso que falla antes de la corrección y pasa después. La
 revisión debe preguntar si el caso prueba la regla o sólo la forma particular de la implementación.
 Usar propiedades y pruebas de fase para evitar depender exclusivamente de programas
 completos.

 Estado
 E01–E03 están definidos y pendientes de ejecución sobre el prototipo. La conformidad del
 documento 05 y las ampliaciones del 07 siguen siendo obligatorias para el alcance declarado;
 estos experimentos no las sustituyen.




Documento 08 · Propuesta 0.1 · 20 de octubre de 2026                                                   5
````

## Página 6

````text
 5. Experimentos de costo y uso
 E04 · Costo de contratos
 Comparar tres versiones de la misma tarea dentro del prototipo: garantía demostrada
 estáticamente; garantía desconocida validada en retorno; validación explícita escrita por el usuario
 cuando sea necesaria. Mantener iguales valores, errores y frontera externa. Si la diferencia de
 dominio impide igualarlas, reportar el límite y no presentar una equivalencia falsa.

 Registrar obligaciones, controles elaborados y ejecutados, tiempo de comprobación, ejecución y
 memoria. Las pruebas instrumentadas verifican la estructura; las mediciones de rendimiento usan
 trazas desactivadas. El modo de auditoría constituye una configuración distinta.

 E05 · Representación especializada
 Comparar la representación exacta de referencia con una candidata para el mismo dominio
 probado. Medir conversiones, detección de límites y rutas de respaldo además del caso rápido.
 Repetir con entradas pequeñas, grandes y cercanas al límite.

 Una candidata que no representa un valor debe usar una estrategia exacta compatible o una
 conversión explícita ya prevista. No puede introducir un desbordamiento nuevo en operaciones
 generales Number. Especializar almacenamiento interno no obliga a agregar un tipo visible.

 E06 · Comprensión y mantenimiento
 Dar tareas breves de predicción, escritura y corrección: distinguir Err de ?, decidir si un consumidor
 necesita check y reparar un error de contrato. Registrar experiencia previa, ayudas, tiempo y
 resultado. Alternar el orden de variantes cuando participen varias personas para reducir el efecto
 del aprendizaje.

 Con un único participante, presentar el resultado como estudio exploratorio y conservar ejemplos
 de confusión. Medir líneas sólo como dato auxiliar; observar también cambios necesarios cuando
 una garantía se fortalece y claridad de diagnósticos.

 EV07 · Condición de especialización
 Una propuesta de especialización requiere necesidad concreta, dominio, evidencia de ciclos o
 memoria, preservación semántica, pruebas de límites y costo de mantenimiento. Sin evidencia
 suficiente, queda experimental. La conveniencia de nombrar un concepto de negocio no basta para
 incorporarlo al núcleo.

 EV08 · Costos de comprensión
 Un diseño más difícil de explicar exige revisar mensajes, sintaxis o alcance del subconjunto. No se
 rebaja una garantía para mejorar una métrica de facilidad sin una decisión semántica explícita.




Documento 08 · Propuesta 0.1 · 20 de octubre de 2026                                                      6
````

## Página 7

````text
 6. Decisiones y versionado
 EV09 · Propuesta de cambio revisable
 Cada propuesta identifica problema reproducible, alternativas, regla afectada, ejemplos antes y
 después, impacto en compatibilidad, pruebas, costos y condición de reversión. Un cambio del
 backend que conserva significado se clasifica como implementación; cambiar valores, errores,
 efectos u obligaciones es un cambio semántico.

   Estado                                Evidencia necesaria                   Salida posible

                                         Problema, alternativas y pruebas      Rechazar, pedir datos o
   Propuesta
                                         previstas.                            experimentar.

                                         Implementación aislada y resultados
   Experimental                                                                Corregir, retirar o recomendar.
                                         acotados.

                                         Reglas y pruebas actualizadas;
   Aceptada                                                                    Integrar con versión explícita.
                                         impacto revisado.

                                         Motivo, alcance y migración cuando    Conservar historial y
   Sustituida o retirada
                                         corresponda.                          regresiones útiles.



 EV10 · Compatibilidad explícita
 Registrar por separado versión de especificación, revisión de implementación, versión de catálogo
 y esquema de informes. Mientras la serie sea propuesta 0.1, no prometer estabilidad que aún no se
 ha definido; aun así, todo cambio incompatible se documenta.

 No reutilizar un identificador de regla para afirmar una conducta opuesta sin indicar revisión. Las
 rutas, posiciones y condition_id tienen la estabilidad acotada por A11. El formato público de los
 informes no debe depender accidentalmente de la representación interna del árbol.

 Aceptación
 La persona responsable del lenguaje decide cambios de semántica con evidencia de desarrollo y
 revisión. Si una persona cubre varios roles, conserva la justificación para revisión posterior. Las
 propuestas no resueltas mantienen el estado experimental; el silencio no significa aceptación.

 Migración y reversión
 Para cambios incompatibles, incluir cómo detectar programas afectados y qué modificación deben
 realizar. Mantener una versión de referencia para reproducir resultados anteriores. Si una
 optimización resulta incorrecta, desactivarla y recuperar la ruta correcta sin modificar los
 resultados esperados para esconder la regresión.




Documento 08 · Propuesta 0.1 · 20 de octubre de 2026                                                             7
````

## Página 8

````text
 7. Puertas de decisión

   Puerta                                Condición necesaria                     Decisión permitida

                                         Frontera completa, éxito válido y
   G1: demostración D0                                                           Ampliar tipos y control.
                                         violación declarada.

                                         P2–P3 y batería aplicable sin éxitos    Evaluar tareas y costos del
   G2: núcleo evaluable
                                         inválidos.                              núcleo.

                                         P4–P5, alcance publicado y              Publicar versión experimental
   G3: prototipo de referencia
                                         reproducción limpia.                    delimitada.

                                         Hipótesis y evidencia de la función o   Aceptar, experimentar más o
   G4: ampliación
                                         backend candidato.                      rechazar.



 Alcance de las puertas
 G1–G4 son decisiones de evaluación, no reemplazos de P1–P5. G2 permite estudios parciales
 declarados; no acredita aritmética completa ni capacidades reales ausentes. G3 exige resultados
 aprobados para todos los requisitos del alcance publicado y una lista visible de lo no soportado.

 EV11 · Bloqueadores
 Bloquear la aceptación del alcance afectado ante garantías falsas, divergencia entre núcleo y
 backend, redondeo alterado, errores ocultos o imposibilidad de reproducir un resultado usado
 como evidencia decisiva. Un defecto localizado puede permitir seguir investigando otras áreas,
 pero no aprobar la función defectuosa.

 Qué no promete G3
 Publicar un prototipo experimental no declara preparación para producción, tiempos de respuesta
 garantizados, aislamiento de programas hostiles ni superioridad frente a otros lenguajes. Esas
 afirmaciones requieren objetivos y evaluaciones adicionales.

 EV12 · Originalidad con evidencia
 Describir con precisión la combinación propuesta y sus diferencias observables. Antes de afirmar
 novedad, realizar una revisión de antecedentes con fuentes verificadas y contrastar mecanismos
 equivalentes, incluidos contratos, refinamientos, efectos y representaciones numéricas. Esta
 revisión no se ha realizado aquí.

 Decidir detenerse
 Si el costo o la complejidad no justifican un mecanismo, reducir el alcance experimental, conservar
 el resultado y revisar la hipótesis. Un experimento que contradice una elección es útil; no requiere
 inventar nuevas características para justificarla.




Documento 08 · Propuesta 0.1 · 20 de octubre de 2026                                                             8
````

## Página 9

````text
 8. Informe y cierre documental
 Ficha de evaluación
 Experimento y pregunta:
 Versiones: especificación, ejecutor, catálogo e informe
 Corpus, entradas y resultados esperados:
 Configuración, límites y procedimiento:
 Casos aprobados, fallidos, omitidos, bloqueados e inconclusos:
 Mediciones individuales y resumen:
 Defectos, amenazas a la interpretación y alcance:
 Conclusión: apoyada, contradicha o inconclusa
 Decisión, responsable y condición de reconsideración:

 La ficha es un formato de contenido propuesto, no el esquema de intercambio definitivo del arnés.
 Los archivos de resultados y los comandos de reproducción acompañarán el informe cuando exista
 una implementación.

 Relación con la construcción
 PI02 mantiene el catálogo de reglas y casos. PI11 y PI13 aportan evidencia de contratos. PI14 y
 PI19 aportan control y límites. PI15–16 aportan exactitud y oráculos. PI18 genera informes y PI20
 prepara reproducción y perfiles. E01–E06 usan esas salidas sin declarar terminados paquetes
 pendientes.

 Estado real de esta edición
 Se definieron doce reglas EV, seis experimentos y cuatro puertas de decisión; se revisó su
 consistencia con la arquitectura y el plan y se verificó la presentación del PDF. No se ejecutaron
 experimentos, comparadores ni estudios de usuarios. Tampoco se demostró originalidad o
 rendimiento del lenguaje.

 Cierre de la serie inicial
 Los documentos 01–04 especifican el núcleo; el 05 fija casos de conformidad; el 06 propone la
 arquitectura; el 07 organiza la construcción; el 08 establece cómo evaluar resultados y controlar su
 evolución. Los pendientes expresos siguen abiertos y deben resolverse antes de habilitar las
 capacidades que dependen de ellos.

 Punto de revisión
 Esta entrega queda para aprobación o corrección. Tras revisar el conjunto documental, el paso
 previsto es iniciar PI01–PI02 y preparar la demostración D0. Crear estos documentos no constituye
 autorización para publicar, desplegar ni afirmar que el prototipo está construido. La
 implementación se iniciará cuando se solicite ese trabajo.




Documento 08 · Propuesta 0.1 · 20 de octubre de 2026                                                    9
````

