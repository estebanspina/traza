# Herramientas de desarrollo

- verificar.py: descubre todas las pruebas y compila sintaxis del anfitrión, sin dependencias externas.
- catalogo.py: valida preparación e integridad del catálogo; no ejecuta los casos.
- traza.py: arranca el comando tokens desde un checkout sin instalar paquetes.

```sh
python herramientas/verificar.py
python herramientas/traza.py tokens ejemplos/contratos/bounded.traza
```
