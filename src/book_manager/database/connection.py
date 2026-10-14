
"""Conexión a la base de datos mediante SQLAlchemy."""

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class ConexionDB:
    """Configura el motor de base de datos y crea sesiones."""

    def __init__(self, url: str | None = None) -> None:
        # Cargar las variables de entorno desde el archivo .env
        raiz = Path(__file__).resolve().parents[3]
        load_dotenv(raiz / ".env")

        # Priorizar la URL recibida por parámetro
        if url is None:
            url = os.getenv("DATABASE_URL")

        # Si no hay DATABASE_URL, utilizar SQLite
        if not url:
            ruta_db = raiz / "book_manager.db"
            url = f"sqlite:///{ruta_db.as_posix()}"

        # Crear el motor SQLAlchemy
        self.engine: Engine = create_engine(url)

        self._fabrica_sesiones = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    def crear_sesion(self) -> Session:
        """Devuelve una sesión para consultar o modificar datos."""
        return self._fabrica_sesiones()

    @contextmanager
    def transaccion(self) -> Iterator[Session]:
        """Context manager que maneja una transacción completa.

        Abre una sesión y la entrega al bloque ``with``. Si el bloque termina
        sin errores se confirma con ``commit``; si ocurre una excepción se
        deshacen los cambios con ``rollback`` y se vuelve a lanzar.
        En ambos casos la sesión se cierra al final.

        Yields:
            Session: sesión activa dentro de la transacción.

        Example:
            with db.transaccion() as sesion:
                sesion.add(GeneroModel(nombre="Novela"))
        """
        sesion = self.crear_sesion()
        try:
            yield sesion
            sesion.commit()
        except Exception:
            sesion.rollback()
            raise
        finally:
            sesion.close()

    def verificar_conexion(self) -> bool:
        """Ejecuta una consulta sencilla para comprobar la conexión."""
        with self.engine.connect() as conexion:
            resultado = conexion.execute(text("SELECT 1")).scalar_one()
            return resultado == 1

    def cerrar(self) -> None:
        """Libera las conexiones del motor."""
        self.engine.dispose()


if __name__ == "__main__":
    db = ConexionDB()
    print("Conexión correcta:", db.verificar_conexion())
    db.cerrar()
