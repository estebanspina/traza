# Analizador léxico · PI03 inicial

Implementa G01–G05: UTF-8 estricto, LF/CRLF, identificadores ASCII, reservadas, comentario //, máxima longitud, números exactos como texto, escapes escalares y bytes hexadecimales.

```sh
python herramientas/traza.py tokens ejemplos/contratos/bounded.traza
python herramientas/verificar.py
```

La primera orden muestra tokens JSON con rangos de bytes y posiciones de línea/columna. La segunda ejecuta pruebas de infraestructura, catálogo, lexer e interfaz. Puede usarse la API desde fuente/traza/analisis o el módulo traza con fuente en PYTHONPATH.

El lexer no verifica delimitadores, precedencia, nombres, contratos ni tipos. Todos los casos CF semánticos siguen pendientes, incluso si sus fuentes se tokenizan. PI03 continúa abierto para completar integración de fases y límites; PI04 no está iniciado.

Ver ADR 0003 para decisiones de frontera, errores, unidades y números mal formados.
