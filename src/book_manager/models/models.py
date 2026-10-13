"""Modelos ORM (tablas) del sistema Book Manager con SQLAlchemy."""

import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    Engine,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Clase base de la que heredan todos los modelos."""


class GeneroModel(Base):
    """Tabla de géneros literarios."""

    __tablename__ = "generos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)

    libros: Mapped[list["LibroModel"]] = relationship(back_populates="genero")


class EditorialModel(Base):
    """Tabla de editoriales."""

    __tablename__ = "editoriales"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True)

    libros: Mapped[list["LibroModel"]] = relationship(
        back_populates="editorial"
    )


class MonedaModel(Base):
    """Tabla de monedas en las que se expresan los precios."""

    __tablename__ = "monedas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(10), unique=True)
    nombre: Mapped[str] = mapped_column(String(100))

    precios: Mapped[list["PrecioModel"]] = relationship(
        back_populates="moneda"
    )


class TipoCotizacionModel(Base):
    """Tabla de tipos de cotización del dólar (Oficial, Blue, MEP...)."""

    __tablename__ = "tipos_cotizacion"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)

    cotizaciones: Mapped[list["CotizacionDolarModel"]] = relationship(
        back_populates="tipo_cotizacion"
    )


class LibroModel(Base):
    """Tabla de libros. Pertenece a una editorial y a un género."""

    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(String(20), unique=True)
    titulo: Mapped[str] = mapped_column(String(255))
    autor: Mapped[str] = mapped_column(String(150))
    editorial_id: Mapped[int] = mapped_column(ForeignKey("editoriales.id"))
    genero_id: Mapped[int] = mapped_column(ForeignKey("generos.id"))

    editorial: Mapped[EditorialModel] = relationship(back_populates="libros")
    genero: Mapped[GeneroModel] = relationship(back_populates="libros")
    precios: Mapped[list["PrecioModel"]] = relationship(
        back_populates="libro",
        cascade="all, delete-orphan",
    )
    stock: Mapped["StockModel | None"] = relationship(
        back_populates="libro",
        cascade="all, delete-orphan",
        uselist=False,
    )


class PrecioModel(Base):
    """Tabla de precios: un libro tiene a lo sumo un precio por moneda."""

    __tablename__ = "precios"
    __table_args__ = (
        UniqueConstraint("libro_id", "moneda_id", name="uq_precio_libro_moneda"),
        CheckConstraint("valor >= 0", name="ck_precio_valor_positivo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    libro_id: Mapped[int] = mapped_column(ForeignKey("libros.id"))
    moneda_id: Mapped[int] = mapped_column(ForeignKey("monedas.id"))
    valor: Mapped[Decimal] = mapped_column(Numeric(14, 2))

    libro: Mapped[LibroModel] = relationship(back_populates="precios")
    moneda: Mapped[MonedaModel] = relationship(back_populates="precios")


class StockModel(Base):
    """Tabla de stock: relación 1 a 1 con libro (la clave es el libro)."""

    __tablename__ = "stock"
    __table_args__ = (
        CheckConstraint("cantidad >= 0", name="ck_stock_cantidad_positiva"),
    )

    libro_id: Mapped[int] = mapped_column(
        ForeignKey("libros.id"),
        primary_key=True,
        autoincrement=False,
    )
    cantidad: Mapped[int] = mapped_column(default=0)

    libro: Mapped[LibroModel] = relationship(back_populates="stock")


class CotizacionDolarModel(Base):
    """Tabla de cotizaciones: una por tipo y fecha (clave compuesta)."""

    __tablename__ = "cotizaciones_dolar"
    __table_args__ = (
        CheckConstraint("compra > 0", name="ck_cotizacion_compra_positiva"),
        CheckConstraint("venta > 0", name="ck_cotizacion_venta_positiva"),
    )

    tipo_cotizacion_id: Mapped[int] = mapped_column(
        ForeignKey("tipos_cotizacion.id"),
        primary_key=True,
        autoincrement=False,
    )
    fecha: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    compra: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    venta: Mapped[Decimal] = mapped_column(Numeric(14, 2))

    tipo_cotizacion: Mapped[TipoCotizacionModel] = relationship(
        back_populates="cotizaciones"
    )


def crear_tablas(engine: Engine) -> None:
    """Crea en la base todas las tablas definidas que aún no existan.

    Args:
        engine (Engine): motor de SQLAlchemy sobre el que se crean las tablas.
    """
    Base.metadata.create_all(engine)
