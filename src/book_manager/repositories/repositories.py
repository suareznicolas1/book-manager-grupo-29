import abc
import datetime
from typing import TypeVar, Generic, List, Optional
from book_manager.entities.entities import EntidadBase, Stock, CotizacionDolar

T = TypeVar('T', bound=EntidadBase)


class IRepositorio(abc.ABC, Generic[T]):
  """Interfaz para repositorios que manejan entidades con operaciones CRUD básicas."""

  @abc.abstractmethod
  def crear(self, entidad: T) -> T:
    pass

  @abc.abstractmethod
  def leer_por_id(self, id: int) -> Optional[T]:
    pass

  @abc.abstractmethod
  def leer_todos(self) -> List[T]:
    pass

  @abc.abstractmethod
  def actualizar(self, entidad: T) -> T:
    pass

  @abc.abstractmethod
  def eliminar(self, id: int) -> bool:
    pass


class IRepositorioCotizacionDolar(abc.ABC):
  """Interfaz para repositorios del tipo RepositorioCotizacionDolar."""

  @abc.abstractmethod
  def crear(self, cotizacion: 'CotizacionDolar') -> 'CotizacionDolar':
    pass

  @abc.abstractmethod
  def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: datetime.date) -> Optional['CotizacionDolar']:
    pass

  @abc.abstractmethod
  def leer_historico_por_tipo(self, tipo_id: int) -> List['CotizacionDolar']:
    pass

  @abc.abstractmethod
  def actualizar(self, cotizacion: 'CotizacionDolar') -> 'CotizacionDolar':
    pass

  @abc.abstractmethod
  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    pass


class IRepositorioStock(abc.ABC):
  """Interfaz para repositorios del tipo Stock."""

  @abc.abstractmethod
  def crear(self, stock: Stock) -> Stock:
    pass

  @abc.abstractmethod
  def leer_por_libro(self, libro_id: int) -> Optional['Stock']:
    pass

  @abc.abstractmethod
  def actualizar(self, stock: 'Stock') -> 'Stock':
    pass

  @abc.abstractmethod
  def eliminar(self, libro_id: int) -> bool:
    pass



from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from book_manager.database.connection import ConexionDB
from book_manager.entities.entities import Genero, Editorial, Moneda, TipoCotizacion, Libro, Precio
from book_manager.models.models import (GeneroModel, EditorialModel, MonedaModel,
    TipoCotizacionModel, LibroModel, PrecioModel, StockModel, CotizacionDolarModel)

MODELOS = {Genero: GeneroModel, Editorial: EditorialModel, Moneda: MonedaModel,
           TipoCotizacion: TipoCotizacionModel, Libro: LibroModel, Precio: PrecioModel}


def _entidad(modelo):
    if modelo is None:
        return None
    if isinstance(modelo, GeneroModel):
        return Genero(modelo.id, modelo.nombre)
    if isinstance(modelo, EditorialModel):
        return Editorial(modelo.id, modelo.nombre)
    if isinstance(modelo, MonedaModel):
        return Moneda(modelo.id, modelo.codigo, modelo.nombre)
    if isinstance(modelo, TipoCotizacionModel):
        return TipoCotizacion(modelo.id, modelo.nombre)
    if isinstance(modelo, LibroModel):
        return Libro(modelo.id, modelo.isbn, modelo.titulo, modelo.autor,
                     _entidad(modelo.editorial), _entidad(modelo.genero))
    if isinstance(modelo, PrecioModel):
        return Precio(modelo.id, _entidad(modelo.libro), _entidad(modelo.moneda), float(modelo.valor))
    if isinstance(modelo, StockModel):
        return Stock(_entidad(modelo.libro), modelo.cantidad)
    if isinstance(modelo, CotizacionDolarModel):
        return CotizacionDolar(modelo.fecha, _entidad(modelo.tipo_cotizacion),
                               float(modelo.compra), float(modelo.venta))
    raise TypeError(f"Modelo desconocido: {type(modelo)}")


def _valores(entidad):
    if isinstance(entidad, (Genero, Editorial, TipoCotizacion)):
        return {"nombre": entidad.nombre}
    if isinstance(entidad, Moneda):
        return {"codigo": entidad.codigo, "nombre": entidad.nombre}
    if isinstance(entidad, Libro):
        return {"isbn": entidad.isbn, "titulo": entidad.titulo, "autor": entidad.autor,
                "editorial_id": entidad.editorial.id, "genero_id": entidad.genero.id}
    if isinstance(entidad, Precio):
        return {"libro_id": entidad.libro.id, "moneda_id": entidad.moneda.id,
                "valor": Decimal(str(entidad.valor))}
    if isinstance(entidad, Stock):
        return {"libro_id": entidad.libro.id, "cantidad": entidad.cantidad}
    if isinstance(entidad, CotizacionDolar):
        return {"tipo_cotizacion_id": entidad.tipo_cotizacion.id, "fecha": entidad.fecha,
                "compra": Decimal(str(entidad.compra)), "venta": Decimal(str(entidad.venta))}
    raise TypeError(f"Entidad desconocida: {type(entidad)}")


def _consulta(sesion, modelo):
    """Carga las relaciones antes de cerrar la sesión."""
    stmt = select(modelo)
    if modelo is LibroModel:
        stmt = stmt.options(joinedload(LibroModel.editorial), joinedload(LibroModel.genero))
    elif modelo is PrecioModel:
        stmt = stmt.options(joinedload(PrecioModel.libro).joinedload(LibroModel.editorial),
                            joinedload(PrecioModel.libro).joinedload(LibroModel.genero),
                            joinedload(PrecioModel.moneda))
    elif modelo is StockModel:
        stmt = stmt.options(joinedload(StockModel.libro).joinedload(LibroModel.editorial),
                            joinedload(StockModel.libro).joinedload(LibroModel.genero))
    elif modelo is CotizacionDolarModel:
        stmt = stmt.options(joinedload(CotizacionDolarModel.tipo_cotizacion))
    return stmt


class RepositorioGenerico(IRepositorio[T]):
    """Repositorio SQLAlchemy que devuelve entidades de dominio, no modelos ORM."""
    def __init__(self, tipo_entidad: type[T], db: ConexionDB):
        self.modelo = MODELOS[tipo_entidad]
        self.db = db

    def crear(self, entidad: T) -> T:
        valores = _valores(entidad)
        if entidad.id:
            valores["id"] = entidad.id
        try:
            with self.db.transaccion() as sesion:
                modelo = self.modelo(**valores)
                sesion.add(modelo)
                sesion.flush()
                id_nuevo = modelo.id
        except IntegrityError as exc:
            raise ValueError("No se pudo crear: registro duplicado o relación inválida.") from exc
        return self.leer_por_id(id_nuevo)

    def leer_por_id(self, id: int) -> Optional[T]:
        with self.db.crear_sesion() as sesion:
            modelo = sesion.execute(_consulta(sesion, self.modelo).where(self.modelo.id == id)).scalar_one_or_none()
            return _entidad(modelo)

    def leer_todos(self) -> List[T]:
        with self.db.crear_sesion() as sesion:
            modelos = sesion.execute(_consulta(sesion, self.modelo).order_by(self.modelo.id)).scalars().all()
            return [_entidad(m) for m in modelos]

    def actualizar(self, entidad: T) -> T:
        try:
            with self.db.transaccion() as sesion:
                modelo = sesion.get(self.modelo, entidad.id)
                if modelo is None:
                    raise ValueError(f"No existe la entidad con ID {entidad.id}.")
                for clave, valor in _valores(entidad).items():
                    setattr(modelo, clave, valor)
        except IntegrityError as exc:
            raise ValueError("No se pudo actualizar: restricción de base de datos.") from exc
        return self.leer_por_id(entidad.id)

    def eliminar(self, id: int) -> bool:
        try:
            with self.db.transaccion() as sesion:
                modelo = sesion.get(self.modelo, id)
                if modelo is None:
                    return False
                sesion.delete(modelo)
            return True
        except IntegrityError as exc:
            raise ValueError("No se puede eliminar: el registro tiene dependencias.") from exc


class RepositorioStock(IRepositorioStock):
    def __init__(self, db: ConexionDB):
        self.db = db

    def crear(self, stock: Stock) -> Stock:
        if self.leer_por_libro(stock.libro.id) is not None:
            raise ValueError("Ya existe stock para ese libro.")
        with self.db.transaccion() as sesion:
            sesion.add(StockModel(**_valores(stock)))
        return self.leer_por_libro(stock.libro.id)

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        with self.db.crear_sesion() as sesion:
            modelo = sesion.execute(_consulta(sesion, StockModel).where(StockModel.libro_id == libro_id)).scalar_one_or_none()
            return _entidad(modelo)

    def actualizar(self, stock: Stock) -> Stock:
        with self.db.transaccion() as sesion:
            modelo = sesion.get(StockModel, stock.libro.id)
            if modelo is None:
                raise ValueError("No existe stock para ese libro.")
            modelo.cantidad = stock.cantidad
        return self.leer_por_libro(stock.libro.id)

    def eliminar(self, libro_id: int) -> bool:
        with self.db.transaccion() as sesion:
            modelo = sesion.get(StockModel, libro_id)
            if modelo is None:
                return False
            sesion.delete(modelo)
        return True


class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
    def __init__(self, db: ConexionDB):
        self.db = db

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        clave = (cotizacion.tipo_cotizacion.id, cotizacion.fecha)
        if self.leer_por_tipo_y_fecha(*clave) is not None:
            raise ValueError("Ya existe una cotización para ese tipo y fecha.")
        with self.db.transaccion() as sesion:
            sesion.add(CotizacionDolarModel(**_valores(cotizacion)))
        return self.leer_por_tipo_y_fecha(*clave)

    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: datetime.date) -> Optional[CotizacionDolar]:
        with self.db.crear_sesion() as sesion:
            modelo = sesion.execute(_consulta(sesion, CotizacionDolarModel).where(
                CotizacionDolarModel.tipo_cotizacion_id == tipo_id,
                CotizacionDolarModel.fecha == fecha)).scalar_one_or_none()
            return _entidad(modelo)

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        with self.db.crear_sesion() as sesion:
            modelos = sesion.execute(_consulta(sesion, CotizacionDolarModel).where(
                CotizacionDolarModel.tipo_cotizacion_id == tipo_id).order_by(CotizacionDolarModel.fecha)).scalars().all()
            return [_entidad(m) for m in modelos]

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        clave = (cotizacion.tipo_cotizacion.id, cotizacion.fecha)
        with self.db.transaccion() as sesion:
            modelo = sesion.get(CotizacionDolarModel, clave)
            if modelo is None:
                raise ValueError("No existe la cotización para actualizar.")
            modelo.compra = Decimal(str(cotizacion.compra))
            modelo.venta = Decimal(str(cotizacion.venta))
        return self.leer_por_tipo_y_fecha(*clave)

    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        with self.db.transaccion() as sesion:
            modelo = sesion.get(CotizacionDolarModel, (tipo_id, fecha))
            if modelo is None:
                return False
            sesion.delete(modelo)
        return True
