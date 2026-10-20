# Parser y ejecución inicial

## Comandos

```sh
python herramientas/verificar.py
python herramientas/probar_d0.py

python herramientas/traza.py tokens ejemplos/contratos/bounded.traza
python herramientas/traza.py analizar ejemplos/contratos/bounded.traza
python herramientas/traza.py verificar ejemplos/contratos/bounded.traza
python herramientas/traza.py ejecutar ejemplos/contratos/bounded.traza --entrada bounded --argumentos '["50"]' --traza
python herramientas/traza.py ejecutar ejemplos/contratos/bounded.traza --entrada bounded --argumentos '["101"]' --traza
```

Los ejemplos de comillas siguen una terminal POSIX; en otros shells debe conservarse el mismo JSON. Number se transmite como texto para evitar conversiones aproximadas.

- tokens: fase léxica y posiciones.
- analizar: AST de la gramática, sin afirmar corrección de tipos.
- verificar: acepta sólo el subconjunto ejecutable comprobado y muestra obligaciones.
- ejecutar: compila primero y ejecuta una función pública, con argumentos compatibles.
- probar_d0.py: ejecuta las cuatro expectativas del manifiesto y emite un informe JSON.

## Resultados D0
bounded(50) produce Ok(Number 50). bounded(101) y bounded(-1) producen Err(ContractViolation) con condition_id, location y boundary. El retorno constante 101 bajo contrato <=100 se rechaza estáticamente con D05.

Un Err esperado es una ejecución satisfactoria de la herramienta, con salida 0. Los códigos de herramienta son: 1 para errores léxicos/sintácticos/estáticos o NI01; 2 para uso, lectura o argumentos externos inválidos; 3 para presupuestos agotados. No son variantes Error de Traza.

## Implementado
Parser de declaraciones, tipos, contratos, efectos, registros, listas, variantes, lambdas, patrones, genéricos y expresiones, con precedencias y rangos. Las restricciones semánticas no pertenecen al parser.

Ejecución inicial: primitivas, funciones puras, recursión con pila explícita, let, if, + - *, comparaciones, cortocircuito, Result, contratos numéricos simples, check y ?. El artefacto comprobado conserva firmas y obligaciones; la elaboración completa es posterior.

## Pendiente
No ejecuta aliases, genéricos, registros, listas, match, lambdas, efectos, división, redondeo, esquemas externos ni predicados incorporados. Las relaciones de contratos con parámetros distintos de value son NI01. La entrada CLI admite Number textual, Boolean y Text; Bytes sólo está disponible como literal en el subconjunto actual.

Los casos CF se mantienen como expectativas. El informe D0 registra resultados reales sin convertir la batería completa en aprobada. Existen pruebas adicionales de composición, rechazo estático, ramas y límites, que tampoco sustituyen la batería completa.
