from typing import List
from book_manager.entities.entities import Libro
from book_manager.repositories.repositories import ILibroRepository

class LibroService:
    """Servicio para gestionar la lógica de negocio de los libros."""

    def __init__(self, libro_repositorio: ILibroRepository):
        # Inyección de dependencia del repositorio de libros
        self._libro_repositorio = libro_repositorio

    def crear_libro(self, titulo: str, autor: str) -> Libro:
        """Crea un nuevo libro con un ID autoincremental y lo guarda en el repositorio."""
        libros_existentes = self._libro_repositorio.leer_todos()
        nuevo_id = len(libros_existentes) + 1
        nuevo_libro = Libro(nuevo_id, titulo, autor)
        return self._libro_repositorio.crear(nuevo_libro)

    def obtener_todos_los_libros(self) -> List[Libro]:
        """Obtiene la lista completa de libros registrados."""
        return self._libro_repositorio.leer_todos()