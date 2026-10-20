# ADR 0003 · Frontera léxica y posiciones

Fecha: 20 de octubre de 2026.
Estado: decisión de implementación de G01–G05 y A04; PI03 inicial.

## API
analizar(bytes, archivo) devuelve una tupla de tokens inmutables o un ErrorLexico anfitrión con diagnóstico SG01. No es un Error ni una excepción pública de Traza. No se produce un árbol parcial ejecutable.

Los rangos son intervalos de bytes UTF-8 [inicio, fin). Líneas y columnas comienzan en 1; las columnas cuentan escalares, no bytes ni grafemas. LF y CRLF son válidos; CR aislado no. Una secuencia UTF-8 inválida conserva su rango binario y señala la columna de su inicio, pues no representa un escalar.

## Tokens
Las palabras reservadas usan su lexema como clase. Identificadores usan IDENT, números NUMBER, textos STRING, bytes BYTES y el comodín _. Los nombres predefinidos siguen siendo IDENT; resolución comprobará su redefinición.

NUMBER conserva el lexema completo como str sin conversión a float ni entero de precisión acotada. STRING conserva el lexema y un valor decodificado sin normalización. BYTES conserva octetos. EOF tiene rango vacío al final físico.

## Máxima longitud y fases
Se reconoce el token válido más largo. Fragmentos como 1e+, 1. o 1_000 se descomponen en tokens válidos; el futuro parser debe rechazar su uso como literal único cuando no forme una expresión. No se añade una regla de adyacencia ajena a la gramática. Un identificador b pegado a comillas inicia BYTES y un contenido inválido es SG01.

No se implementan comentarios de bloque, recuperación de múltiples errores, parser, tipos ni ejecución. La primera versión produce el primer error y exige fuente completa en memoria; los presupuestos de fuente y proceso se completarán con PI19.

## Interfaz
python herramientas/traza.py tokens archivo.traza produce JSON de tokens. Códigos de salida: 0 análisis léxico satisfactorio, 1 error léxico, 2 uso o lectura de archivo incorrectos. Este comando no garantiza aceptación sintáctica.
