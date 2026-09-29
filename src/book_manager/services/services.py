import datetime
from typing import Generic, List, Optional, TypeVar

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
        repositorio: IRepositorioCotizacionDolar
    ):
        self.repositorio = repositorio

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