# Guía inicial de diseño

Todavía no existe una herramienta que ejecute Traza. Los fragmentos siguientes describen la propuesta de sintaxis 0.1.

## Respuesta validada

Ver [bounded.traza](../ejemplos/contratos/bounded.traza). Una entrada general Number no acredita el intervalo 0..100. El contrato desconocido se comprueba antes de entregar Ok; si falla, se obtiene Err(ContractViolation).

## Composición
Un consumidor puede utilizar las garantías de un Ok validado sin repetir validación manual cuando éstas impliquen su precondición. Una transformación puede perderlas. El operador ? propaga Err desde la función contenedora compatible; un Err ordinario sigue siendo un valor.

## Números y efectos
Number representa decimales finitos exactos. Las divisiones inexactas y los redondeos necesitan la política del documento 03. La entrada/salida necesita efectos declarados y capacidades concedidas.

Consultar el índice para reglas completas. Esta guía no fija terminación general, formato externo, interfaz binaria ni unidad de longitud de Text.
