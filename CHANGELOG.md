# CHANGELOG

## [Ejercicio 07]
* Implementación de `main.py` como punto de entrada principal de la aplicación.
* Integración desde `main.py` de los repositorios, servicios, precarga de datos e interfaz de consola.
* Incorporación del parámetro `import_default_data`, permitiendo iniciar la aplicación con o sin la precarga de datos desde los archivos CSV.

### Fixes
* Corrección de `services.py` para adaptar la capa de servicios a las interfaces y métodos definidos en los repositorios.
* Implementación de `ServicioBase` genérico para centralizar las operaciones CRUD y sus validaciones.
* Incorporación de servicios específicos para Stock y Cotización del Dólar, contemplando sus claves particulares.
* Corrección de las validaciones para permitir la creación de entidades con ID autogenerado y evitar operaciones sobre registros inexistentes.
* Corrección de `console.py` para utilizar la capa de servicios en lugar de acceder directamente a los repositorios.
* Corrección de la integración entre `main.py` y `ConsoleUI` para enviar las instancias de los servicios correspondientes.
* Validación de la ejecución completa de la aplicación y de la precarga opcional de datos.

## [Ejercicio 06]
* Creación de los CRUD para Géneros,Editoriales,Monedas,Tipos de Cotización,Libros,Precios,Stock,Cotizaciones del Dolar.


## [Ejercicio 05]
* Creación de los archivos CSV de precarga en `migrations/csv` (generos,
  editoriales, monedas, tipos_cotizacion, libros, precios, stock y
  cotizaciones_dolar), con un mínimo de 10 registros por clase.
* Implementación de `preload_data.py` con funciones para leer cada CSV
  y cargar las entidades en sus repositorios, resolviendo las
  relaciones entre ellas (Libro-Editorial/Genero, Precio-Libro/Moneda,
  Stock-Libro, CotizacionDolar-TipoCotizacion).
* Corrección de un bug en `repositories.py` (`RepositorioCotizacionDolar`
  usaba `cotizacion.tipo_id`, atributo inexistente en la entidad;
  se corrigió a `cotizacion.tipo_cotizacion.id`).
* Corrección del import de `repositories.py`, que apuntaba a
  `src.book_manager.entities.entities` en lugar de
  `book_manager.entities.entities`, rompiendo la ejecución con el
  `PYTHONPATH` definido en el notebook.

## [Ejercicio 04]
* Creación de servicios.

## [Ejercicio 03]
* Creación de interfaces abstractas para la persistencia de datos.
* Implementación de RepositorioStock y RepositorioCotizacionDolar en memoria.
* Desarrollo de RepositorioGenerico para cubrir el CRUD del resto de las entidades.

## [Ejercicio 02]

- Se definieron las entidades del sistema:
  - EntidadBase
  - Libro
  - Genero
  - Editorial
  - Moneda
  - TipoCotizacion
  - Precio
  - Stock
  - CotizacionDolar
- Se aplicó encapsulación mediante atributos privados y properties.
- Se agregaron validaciones básicas para los atributos de las entidades.
- Se implementaron relaciones entre entidades mediante objetos.

## [Ejercicio 01]

- Creación de la estructura inicial del proyecto.
- Creación de los módulos de entidades, repositorios, servicios e interfaz de consola.
- Creación del directorio para la precarga de datos.
- Creación del directorio para archivos CSV.
- Creación de los archivos README.md, CHANGELOG.md y requirements.txt.
- Creación de la rama Sprint_1.