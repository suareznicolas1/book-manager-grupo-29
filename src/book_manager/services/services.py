import csv
import datetime
from pathlib import Path
from typing import Generic, List, Optional, TypeVar

import os
from decimal import Decimal, InvalidOperation

import requests
from dotenv import load_dotenv

from book_manager.entities.entities import (
    EntidadBase,
    Genero,
    Editorial,
    Moneda,
    TipoCotizacion,
    Libro,
    Precio,
    Stock,
    CotizacionDolar,
)

from book_manager.repositories.repositories import (
    IRepositorio,
    IRepositorioStock,
    IRepositorioCotizacionDolar,
)


T = TypeVar("T", bound=EntidadBase)


class ServicioBase(Generic[T]):
    """
    Servicio base para entidades que utilizan
    operaciones CRUD mediante IRepositorio.
    """

    def __init__(self, repositorio: IRepositorio[T]):
        self.repositorio = repositorio

    def crear(self, entidad: T) -> T:
        """
        Crea una nueva entidad.

        Si el ID es 0, el repositorio se encargará
        de asignar automáticamente el siguiente ID.
        """

        if entidad.id != 0:
            existente = self.repositorio.leer_por_id(entidad.id)

            if existente is not None:
                raise ValueError(
                    f"Ya existe una entidad con ID {entidad.id}"
                )

        return self.repositorio.crear(entidad)

    def leer_por_id(self, id: int) -> Optional[T]:
        """Busca una entidad por su ID."""
        return self.repositorio.leer_por_id(id)

    def leer_todos(self) -> List[T]:
        """Devuelve todas las entidades."""
        return self.repositorio.leer_todos()

    def actualizar(self, entidad: T) -> T:
        """Actualiza una entidad existente."""

        if self.repositorio.leer_por_id(entidad.id) is None:
            raise ValueError(
                f"No existe una entidad con ID {entidad.id}"
            )

        return self.repositorio.actualizar(entidad)

    def eliminar(self, id: int) -> bool:
        """Elimina una entidad por su ID."""

        if self.repositorio.leer_por_id(id) is None:
            raise ValueError(
                f"No existe una entidad con ID {id}"
            )

        return self.repositorio.eliminar(id)


# ==========================================================
# Servicios para entidades con ID
# ==========================================================

class ServicioGenero(ServicioBase[Genero]):
    pass


class ServicioEditorial(ServicioBase[Editorial]):
    pass


class ServicioMoneda(ServicioBase[Moneda]):
    pass


class ServicioTipoCotizacion(ServicioBase[TipoCotizacion]):
    pass


class ServicioLibro(ServicioBase[Libro]):
    pass


class ServicioPrecio(ServicioBase[Precio]):
    pass


# ==========================================================
# Servicio Stock
# ==========================================================

class ServicioStock:
    """
    Servicio encargado de la lógica relacionada con el stock.

    Stock utiliza el ID del libro como clave.
    """

    def __init__(self, repositorio: IRepositorioStock):
        self.repositorio = repositorio

    def crear(self, stock: Stock) -> Stock:

        existente = self.repositorio.leer_por_libro(
            stock.libro.id
        )

        if existente is not None:
            raise ValueError(
                "Ya existe stock registrado para este libro."
            )

        return self.repositorio.crear(stock)

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        return self.repositorio.leer_por_libro(libro_id)

    def actualizar(self, stock: Stock) -> Stock:

        existente = self.repositorio.leer_por_libro(
            stock.libro.id
        )

        if existente is None:
            raise ValueError(
                "No existe stock registrado para este libro."
            )

        return self.repositorio.actualizar(stock)

    def eliminar(self, libro_id: int) -> bool:

        existente = self.repositorio.leer_por_libro(libro_id)

        if existente is None:
            raise ValueError(
                "No existe stock registrado para este libro."
            )

        return self.repositorio.eliminar(libro_id)


# ==========================================================
# Servicio Cotización Dólar
# ==========================================================

class ServicioCotizacionDolar:
    """
    Servicio encargado de la lógica relacionada
    con las cotizaciones del dólar.

    Las cotizaciones utilizan como clave:
    tipo de cotización + fecha.
    """

    def __init__(
    self,
    repositorio: IRepositorioCotizacionDolar,
    repositorio_tipos: IRepositorio[TipoCotizacion]
):
        self.repositorio = repositorio
        self.repositorio_tipos = repositorio_tipos

    def crear(
        self,
        cotizacion: CotizacionDolar
    ) -> CotizacionDolar:

        existente = self.repositorio.leer_por_tipo_y_fecha(
            cotizacion.tipo_cotizacion.id,
            cotizacion.fecha
        )

        if existente is not None:
            raise ValueError(
                "Ya existe una cotización para ese tipo y fecha."
            )

        return self.repositorio.crear(cotizacion)

    def leer_por_tipo_y_fecha(
        self,
        tipo_id: int,
        fecha: datetime.date
    ) -> Optional[CotizacionDolar]:

        return self.repositorio.leer_por_tipo_y_fecha(
            tipo_id,
            fecha
        )

    def leer_historico_por_tipo(
        self,
        tipo_id: int
    ) -> List[CotizacionDolar]:

        return self.repositorio.leer_historico_por_tipo(
            tipo_id
        )

    def actualizar(
        self,
        cotizacion: CotizacionDolar
    ) -> CotizacionDolar:

        existente = self.repositorio.leer_por_tipo_y_fecha(
            cotizacion.tipo_cotizacion.id,
            cotizacion.fecha
        )

        if existente is None:
            raise ValueError(
                "No existe una cotización para ese tipo y fecha."
            )

        return self.repositorio.actualizar(cotizacion)

    def eliminar(
        self,
        tipo_id: int,
        fecha: datetime.date
    ) -> bool:

        existente = self.repositorio.leer_por_tipo_y_fecha(
            tipo_id,
            fecha
        )

        if existente is None:
            raise ValueError(
                "No existe una cotización para ese tipo y fecha."
            )

        return self.repositorio.eliminar(
            tipo_id,
            fecha
        )

    def obtener_cotizaciones(self) -> dict:
        """
        Descarga cotizaciones desde DolarAPI y las registra en SQLite.

        Utiliza la fecha de actualización informada por la API.
        Evita duplicados mediante la clave tipo de cotización + fecha.

        Returns:
            dict: resumen de cotizaciones insertadas, existentes y omitidas.
        """
        load_dotenv()

        api_url = os.getenv("API_URL")
        if not api_url:
            raise ValueError("No se configuró API_URL en el archivo .env.")

        try:
            respuesta = requests.get(api_url, timeout=15)
            respuesta.raise_for_status()
            datos = respuesta.json()
        except (requests.RequestException, ValueError) as exc:
            raise RuntimeError(
                f"No se pudieron obtener las cotizaciones: {exc}"
            ) from exc

        if not isinstance(datos, list):
            raise ValueError("La API no devolvió una lista de cotizaciones.")

        tipos = {
            tipo.nombre.strip().casefold(): tipo
            for tipo in self.repositorio_tipos.leer_todos()
        }

        # Correspondencias entre los códigos de la API
        # y los nombres definidos en nuestra base de datos.
        equivalencias = {
            "oficial": "oficial",
            "blue": "blue",
            "bolsa": "bolsa",
            "contadoconliqui": "ccl",
            "mayorista": "mayorista",
            "cripto": "cripto",
            "tarjeta": "turista",
        }

        resultado = {
            "insertadas": 0,
            "existentes": 0,
            "omitidas": 0,
        }

        for dato in datos:
            try:
                codigo = str(dato["casa"]).strip().casefold()
                nombre_tipo = equivalencias.get(codigo, codigo)
                tipo = tipos.get(nombre_tipo)

                if tipo is None:
                    resultado["omitidas"] += 1
                    continue

                fecha_texto = dato["fechaActualizacion"]
                fecha = datetime.date.fromisoformat(
                    fecha_texto[:10]
                )

                compra = Decimal(str(dato["compra"]))
                venta = Decimal(str(dato["venta"]))

                if not (
                    compra.is_finite()
                    and venta.is_finite()
                    and compra > 0
                    and venta > 0
                ):
                    resultado["omitidas"] += 1
                    continue

                if self.leer_por_tipo_y_fecha(tipo.id, fecha):
                    resultado["existentes"] += 1
                    continue

                cotizacion = CotizacionDolar(
                    fecha=fecha,
                    tipo_cotizacion=tipo,
                    compra=compra,
                    venta=venta,
                )

                self.crear(cotizacion)
                resultado["insertadas"] += 1

            except (
                KeyError,
                TypeError,
                ValueError,
                InvalidOperation,
            ):
                resultado["omitidas"] += 1
        return resultado


# ==========================================================
# Servicio Reporte de Precios
# ==========================================================

class ServicioReportePrecios:
    """Genera los reportes de precios en distintas monedas."""

    CODIGO_PESOS = "ARS"
    CODIGO_DOLAR = "USD"

    def __init__(
        self,
        servicio_precios: ServicioPrecio,
        servicio_monedas: ServicioMoneda,
        servicio_cotizaciones: ServicioCotizacionDolar,
    ) -> None:
        self.servicio_precios = servicio_precios
        self.servicio_monedas = servicio_monedas
        self.servicio_cotizaciones = servicio_cotizaciones

    def _venta_mas_reciente(self, tipo_id: int) -> Optional[float]:
        """Devuelve la última cotización de venta del tipo indicado."""
        historico = self.servicio_cotizaciones.leer_historico_por_tipo(tipo_id)
        return historico[-1].venta if historico else None

    def _precio_en(
        self,
        pesos: float,
        libro_id: int,
        moneda: Moneda,
        guardados: dict[tuple[int, int], float],
        venta: Optional[float],
    ) -> Optional[float]:
        """Precio de un libro en una moneda: guardado o convertido."""
        if (libro_id, moneda.id) in guardados:
            return guardados[(libro_id, moneda.id)]
        if moneda.codigo == self.CODIGO_DOLAR and venta:
            return round(pesos / venta, 2)
        return None

    def _precios_guardados(self) -> dict[tuple[int, int], float]:
        return {
            (p.libro.id, p.moneda.id): p.valor
            for p in self.servicio_precios.leer_todos()
        }

    def lista_bimonetaria(
        self, moneda: Moneda, tipo_cotizacion_id: int
    ) -> list[tuple[Libro, float, Optional[float]]]:
        """Devuelve (libro, precio en pesos, precio en la otra moneda)."""
        guardados = self._precios_guardados()
        venta = self._venta_mas_reciente(tipo_cotizacion_id)
        filas = []
        for p in self.servicio_precios.leer_todos():
            if p.moneda.codigo != self.CODIGO_PESOS:
                continue
            otro = self._precio_en(p.valor, p.libro.id, moneda, guardados, venta)
            filas.append((p.libro, p.valor, otro))
        return filas

    def exportar_csv(self, ruta: str, tipo_cotizacion_id: int) -> int:
        """Exporta los precios de todos los libros en todas las monedas.

        Returns:
            int: cantidad de libros exportados.
        """
        monedas = self.servicio_monedas.leer_todos()
        guardados = self._precios_guardados()
        venta = self._venta_mas_reciente(tipo_cotizacion_id)
        pesos_por_libro = {
            p.libro.id: p
            for p in self.servicio_precios.leer_todos()
            if p.moneda.codigo == self.CODIGO_PESOS
        }
        destino = Path(ruta)
        destino.parent.mkdir(parents=True, exist_ok=True)
        with open(destino, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(
                ["isbn", "titulo"] + [m.codigo for m in monedas]
            )
            for p in pesos_por_libro.values():
                valores = [
                    self._precio_en(p.valor, p.libro.id, m, guardados, venta)
                    for m in monedas
                ]
                escritor.writerow(
                    [p.libro.isbn, p.libro.titulo]
                    + ["" if v is None else f"{v:.2f}" for v in valores]
                )
        return len(pesos_por_libro)
