# CHANGELOG

## [Ejercicio 07]

- Implementación del método `obtener_cotizaciones()` en `ServicioCotizacionDolar` para consultar cotizaciones mediante la API de DolarAPI.
- Incorporación de `python-dotenv` para obtener la URL de la API desde el archivo `.env`.
- Utilización de `requests` para realizar solicitudes HTTP y procesar las respuestas JSON.
- Integración de las cotizaciones obtenidas con los tipos de cotización existentes en la base de datos.
- Validación de fechas y valores de compra y venta antes de registrar las cotizaciones.
- Persistencia de las cotizaciones descargadas en SQLite mediante los repositorios SQLAlchemy.
- Implementación de controles para evitar registros duplicados por tipo de cotización y fecha.
- Validación funcional de la descarga, inserción y consulta del histórico, comprobando que las ejecuciones posteriores no generan duplicados.

## [Ejercicio 06]

- Adaptación de `RepositorioGenerico` para realizar operaciones CRUD sobre la base de datos SQLite mediante SQLAlchemy.
- Implementación de los métodos de creación, consulta, actualización y eliminación utilizando sesiones administradas por `ConexionDB`.
- Incorporación del mapeo entre las entidades del dominio y los modelos ORM, manteniendo la compatibilidad con la capa de servicios existente.
- Adaptación de `RepositorioStock` y `RepositorioCotizacionDolar` para utilizar persistencia en la base de datos.
- Actualización de `main.py` para inicializar la conexión, crear las tablas y utilizar los repositorios SQLAlchemy.
- Integración del proceso de migración de datos CSV a SQLite mediante el parámetro `import_default_data`.
- Validación de las operaciones CRUD desde la consola y de la persistencia de los registros después de reiniciar la aplicación.
- Verificación de las relaciones entre libros, géneros y editoriales, incluyendo las restricciones de integridad.

## [Ejercicio 05]

- Implementación de `migrar_datos` en `migrations/migrations.py` para migrar los CSV del TP1 a la base de datos.
- Generación de un archivo `.sql` por tabla en `migrations/sql` con las sentencias INSERT (orden de carga numerado).
- Ejecución de las sentencias en una única transacción con el context manager de `ConexionDB`.
- Validación y conversión de cada valor del CSV, con mensajes de error indicando archivo y línea.
- Migración repetible: las tablas que ya tienen datos se omiten.

## [Ejercicio 04]

- Definición de los modelos ORM en `models/models.py` con SQLAlchemy (DeclarativeBase y `Mapped`).
- Tablas creadas: generos, editoriales, monedas, tipos_cotizacion, libros, precios, stock y cotizaciones_dolar.
- Relaciones entre tablas mediante claves foráneas y `relationship`.
- Claves primarias compuestas en cotizaciones_dolar (tipo y fecha) y clave primaria/foránea en stock (libro).
- Restricciones de integridad: valores únicos (ISBN, nombres, código de moneda), un precio por libro y moneda, y valores no negativos.
- Incorporación de la función `crear_tablas` para generar el esquema en la base.

## [Ejercicio 03]

- Implementación del context manager `transaccion` en `ConexionDB` usando `contextlib.contextmanager`.
- Confirmación automática (commit) al finalizar el bloque sin errores.
- Reversión (rollback) y relanzamiento de la excepción ante cualquier error.
- Cierre de la sesión garantizado en todos los casos.


## [Ejercicio 02]

- Implementación de la clase ConexionDB utilizando SQLAlchemy.
- Configuración de una base SQLite en la carpeta principal del proyecto.
- Incorporación de creación de sesiones y verificación de conexión.
- Exclusión de los archivos de la base local mediante .gitignore.

## [Ejercicio 01]

- Inicio del Sprint 2 sobre la rama Sprint_2, partiendo de Sprint_1.
- Incorporación de las carpetas database y models.
- Preparación del archivo migrations.py y de la carpeta migrations/sql.
- Actualización del README con el objetivo y contexto del Sprint 2.


## [SPRINT_02]


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