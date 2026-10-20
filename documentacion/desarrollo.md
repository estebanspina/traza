# Entorno y verificación

## PI01
La referencia de desarrollo es CPython 3.12.12, fijada en .python-version. La familia soportada es 3.12; la CI usa la referencia exacta y registra versión y plataforma. Las acciones se fijan por SHA. No se requieren paquetes externos para verificar esta entrega.

```sh
git clone https://github.com/estebanspina/traza.git
cd traza
python --version
python herramientas/verificar.py
```

El verificador descubre todas las pruebas, falla si no encuentra ninguna y comprueba la sintaxis del código anfitrión. Puede ejecutarse desde otro directorio usando su ruta absoluta. No instala dependencias ni requiere secretos. El runner ubuntu-latest puede cambiar; la versión y plataforma registradas delimitan la reproducción, que no se promete binariamente idéntica.

## PI02
El catálogo contiene todas las reglas S01–S24, T01–T28, N01–N32 y G01–G32, y los cuarenta casos CF con sus variantes. El esquema 0.1 distingue programas, vectores, propiedades y protocolos. La integridad de esos artefactos se verifica sin ejecutar sus expectativas.

La finalización de PI02 significa preparación de catálogo y fixtures, no aprobación de conformidad ni resolución de todas las APIs futuras. Una regla sin caso directo sigue visible como pendiente.

## Límites
Aún no se implementan parser, resolución, comprobador ni runtime. No declarar esos paquetes terminados porque pase esta verificación.
