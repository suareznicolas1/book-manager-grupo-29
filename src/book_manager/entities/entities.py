import datetime

# ============================================================
# Entidad base
# ============================================================

class EntidadBase:
    def __init__(self, id: int):
        self.__id = id

    @property
    def id(self) -> int:
        return self.__id


# ============================================================
# Género
# ============================================================

class Genero(EntidadBase):
    def __init__(self, id: int, nombre: str):
        super().__init__(id)
        self.nombre = nombre

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre del género no puede estar vacío.")
        self.__nombre = valor.strip()


# ============================================================
# Editorial
# ============================================================

class Editorial(EntidadBase):
    def __init__(self, id: int, nombre: str):
        super().__init__(id)
        self.nombre = nombre

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre de la editorial no puede estar vacío.")
        self.__nombre = valor.strip()


# ============================================================
# Moneda
# ============================================================

class Moneda(EntidadBase):
    def __init__(self, id: int, codigo: str, nombre: str):
        super().__init__(id)
        self.codigo = codigo
        self.nombre = nombre

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El código de la moneda no puede estar vacío.")
        self.__codigo = valor.strip().upper()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre de la moneda no puede estar vacío.")
        self.__nombre = valor.strip()


# ============================================================
# Tipo de cotización
# ============================================================

class TipoCotizacion(EntidadBase):
    def __init__(self, id: int, nombre: str):
        super().__init__(id)
        self.nombre = nombre

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El tipo de cotización no puede estar vacío.")
        self.__nombre = valor.strip()


# ============================================================
# Libro
# ============================================================

class Libro(EntidadBase):
    def __init__(
        self,
        id: int,
        isbn: str,
        titulo: str,
        autor: str,
        editorial: Editorial,
        genero: Genero
    ):
        super().__init__(id)

        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.genero = genero

    @property
    def isbn(self) -> str:
        return self.__isbn

    @isbn.setter
    def isbn(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El ISBN no puede estar vacío.")
        self.__isbn = valor.strip()

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El título no puede estar vacío.")
        self.__titulo = valor.strip()

    @property
    def autor(self) -> str:
        return self.__autor

    @autor.setter
    def autor(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El autor no puede estar vacío.")
        self.__autor = valor.strip()

    @property
    def editorial(self) -> Editorial:
        return self.__editorial

    @editorial.setter
    def editorial(self, valor: Editorial):
        if not isinstance(valor, Editorial):
            raise TypeError("La editorial debe ser un objeto Editorial.")
        self.__editorial = valor

    @property
    def genero(self) -> Genero:
        return self.__genero

    @genero.setter
    def genero(self, valor: Genero):
        if not isinstance(valor, Genero):
            raise TypeError("El género debe ser un objeto Genero.")
        self.__genero = valor


# ============================================================
# Precio
# ============================================================

class Precio(EntidadBase):
    def __init__(
        self,
        id: int,
        libro: Libro,
        moneda: Moneda,
        valor: float
    ):
        super().__init__(id)

        self.libro = libro
        self.moneda = moneda
        self.valor = valor

    @property
    def libro(self) -> Libro:
        return self.__libro

    @libro.setter
    def libro(self, valor: Libro):
        if not isinstance(valor, Libro):
            raise TypeError("El libro debe ser un objeto Libro.")
        self.__libro = valor

    @property
    def moneda(self) -> Moneda:
        return self.__moneda

    @moneda.setter
    def moneda(self, valor: Moneda):
        if not isinstance(valor, Moneda):
            raise TypeError("La moneda debe ser un objeto Moneda.")
        self.__moneda = valor

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, valor: float):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__valor = valor


# ============================================================
# Stock
# ============================================================

class Stock:
    def __init__(self, libro: Libro, cantidad: int):
        self.libro = libro
        self.cantidad = cantidad

    @property
    def libro(self) -> Libro:
        return self.__libro

    @libro.setter
    def libro(self, valor: Libro):
        if not isinstance(valor, Libro):
            raise TypeError("El libro debe ser un objeto Libro.")
        self.__libro = valor

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int):
        if valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.__cantidad = valor


# ============================================================
# Cotización dólar
# ============================================================

class CotizacionDolar:
    def __init__(
        self,
        fecha: datetime.date,
        tipo_cotizacion: TipoCotizacion,
        compra: float,
        venta: float
    ):
        self.fecha = fecha
        self.tipo_cotizacion = tipo_cotizacion
        self.compra = compra
        self.venta = venta

    @property
    def fecha(self) -> datetime.date:
        return self.__fecha

    @fecha.setter
    def fecha(self, valor: datetime.date):
        if not isinstance(valor, datetime.date):
            raise TypeError("La fecha debe ser de tipo datetime.date.")
        self.__fecha = valor

    @property
    def tipo_cotizacion(self) -> TipoCotizacion:
        return self.__tipo_cotizacion

    @tipo_cotizacion.setter
    def tipo_cotizacion(self, valor: TipoCotizacion):
        if not isinstance(valor, TipoCotizacion):
            raise TypeError(
                "El tipo de cotización debe ser un objeto TipoCotizacion."
            )
        self.__tipo_cotizacion = valor

    @property
    def compra(self) -> float:
        return self.__compra

    @compra.setter
    def compra(self, valor: float):
        if valor <= 0:
            raise ValueError("La cotización de compra debe ser mayor a cero.")
        self.__compra = valor

    @property
    def venta(self) -> float:
        return self.__venta

    @venta.setter
    def venta(self, valor: float):
        if valor <= 0:
            raise ValueError("La cotización de venta debe ser mayor a cero.")
        self.__venta = valor