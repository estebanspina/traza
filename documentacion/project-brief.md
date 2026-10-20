> Documento histórico, versión 1.0. El nombre vigente es Traza; el estado y alcance actuales están en el README raíz y el índice documental. El contenido original se conserva debajo.

# Project Brief — Nuevo lenguaje de programación funcional

| Campo | Valor |
| --- | --- |
| Versión del brief | 1.0 |
| Fecha | 14 de octubre de 2026 |
| Documento de contexto | `contexto-lenguaje-funcional.docx`, versión documental 1.1 |
| Estado del proyecto | Diseño conceptual; sin implementación ni mediciones |
| Nombre del lenguaje | Por definir |
| Próximo entregable recomendado | Especificación semántica mínima y caso de liquidación |

## 1. Visión y objetivo

Crear un lenguaje funcional nuevo y original que combine la atención a recursos y representación de C, la precisión y los contratos de datos de COBOL, y la composición funcional e inmutabilidad de Haskell.

El lenguaje tendrá tipos generales y contratos de retorno comprobados. Una función deberá entregar resultados con condiciones verificadas para que el programador pueda consumirlos sin repetir validaciones que sigan siendo válidas.

La orientación propuesta es implementar reglas de negocio y procesamiento de datos con semántica numérica explícita, recursos controlados y resultados explicables. El público, el carácter general o especializado del lenguaje y su originalidad siguen pendientes de validación.

## 2. Problema que buscamos resolver

El diseño aborda cuatro dificultades identificadas en el análisis:

- La responsabilidad de controlar memoria, límites y conversiones puede introducir defectos difíciles de verificar.
- El formato físico de un registro no expresa por sí solo la validez de su contenido ni su significado.
- Un tipo general, como `Number`, no garantiza rango, finitud o representabilidad.
- La composición y abstracción pueden ocultar costos de ejecución, efectos o decisiones de redondeo.

La propuesta central es establecer garantías en las fronteras que producen valores, conservarlas durante su uso y restablecerlas únicamente cuando una transformación o frontera pueda invalidarlas. Esto debe reducir validaciones manuales repetidas sin ocultar fallos ni alterar la semántica.

## 3. Usuarios y caso inicial

**Hipótesis de usuarios:** equipos que desarrollan reglas financieras, integraciones y procesamiento de registros. Esta hipótesis no restringe todavía el lenguaje ni constituye evidencia de demanda.

**Caso conductor recomendado:** una liquidación que lee movimientos, valida registros, calcula comisiones y produce resultados. Debe permitir examinar datos inválidos, límites numéricos, redondeo, consumo de memoria y fallos de escritura.

La liquidación sirve como experimento de diseño. Sus reglas concretas, formatos y políticas todavía deben especificarse; los ejemplos existentes son conceptuales.

## 4. Decisiones establecidas y propuestas

| Elemento | Dirección | Estado |
| --- | --- | --- |
| Objetivo | Crear un lenguaje funcional nuevo y original | Establecido por el usuario |
| Método | Comparación crítica de C, COBOL y Haskell con enfoque de abogado del diablo | Establecido por el usuario |
| Tipos | Generales; especializaciones solo si favorecen ejecución o memoria | Establecido por el usuario |
| Retornos | Resultados tipados para evitar repetir validaciones | Dirección establecida por el usuario |
| Garantías | Restricciones sobre el tipo base, demostradas estáticamente o comprobadas al retornar | Recomendación incorporada al contexto |
| Dominio inicial | Reglas de negocio y procesamiento de registros | Propuesto |
| Evaluación | Estricta por defecto y con orden definido | Propuesto |
| Datos | Inmutables por defecto, con mutación interna encapsulada | Propuesto |
| Implementación inicial | Intérprete pequeño de referencia | Recomendado |

Los requisitos siguientes expresan el diseño buscado. No describen capacidades ya implementadas.

## 5. Principios de diseño

| Principio | Consecuencia para el proyecto |
| --- | --- |
| Composición funcional | Las reglas se expresan como transformaciones de valores y funciones como valores |
| Tipos generales | Evitar familias nominales de negocio como `Money` o `Rate` |
| Garantías reutilizables | Conservar las condiciones verificadas del resultado exitoso |
| Semántica numérica explícita | Definir rango, exactitud, desbordamiento y redondeo |
| Efectos visibles | Separar cálculo puro de archivos, red, reloj y otros servicios |
| Recursos controlados | Definir duración, propiedad y fronteras inseguras |
| Representación independiente | Separar esquemas externos de estructuras internas |
| Optimización comprobable | Preservar resultados, errores y políticas; medir ventajas |
| Legibilidad | Permitir comprender reglas habituales sin teoría avanzada de tipos |

Una restricción lógica sobre `Number` no implica una representación física especializada. La especialización por rendimiento o memoria debe justificarse con evidencia.

## 6. Requisitos del lenguaje

### 6.1. Funciones, evaluación y estructuras

- Funciones puras, composición y funciones como valores.
- Evaluación estricta por defecto, con orden definido; diferimiento explícito cuando corresponda.
- Valores inmutables por defecto.
- Registros, colecciones y variantes generales.
- Coincidencia de patrones con comprobación de exhaustividad.
- Tipado estático, inferencia local y firmas explícitas en interfaces públicas como dirección propuesta.

La mutación interna solo será admisible si preserva el comportamiento observable. La primera versión no intentará demostrar la terminación de todas las funciones.

### 6.2. Contratos de retorno y conservación de garantías

Una función podrá declarar el tipo general de su resultado y las condiciones que cumple el caso exitoso. Sintaxis exploratoria:

```text
fn porcentaje(valor: Number)
    -> Result<Number where 0 <= value <= 100, Error>
{
    ...
}
```

`value` representa el resultado exitoso. El fragmento no define una gramática definitiva ni es código ejecutable.

| Frontera | Comportamiento requerido |
| --- | --- |
| Entrada externa | Comprobar datos que no tienen garantías |
| Retorno de función | Demostrar el contrato o comprobarlo antes de entregar éxito |
| Consumo del éxito | Mantener las restricciones sin repetir su validación |
| Composición | Reutilizar garantías que satisfagan los requisitos de la siguiente función |
| Transformación | Demostrar o comprobar las condiciones de su nuevo resultado |
| Frontera insegura | Restablecer las garantías que pueda invalidar |

Las condiciones comprobadas en ejecución deberán ser puras y tener reglas de terminación y fallo definidas. El subconjunto inicial recomendado comprende restricciones simples, como intervalos y propiedades estructurales.

Multiplicar por dos un valor entre 0 y 100 no conserva ese intervalo. Haber comprobado un saldo o la existencia de un archivo tampoco garantiza su vigencia futura. Las garantías sobre estado externo necesitan una instantánea, transacción o protocolo definido.

### 6.3. Errores y ausencia

- Representar ausencia mediante un mecanismo general como `Option`.
- Representar fallos esperables mediante un mecanismo general como `Result`.
- Impedir que se entregue como exitoso un valor que incumple su contrato.
- Proporcionar diagnósticos que identifiquen función, condición y punto de comprobación.

El consumidor debe manejar o propagar el fallo. Esto es distinto de volver a validar el valor exitoso. La política exacta para errores de contrato y fallos del proceso queda abierta.

### 6.4. Modelo numérico

`Number` es una categoría conceptual; su representación y reglas definitivas están pendientes.

- Definir rangos, precisión intermedia y exactitud.
- Evitar convertir primero a flotante binario los literales que deban conservar semántica decimal.
- Exigir política explícita al reducir escala.
- Definir precisión o política de salida para divisiones no representables.
- Evitar desbordamiento con envolvimiento silencioso en operaciones ordinarias.
- Mantener conversiones de moneda como operaciones explícitas de negocio.

Entero, decimal y flotante pueden producir resultados distintos aun con tamaños similares. La simplificación de tipos no elimina esa diferencia. Debe resolverse si se expresa mediante tipos generales diferenciados, representaciones o contextos de operación.

Redondear una suma puede diferir de sumar valores previamente redondeados. Las optimizaciones deben respetar esta diferencia y las condiciones de desbordamiento.

### 6.5. Formatos, efectos y recursos

- Decodificar y codificar mediante esquemas externos definidos.
- Conservar en el contrato del registro exitoso las propiedades comprobadas por el esquema.
- Distinguir equivalencia semántica e identidad binaria; esta última puede exigir conservar información adicional.
- Declarar efectos y diferenciar sus permisos sobre recursos mediante capacidades cuando corresponda.
- Definir duración de recursos y una frontera restringida para interoperabilidad nativa.

El sistema de efectos no sustituye protocolos de transacción, idempotencia o recuperación.

## 7. Alcance inicial recomendado

La primera versión experimental incluiría:

1. Un subconjunto funcional con evaluación estricta.
2. Tipos generales, registros, colecciones y variantes.
3. Contratos de retorno simples y conservación de garantías.
4. Comprobaciones estáticas y comprobaciones en ejecución cuando sean necesarias.
5. Patrones exhaustivos, `Option` y `Result`.
6. Semántica numérica definida para el caso inicial.
7. Una familia limitada de esquemas externos.
8. Procesamiento secuencial de registros y efectos mínimos de entrada y salida.
9. Intérprete de referencia y diagnósticos.
10. Pruebas de conformidad y casos negativos.

Se recomienda diferir concurrencia distribuida, metaprogramación avanzada, demostración general de terminación y múltiples estrategias de memoria. El compilador completo no es el primer entregable recomendado.

Las pruebas de paralelismo y recuperación identificadas en el contexto pertenecen a fases que incorporen esas capacidades; no amplían automáticamente el alcance inicial.

## 8. Entregables y secuencia propuesta

| Fase | Entregable | Condición para avanzar |
| --- | --- | --- |
| Definición | Especificación semántica mínima y decisiones registradas | Reglas de evaluación, tipos, contratos, números y fallos sin ambigüedades centrales |
| Caso conductor | Liquidación con entradas, políticas y resultados esperados | Casos válidos e inválidos definidos |
| Prototipo | Intérprete de referencia del subconjunto | Ejecuta el caso y aplica los contratos especificados |
| Conformidad | Suite positiva y negativa con diagnósticos | No entrega éxitos inválidos y conserva garantías reutilizables |
| Evaluación | Informe comparativo de costos y alternativas | Mediciones equivalentes y diferenciación sustentada |

Esta secuencia organiza las recomendaciones del contexto. No fija plazos, presupuesto, responsables ni tecnología de implementación.

## 9. Criterios de éxito y validación

| Criterio | Evidencia requerida |
| --- | --- |
| Retornos válidos | Todo éxito del conjunto de pruebas cumple su contrato |
| Fallos visibles | Incumplimientos rechazados estáticamente o antes de entregar éxito |
| Garantías conservadas | Consumidores usan condiciones establecidas sin repetir su validación |
| Transformaciones seguras | Cambios que rompen condiciones generan nuevas obligaciones o diagnósticos |
| Semántica numérica | Resultados y fallos conformes a las políticas de rango y redondeo |
| Formatos seguros | Registros corruptos no producen valores exitosos válidos |
| Recursos | Usos inválidos rechazados o protegidos según el modelo definido |
| Rendimiento evaluable | Medición de ciclos, tiempo, asignaciones y memoria con validaciones equivalentes |
| Legibilidad | Evaluación de comprensión y resolución de errores por desarrolladores |
| Diferenciación | Comparación documentada con alternativas y antecedentes |

No existen todavía resultados, umbrales de rendimiento ni objetivos cuantitativos de adopción. Deben definirse antes de usar estas métricas como criterios de aprobación.

## 10. Riesgos y respuesta de diseño

| Riesgo | Respuesta propuesta |
| --- | --- |
| Tipos y contratos demasiado complejos | Mantener tipos generales y empezar con restricciones simples |
| Condiciones imposibles de demostrar | Definir límites del comprobador y controles en ejecución |
| Costos ocultos de validación | Medir comprobaciones restantes y eliminación de redundancias |
| Garantías desactualizadas | Distinguir valores inmutables de estado externo mutable |
| Resultados cambiados por optimización | Exigir equivalencia semántica y pruebas de conformidad |
| Alcance excesivo | Validar un intérprete y un caso antes de ampliar capacidades |
| Originalidad insuficiente | Contrastar biblioteca, DSL y lenguaje independiente |
| Dificultad de adopción | Evaluar legibilidad, diagnósticos y costo de herramientas |

No se promete costo cero, corrección financiera automática, terminación general ni ejecución exactamente una vez por incorporar pureza o contratos.

## 11. Responsabilidades arquitectónicas

| Capa | Responsabilidad |
| --- | --- |
| Lenguaje | Evaluación, tipos, pureza y contratos |
| Comprobador | Demostrar condiciones y determinar obligaciones pendientes |
| Biblioteca y semántica | Operaciones numéricas, estructuras y esquemas |
| Runtime | Ejecutar comprobaciones pendientes y gestionar recursos |
| Plataforma de procesamiento | Checkpoints, reintentos y publicación cuando se incorporen |
| Aplicación y protocolos | Idempotencia y vigencia de estado externo |
| Herramientas y operación | Versiones, entradas y políticas para explicar resultados |

La plataforma de procesos puede integrarse con el lenguaje sin incorporar todas sus responsabilidades a la sintaxis.

## 12. Decisiones abiertas

- Público inicial y alcance general o especializado.
- Categorías finales de tipos y mecanismo de especialización por costo o memoria.
- Sintaxis y subconjunto de restricciones de retorno.
- Propagación de garantías entre funciones y módulos.
- Modelo numérico, representación, precisión y contexto de operación.
- Política de fallos de contrato, errores de proceso y propagación.
- Modelo de propiedad, memoria, recursos y fronteras nativas.
- Sistema de efectos y capacidades.
- Esquemas iniciales y reglas de versionado.
- Información de auditoría que se conserva y forma de explicarla.
- Nombre, gramática y plataforma de implementación.
- Originalidad frente a antecedentes y justificación de un lenguaje independiente.
- Responsables, presupuesto, plazos y umbrales de evaluación.

## 13. Base documental y antecedentes

Este brief deriva de **Contexto para diseñar un nuevo lenguaje funcional**, versión documental **1.1**, especialmente de las secciones 1, 9 y 11 a 20. Las propuestas permanecen sujetas a especificación y validación.

Los antecedentes técnicos registrados en ese documento incluyen:

- [WG14 N1570 — borrador de C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).
- [Haskell 2010 Language Report](https://www.haskell.org/onlinereport/haskell2010/).
- [IBM Enterprise COBOL — precisión de resultados intermedios](https://www.ibm.com/docs/en/cobol-zos/6.5.0?topic=appendixes-intermediate-results-arithmetic-precision).
- [Linear Haskell](https://arxiv.org/abs/1710.09756).
- [Koka](https://koka-lang.github.io/koka/doc/book.html).

La hipótesis de diferenciación consiste en integrar tipos generales, contratos de retorno comprobados, semántica numérica explícita, formatos externos y efectos en un diseño funcional coherente. Esa integración no se presenta como originalidad demostrada.
