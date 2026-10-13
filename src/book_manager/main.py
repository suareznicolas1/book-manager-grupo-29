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

    from book_manager.database.connection import ConexionDB
    from book_manager.models.models import crear_tablas
    from book_manager.migrations.migrations import migrar_datos

    db = ConexionDB()
    crear_tablas(db.engine)

    repo_generos = RepositorioGenerico(Genero, db)
    repo_editoriales = RepositorioGenerico(Editorial, db)
    repo_monedas = RepositorioGenerico(Moneda, db)
    repo_tipos_cotizacion = RepositorioGenerico(TipoCotizacion, db)
    repo_libros = RepositorioGenerico(Libro, db)
    repo_precios = RepositorioGenerico(Precio, db)
    repo_stock = RepositorioStock(db)
    repo_cotizaciones = RepositorioCotizacionDolar(db)

    # ------------------------------------------------------
    # 2. Precarga de datos desde CSV
    # ------------------------------------------------------

    if import_default_data:
        carpeta = Path(__file__).resolve().parent / "migrations"
        migrar_datos(str(carpeta / "csv"), str(carpeta / "sql"), db)
    else:
        print("Sistema iniciado con base de datos, sin migración inicial.")

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