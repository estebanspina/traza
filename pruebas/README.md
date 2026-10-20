# Pruebas

## Infraestructura
`python -m unittest discover -s pruebas/infraestructura -v` valida los manifiestos iniciales, rutas y presencia documental. No analiza ni ejecuta Traza.

## Conformidad
El manifiesto d0.json contiene expectativas para CF01, CF02 y CF06 con una variante negativa de CF02. Todos están pendientes. No representa el catálogo completo CF01–CF40. El estado no cambia automáticamente por aprobar infraestructura.

La extensión .traza identifica fixtures provisionales y no fija un formato de paquete o ABI.

## Próximos pasos
Implementar pruebas de fase, arnés y oráculos independientes. Agregar regresiones ante defectos concretos y conservar semillas. No copiar algoritmos del núcleo como oráculo.
