# Pruebas de Traza

```sh
python herramientas/verificar.py
python herramientas/probar_d0.py
```

El primer comando descubre todas las pruebas: infraestructura, catálogo, lexer, parser, comprobación, máquina e interfaz. El segundo ejecuta explícitamente el manifiesto D0 y emite resultados JSON.

La aceptación léxica no implica aceptación sintáctica; la aceptación sintáctica no implica soporte de ejecución. NI01 significa capacidad no implementada, no aprobación del programa.

El catálogo CF01–CF40 conserva expectativas y metadatos de preparación. Los resultados reales se publican en informes separados; cobertura.json delimita el arnés D0. Aprobar D0 no aprueba automáticamente la batería completa.

Las pruebas incluyen exactitud decimal mínima, garantías, precondiciones, rechazo de retornos imposibles, propagación, orden, ramas descartadas, límites externos y pila explícita.
