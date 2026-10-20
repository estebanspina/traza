# Código del prototipo

- analisis/: UTF-8, lexer, AST y parser.
- comprobacion.py: firmas, tipos y obligaciones conservadoras del subconjunto D0.
- numeros.py: decimal finito exacto mínimo con presupuestos externos.
- ejecucion.py: máquina de continuaciones, contratos, propagación y serialización.
- __main__.py: tokens, analizar, verificar y ejecutar.

No existe todavía un núcleo elaborado completo, efectos, comprobador general ni biblioteca numérica completa. No ejecutar texto Traza mediante eval o exec. Ver documentacion/ejecucion-d0.md para alcance y decisiones.
