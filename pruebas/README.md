# Pruebas

```sh
python herramientas/verificar.py
```

## Infraestructura
Comprueba catálogo completo, rutas, reglas y expectativas de D0. No instala dependencias ni ejecuta programas Traza.

## Léxico
Prueba tokens, UTF-8 inválido, escapes, bytes, rangos, comentarios, máxima longitud e interfaz JSON. Los programas CF se tokenizan para validar su frontera léxica; esto no ejecuta sus expectativas.

## Conformidad
catalogo.json contiene CF01–CF40 con variantes; documentacion/conformidad/reglas.json contiene 116 reglas. d0.json mantiene el subconjunto de arranque. Todos los estados semánticos permanecen pendientes. La CI de lexer no los modifica.

Ver el catálogo documentado y ADR 0002 para modalidades, trazabilidad y protocolos pendientes de API externa.
