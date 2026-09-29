import sys
from pathlib import Path


# ==========================================================
# Configuración del path
# ==========================================================

# Agrega /src al path para poder importar book_manager
src_path = str(Path(__file__).resolve().parent.parent)

if src_path not in sys.path:
    sys.path.insert(0, src_path)


# ==========================================================
# Imports
# ==========================================================

from book_manager.entities.entities import (
    Genero,
    Editorial,
    Moneda,
    TipoCotizacion,
    Libro,
    Precio,
)

from book_manager.repositories.repositories import (
    RepositorioGenerico,
    RepositorioStock,
    RepositorioCotizacionDolar,
)

from book_manager.services.services import (
    ServicioGenero,
    ServicioEditorial,
    ServicioMoneda,
    ServicioTipoCotizacion,
    ServicioLibro,
    ServicioPrecio,
    ServicioStock,
    ServicioCotizacionDolar,
)

from book_manager.preload_data.preload_data import precargar_datos
from book_manager.ui.console import ConsoleUI


# ==========================================================
# Main
# ==========================================================

def main(import_default_data: bool = True) -> None:

    # ------------------------------------------------------
    # 1. Crear repositorios
    # ------------------------------------------------------

    repo_generos = RepositorioGenerico[Genero]()
    repo_editoriales = RepositorioGenerico[Editorial]()
    repo_monedas = RepositorioGenerico[Moneda]()
    repo_tipos_cotizacion = RepositorioGenerico[TipoCotizacion]()
    repo_libros = RepositorioGenerico[Libro]()
    repo_precios = RepositorioGenerico[Precio]()

    repo_stock = RepositorioStock()
    repo_cotizaciones = RepositorioCotizacionDolar()

    # ------------------------------------------------------
    # 2. Precarga de datos desde CSV
    # ------------------------------------------------------

    if import_default_data:

        print("Iniciando precarga de datos desde archivos CSV...")

        try:

            precargar_datos(
                repo_generos=repo_generos,
                repo_editoriales=repo_editoriales,
                repo_monedas=repo_monedas,
                repo_tipos_cotizacion=repo_tipos_cotizacion,
                repo_libros=repo_libros,
                repo_precios=repo_precios,
                repo_stock=repo_stock,
                repo_cotizaciones=repo_cotizaciones,
            )

            print("✅ Precarga completada exitosamente.")

        except Exception as e:

            print(
                f"⚠️ Error durante la precarga de datos: {e}"
            )

    else:

        print("ℹ️ Sistema iniciado sin precarga de datos.")

    # ------------------------------------------------------
    # 3. Crear servicios
    # ------------------------------------------------------

    servicio_generos = ServicioGenero(repo_generos)
    servicio_editoriales = ServicioEditorial(repo_editoriales)
    servicio_monedas = ServicioMoneda(repo_monedas)
    servicio_tipos_cotizacion = ServicioTipoCotizacion(
        repo_tipos_cotizacion
    )
    servicio_libros = ServicioLibro(repo_libros)
    servicio_precios = ServicioPrecio(repo_precios)
    servicio_stock = ServicioStock(repo_stock)
    servicio_cotizaciones = ServicioCotizacionDolar(
        repo_cotizaciones
    )


    # ------------------------------------------------------
    # 4. Iniciar interfaz de consola
    # ------------------------------------------------------

    ui = ConsoleUI(
        servicio_generos=servicio_generos,
        servicio_editoriales=servicio_editoriales,
        servicio_monedas=servicio_monedas,
        servicio_tipos_cotizacion=servicio_tipos_cotizacion,
        servicio_libros=servicio_libros,
        servicio_precios=servicio_precios,
        servicio_stock=servicio_stock,
        servicio_cotizaciones=servicio_cotizaciones,
    )

    ui.iniciar()


# ==========================================================
# Ejecución directa
# ==========================================================

if __name__ == "__main__":
    main()