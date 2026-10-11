"""Conexión a la base de datos mediante SQLAlchemy."""

from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class ConexionDB:
    """Configura el motor de base de datos y crea sesiones."""

    def __init__(self, url: str | None = None) -> None:
        if url is None:
            raiz = Path(__file__).resolve().parents[3]
            ruta_db = raiz / "book_manager.db"
            url = f"sqlite:///{ruta_db.as_posix()}"

        self.engine: Engine = create_engine(url)
        self._fabrica_sesiones = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    def crear_sesion(self) -> Session:
        """Devuelve una sesión para consultar o modificar datos."""
        return self._fabrica_sesiones()

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