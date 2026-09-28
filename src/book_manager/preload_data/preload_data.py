"""Precarga de datos iniciales para el sistema Book Manager.

Este módulo lee los archivos CSV ubicados en
``book_manager/migrations/csv`` y crea las entidades correspondientes,
insertándolas en los repositorios en memoria del sistema. Respeta las
relaciones entre entidades (Libro -> Editorial/Genero, Precio ->
Libro/Moneda, Stock -> Libro, CotizacionDolar -> TipoCotizacion).
"""
import csv
import datetime
from pathlib import Path
from typing import Dict

from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)
from book_manager.repositories.repositories import (
    RepositorioCotizacionDolar,
    RepositorioGenerico,
    RepositorioStock,
)

RUTA_CSV = Path(__file__).resolve().parent.parent / "migrations" / "csv"


def _leer_csv(nombre_archivo: str) -> list[dict[str, str]]:
    """Lee un archivo CSV de la carpeta migrations/csv.

    Args:
        nombre_archivo: Nombre del archivo CSV a leer.

    Returns:
        Lista de diccionarios, uno por fila del archivo.
    """
    ruta = RUTA_CSV / nombre_archivo
    with open(ruta, newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def cargar_generos(repositorio: RepositorioGenerico) -> Dict[int, Genero]:
    """Carga los géneros desde generos.csv en el repositorio dado."""
    generos: Dict[int, Genero] = {}
    for fila in _leer_csv("generos.csv"):
        genero = Genero(id=int(fila["id"]), nombre=fila["nombre"])
        repositorio.crear(genero)
        generos[genero.id] = genero
    return generos


def cargar_editoriales(repositorio: RepositorioGenerico) -> Dict[int, Editorial]:
    """Carga las editoriales desde editoriales.csv en el repositorio dado."""
    editoriales: Dict[int, Editorial] = {}
    for fila in _leer_csv("editoriales.csv"):
        editorial = Editorial(id=int(fila["id"]), nombre=fila["nombre"])
        repositorio.crear(editorial)
        editoriales[editorial.id] = editorial
    return editoriales


def cargar_monedas(repositorio: RepositorioGenerico) -> Dict[int, Moneda]:
    """Carga las monedas desde monedas.csv en el repositorio dado."""
    monedas: Dict[int, Moneda] = {}
    for fila in _leer_csv("monedas.csv"):
        moneda = Moneda(
            id=int(fila["id"]), codigo=fila["codigo"], nombre=fila["nombre"]
        )
        repositorio.crear(moneda)
        monedas[moneda.id] = moneda
    return monedas


def cargar_tipos_cotizacion(
    repositorio: RepositorioGenerico,
) -> Dict[int, TipoCotizacion]:
    """Carga los tipos de cotización desde tipos_cotizacion.csv."""
    tipos: Dict[int, TipoCotizacion] = {}
    for fila in _leer_csv("tipos_cotizacion.csv"):
        tipo = TipoCotizacion(id=int(fila["id"]), nombre=fila["nombre"])
        repositorio.crear(tipo)
        tipos[tipo.id] = tipo
    return tipos


def cargar_libros(
    repositorio: RepositorioGenerico,
    editoriales: Dict[int, Editorial],
    generos: Dict[int, Genero],
) -> Dict[int, Libro]:
    """Carga los libros desde libros.csv, resolviendo sus relaciones."""
    libros: Dict[int, Libro] = {}
    for fila in _leer_csv("libros.csv"):
        libro = Libro(
            id=int(fila["id"]),
            isbn=fila["isbn"],
            titulo=fila["titulo"],
            autor=fila["autor"],
            editorial=editoriales[int(fila["editorial_id"])],
            genero=generos[int(fila["genero_id"])],
        )
        repositorio.crear(libro)
        libros[libro.id] = libro
    return libros


def cargar_precios(
    repositorio: RepositorioGenerico,
    libros: Dict[int, Libro],
    monedas: Dict[int, Moneda],
) -> None:
    """Carga los precios desde precios.csv, resolviendo sus relaciones."""
    for fila in _leer_csv("precios.csv"):
        precio = Precio(
            id=int(fila["id"]),
            libro=libros[int(fila["libro_id"])],
            moneda=monedas[int(fila["moneda_id"])],
            valor=float(fila["valor"]),
        )
        repositorio.crear(precio)


def cargar_stock(
    repositorio: RepositorioStock, libros: Dict[int, Libro]
) -> None:
    """Carga el stock desde stock.csv, resolviendo la relación con Libro."""
    for fila in _leer_csv("stock.csv"):
        stock = Stock(
            libro=libros[int(fila["libro_id"])], cantidad=int(fila["cantidad"])
        )
        repositorio.crear(stock)


def cargar_cotizaciones_dolar(
    repositorio: RepositorioCotizacionDolar,
    tipos: Dict[int, TipoCotizacion],
) -> None:
    """Carga el histórico de cotizaciones desde cotizaciones_dolar.csv."""
    for fila in _leer_csv("cotizaciones_dolar.csv"):
        cotizacion = CotizacionDolar(
            fecha=datetime.datetime.strptime(fila["fecha"], "%Y-%m-%d").date(),
            tipo_cotizacion=tipos[int(fila["tipo_cotizacion_id"])],
            compra=float(fila["compra"]),
            venta=float(fila["venta"]),
        )
        repositorio.crear(cotizacion)


def precargar_datos(
    repo_generos: RepositorioGenerico,
    repo_editoriales: RepositorioGenerico,
    repo_monedas: RepositorioGenerico,
    repo_tipos_cotizacion: RepositorioGenerico,
    repo_libros: RepositorioGenerico,
    repo_precios: RepositorioGenerico,
    repo_stock: RepositorioStock,
    repo_cotizaciones: RepositorioCotizacionDolar,
) -> None:
    """Precarga todos los datos iniciales del sistema en los repositorios.

    Lee los CSV de ``migrations/csv`` en el orden correcto para poder
    resolver las relaciones entre entidades (por ejemplo, un Libro
    necesita que su Editorial y Genero ya existan).

    Args:
        repo_generos: Repositorio de Genero.
        repo_editoriales: Repositorio de Editorial.
        repo_monedas: Repositorio de Moneda.
        repo_tipos_cotizacion: Repositorio de TipoCotizacion.
        repo_libros: Repositorio de Libro.
        repo_precios: Repositorio de Precio.
        repo_stock: Repositorio de Stock.
        repo_cotizaciones: Repositorio de CotizacionDolar.
    """
    generos = cargar_generos(repo_generos)
    editoriales = cargar_editoriales(repo_editoriales)
    monedas = cargar_monedas(repo_monedas)
    tipos_cotizacion = cargar_tipos_cotizacion(repo_tipos_cotizacion)

    libros = cargar_libros(repo_libros, editoriales, generos)

    cargar_precios(repo_precios, libros, monedas)
    cargar_stock(repo_stock, libros)
    cargar_cotizaciones_dolar(repo_cotizaciones, tipos_cotizacion)
