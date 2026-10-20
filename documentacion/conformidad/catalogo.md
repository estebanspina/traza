# Catálogo de requisitos y casos

Estado de preparación: PI02. Los casos son expectativas, no resultados de ejecución.

- [Catálogo CF01–CF40](../../pruebas/conformidad/catalogo.json): cuarenta casos, con variantes, fase y oráculo.
- [Reglas S/T/N/G](reglas.json): 116 reglas, títulos y ubicación de origen.
- [Manifiesto D0](../../pruebas/conformidad/manifiestos/d0.json): subconjunto histórico de arranque.
- [Fuentes de programas](../../pruebas/conformidad/programas/).

## Modalidades
programa: archivo fuente y entrada cuando corresponde.
vector: operación numérica y argumentos etiquetados; Number siempre viaja como texto.
propiedad: generador reproducible y propiedad que verificará el arnés futuro.
protocolo: mecanismo de arnés o frontera externa; no se inventa sintaxis o API todavía no especificada.

Cada variante declara argumentos y resultado esperado. Todos los casos están pendientes; tokenizar sus programas no los aprueba semánticamente. CF33 mantiene pendiente el enlace de API de esquemas, conservando el protocolo y el resultado esperado.

## Trazabilidad
Las relaciones regla/caso indican cobertura prevista. Una regla sin caso directo se mantiene explícitamente sin cobertura; no equivale a requisito cumplido. Los escenarios históricos C, TC, MN y GR siguen en los documentos fuente y deben ampliar el arnés.

PI02 cierra la preparación de catálogo y fixtures, no la implementación de la batería ni todos los pendientes semánticos. La validación de integridad comprueba identificadores, rutas, fases, argumentos y referencias recíprocas.
