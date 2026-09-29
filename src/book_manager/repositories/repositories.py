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


class RepositorioStock(IRepositorioStock):
    def __init__(self):
        self._datos = {}

    def crear(self, stock: Stock) -> Stock:
        # Cambiamos stock.libro_id por stock.libro.id
        if stock.libro.id in self._datos:
            raise ValueError(f"Ya existe un registro de stock para el libro {stock.libro.id}.")
        self._datos[stock.libro.id] = stock
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional['Stock']:
        return self._datos.get(libro_id)

    def actualizar(self, stock: 'Stock') -> 'Stock':
        # Cambiamos stock.libro_id por stock.libro.id
        if stock.libro.id not in self._datos:
            raise ValueError(f"No se encontró el stock para actualizar (Libro ID {stock.libro.id}).")
        self._datos[stock.libro.id] = stock
        return stock

    def eliminar(self, libro_id: int) -> bool:
        if libro_id in self._datos:
            del self._datos[libro_id]
            return True
        return False


class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
    def __init__(self):
        self._datos = {}

    def crear(self, cotizacion: 'CotizacionDolar') -> 'CotizacionDolar':
        clave = (cotizacion.tipo_cotizacion.id, cotizacion.fecha)
        if clave in self._datos:
            raise ValueError("Ya existe una cotización para este tipo y fecha.")
        self._datos[clave] = cotizacion
        return cotizacion

    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: datetime.date) -> Optional['CotizacionDolar']:
        clave = (tipo_id, fecha)
        return self._datos.get(clave)

    def leer_historico_por_tipo(self, tipo_id: int) -> List['CotizacionDolar']:
        return [
            cot for cot in self._datos.values()
            if cot.tipo_cotizacion.id == tipo_id
        ]

    def actualizar(self, cotizacion: 'CotizacionDolar') -> 'CotizacionDolar':
        clave = (cotizacion.tipo_cotizacion.id, cotizacion.fecha)
        if clave not in self._datos:
            raise ValueError("No se encontró la cotización para actualizar.")
        self._datos[clave] = cotizacion
        return cotizacion

    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        clave = (tipo_id, fecha)
        if clave in self._datos:
            del self._datos[clave]
            return True
        return False
    
    
class RepositorioGenerico(IRepositorio[T]):
    def __init__(self):
        self._datos: dict[int, T] = {}

    def crear(self, entidad: T) -> T:
        if not getattr(entidad, "id", None) or entidad.id == 0:
            nuevo_id = max(self._datos.keys(), default=0) + 1
            setattr(entidad, "_EntidadBase__id", nuevo_id)

        if entidad.id in self._datos:
            raise ValueError(f"Ya existe una entidad con el ID {entidad.id}.")

        self._datos[entidad.id] = entidad
        return entidad

    def leer_por_id(self, id: int) -> Optional[T]:
        return self._datos.get(id)

    def leer_todos(self) -> List[T]:
        return list(self._datos.values())

    def actualizar(self, entidad: T) -> T:
        if entidad.id not in self._datos:
            raise ValueError(f"No se encontró la entidad con ID {entidad.id}.")
        self._datos[entidad.id] = entidad
        return entidad

    def eliminar(self, id: int) -> bool:
        if id in self._datos:
            del self._datos[id]
            return True
        return False