"""Migración de datos desde los archivos CSV a la base de datos.

Lee los CSV del TP1, genera un archivo ``.sql`` por tabla con las
sentencias ``INSERT`` y luego ejecuta esas mismas sentencias en la base
de datos, dentro de una única transacción.
"""

import csv
import datetime
from collections.abc import Callable
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from book_manager.database.connection import ConexionDB
from book_manager.models.models import crear_tablas

CARPETA_BASE = Path(__file__).resolve().parent
CARPETA_CSV = CARPETA_BASE / "csv"
CARPETA_SQL = CARPETA_BASE / "sql"


# ============================================================
# Conversores de valores (CSV -> literal SQL)
# ============================================================

def _entero(valor: str) -> str:
    """Valida un entero y lo devuelve como literal SQL."""
    return str(int(valor.strip()))


def _decimal(valor: str) -> str:
    """Valida un número decimal y lo devuelve como literal SQL."""
    try:
        return str(Decimal(valor.strip()))
    except InvalidOperation as error:
        raise ValueError(f"Número inválido: {valor!r}") from error


def _texto(valor: str) -> str:
    """Devuelve un texto entre comillas, escapando las comillas simples."""
    limpio = valor.strip()
    if not limpio:
        raise ValueError("Texto vacío")
    return "'" + limpio.replace("'", "''") + "'"


def _fecha(valor: str) -> str:
    """Valida una fecha ISO (AAAA-MM-DD) y la devuelve como literal SQL."""
    return f"'{datetime.date.fromisoformat(valor.strip()).isoformat()}'"


# Orden de migración: primero las tablas de las que dependen las demás.
# Cada elemento: (archivo CSV, tabla destino, {columna: conversor}).
TABLAS: list[tuple[str, str, dict[str, Callable[[str], str]]]] = [
    ("generos.csv", "generos", {"id": _entero, "nombre": _texto}),
    ("editoriales.csv", "editoriales", {"id": _entero, "nombre": _texto}),
    (
        "monedas.csv",
        "monedas",
        {"id": _entero, "codigo": _texto, "nombre": _texto},
    ),
    ("tipos_cotizacion.csv", "tipos_cotizacion", {"id": _entero, "nombre": _texto}),
    (
        "libros.csv",
        "libros",
        {
            "id": _entero,
            "isbn": _texto,
            "titulo": _texto,
            "autor": _texto,
            "editorial_id": _entero,
            "genero_id": _entero,
        },
    ),
    (
        "precios.csv",
        "precios",
        {
            "id": _entero,
            "libro_id": _entero,
            "moneda_id": _entero,
            "valor": _decimal,
        },
    ),
    ("stock.csv", "stock", {"libro_id": _entero, "cantidad": _entero}),
    (
        "cotizaciones_dolar.csv",
        "cotizaciones_dolar",
        {
            "tipo_cotizacion_id": _entero,
            "fecha": _fecha,
            "compra": _decimal,
            "venta": _decimal,
        },
    ),
]


# ============================================================
# Generación de sentencias SQL
# ============================================================

def _generar_sentencias(
    ruta_csv: Path,
    tabla: str,
    columnas: dict[str, Callable[[str], str]],
) -> list[str]:
    """Convierte las filas de un CSV en sentencias INSERT.

    Args:
        ruta_csv (Path): archivo CSV de origen.
        tabla (str): nombre de la tabla destino.
        columnas (dict): conversor a aplicar a cada columna del CSV.

    Returns:
        list[str]: una sentencia INSERT por cada fila del CSV.

    Raises:
        ValueError: si falta una columna o un valor no es válido.
    """
    sentencias: list[str] = []
    with open(ruta_csv, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        faltantes = set(columnas) - set(lector.fieldnames or [])
        if faltantes:
            raise ValueError(
                f"{ruta_csv.name}: faltan las columnas {sorted(faltantes)}"
            )
        nombres = ", ".join(columnas)
        for numero, fila in enumerate(lector, start=2):
            try:
                valores = ", ".join(
                    conversor(fila[columna])
                    for columna, conversor in columnas.items()
                )
            except (ValueError, TypeError) as error:
                raise ValueError(
                    f"{ruta_csv.name}, línea {numero}: {error}"
                ) from error
            sentencias.append(
                f"INSERT INTO {tabla} ({nombres}) VALUES ({valores});"
            )
    return sentencias


def _guardar_sql(
    ruta_sql: Path, archivo_csv: str, tabla: str, sentencias: list[str]
) -> None:
    """Escribe un archivo .sql con las sentencias de una tabla."""
    encabezado = f"-- Tabla {tabla} (origen: {archivo_csv})\n"
    ruta_sql.write_text(
        encabezado + "\n".join(sentencias) + "\n", encoding="utf-8"
    )


# ============================================================
# Migración
# ============================================================

def migrar_datos(
    carpeta_csvs: str,
    carpeta_sqls: str,
    db: ConexionDB | None = None,
) -> dict[str, int]:
    """Función encargada de la migración de datos de csv a sql.
    Se encarga de leer los archivos csv y crear los archivos sql
    para la inserción en la base de datos.

    Crea las tablas si no existen, genera un archivo .sql por tabla (con
    prefijo numérico que indica el orden de carga) y ejecuta las sentencias
    en una sola transacción. Si una tabla ya tiene datos no se vuelve a
    cargar, por lo que la función puede ejecutarse más de una vez.

    Args:
        carpeta_csvs (str): Carpeta donde se encuentran los archivos csv de origen.
        carpeta_sqls (str): Carpeta donde se deben guardar los archivos sql generados.
        db (ConexionDB | None): conexión a usar. Si es None se usa la
            base por defecto del proyecto.

    Returns:
        dict[str, int]: cantidad de filas insertadas por tabla.
    """
    origen = Path(carpeta_csvs)
    destino = Path(carpeta_sqls)
    destino.mkdir(parents=True, exist_ok=True)

    conexion = db if db is not None else ConexionDB()
    crear_tablas(conexion.engine)

    # 1. Generar todos los .sql antes de tocar la base de datos.
    pendientes: list[tuple[str, list[str]]] = []
    for orden, (archivo_csv, tabla, columnas) in enumerate(TABLAS, start=1):
        sentencias = _generar_sentencias(origen / archivo_csv, tabla, columnas)
        _guardar_sql(destino / f"{orden:02d}_{tabla}.sql", archivo_csv, tabla, sentencias)
        pendientes.append((tabla, sentencias))

    # 2. Ejecutar las sentencias en una única transacción.
    insertadas: dict[str, int] = {}
    with conexion.transaccion() as sesion:
        cnx: Any = sesion.connection()
        for tabla, sentencias in pendientes:
            existentes = cnx.exec_driver_sql(
                f"SELECT COUNT(*) FROM {tabla}"
            ).scalar_one()
            if existentes:
                print(f"- {tabla}: ya tiene datos, se omite.")
                insertadas[tabla] = 0
                continue
            for sentencia in sentencias:
                cnx.exec_driver_sql(sentencia)
            insertadas[tabla] = len(sentencias)
            print(f"- {tabla}: {len(sentencias)} registros insertados.")
    return insertadas


if __name__ == "__main__":
    migrar_datos(str(CARPETA_CSV), str(CARPETA_SQL))
