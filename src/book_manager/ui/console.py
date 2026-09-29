import datetime
from typing import Optional

from book_manager.entities.entities import (
    Libro,
    Genero,
    Editorial,
    Moneda,
    TipoCotizacion,
    Precio,
    Stock,
    CotizacionDolar,
)
from book_manager.repositories.repositories import (
    RepositorioGenerico,
    RepositorioStock,
    RepositorioCotizacionDolar,
)


class ConsoleUI:
    """Interfaz gráfica de consola para la gestión interactiva del sistema Book Manager."""

    def __init__(
        self,
        repo_generos: RepositorioGenerico,
        repo_editoriales: RepositorioGenerico,
        repo_monedas: RepositorioGenerico,
        repo_tipos_cotizacion: RepositorioGenerico,
        repo_libros: RepositorioGenerico,
        repo_precios: RepositorioGenerico,
        repo_stock: RepositorioStock,
        repo_cotizaciones: RepositorioCotizacionDolar,
    ) -> None:
        self.repo_generos = repo_generos
        self.repo_editoriales = repo_editoriales
        self.repo_monedas = repo_monedas
        self.repo_tipos_cotizacion = repo_tipos_cotizacion
        self.repo_libros = repo_libros
        self.repo_precios = repo_precios
        self.repo_stock = repo_stock
        self.repo_cotizaciones = repo_cotizaciones

    # -------------------------------------------------------------------------
    # Auxiliares de Lectura
    # -------------------------------------------------------------------------
    @staticmethod
    def _leer_int(mensaje: str) -> int:
        while True:
            try:
                return int(input(mensaje).strip())
            except ValueError:
                print("❌ Error: Debe ingresar un número entero válido.")

    @staticmethod
    def _leer_float(mensaje: str) -> float:
        while True:
            try:
                return float(input(mensaje).strip())
            except ValueError:
                print("❌ Error: Debe ingresar un número decimal válido.")

    @staticmethod
    def _leer_fecha(mensaje: str) -> datetime.date:
        while True:
            entrada = input(mensaje + " (AAAA-MM-DD): ").strip()
            try:
                return datetime.datetime.strptime(entrada, "%Y-%m-%d").date()
            except ValueError:
                print("❌ Error: Formato de fecha inválido. Utilice AAAA-MM-DD.")

    # -------------------------------------------------------------------------
    # Menú Principal
    # -------------------------------------------------------------------------
    def iniciar(self) -> None:
        while True:
            print("\n" + "=" * 50)
            print("        BOOK MANAGER - SISTEMA DE GESTIÓN       ")
            print("=" * 50)
            print("1. CRUD Géneros")
            print("2. CRUD Editoriales")
            print("3. CRUD Monedas")
            print("4. CRUD Tipos de Cotización")
            print("5. CRUD Libros")
            print("6. CRUD Precios")
            print("7. CRUD Stock")
            print("8. CRUD Cotizaciones del Dólar")
            print("0. Salir")
            print("-" * 50)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._menu_genero()
            elif opcion == "2":
                self._menu_editorial()
            elif opcion == "3":
                self._menu_moneda()
            elif opcion == "4":
                self._menu_tipo_cotizacion()
            elif opcion == "5":
                self._menu_libro()
            elif opcion == "6":
                self._menu_precio()
            elif opcion == "7":
                self._menu_stock()
            elif opcion == "8":
                self._menu_cotizacion_dolar()
            elif opcion == "0":
                print("\n¡Gracias por utilizar Book Manager!")
                break
            else:
                print("❌ Opción no válida. Intente nuevamente.")

    # -------------------------------------------------------------------------
    # 1. CRUD Géneros
    # -------------------------------------------------------------------------
    def _menu_genero(self) -> None:
        while True:
            print("\n--- GESTIÓN DE GÉNEROS ---")
            print("1. Crear Género")
            print("2. Listar Géneros")
            print("3. Buscar Género por ID")
            print("4. Actualizar Género")
            print("5. Eliminar Género")
            print("0. Volver")

            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                break

            try:
                if opcion == "1":
                    id_g = self._leer_int("ID del Género: ")
                    nombre = input("Nombre: ").strip()
                    g = Genero(id=id_g, nombre=nombre)
                    self.repo_generos.crear(g)
                    print("✅ Género creado con éxito.")

                elif opcion == "2":
                    generos = self.repo_generos.leer_todos()
                    if not generos:
                        print("No hay géneros registrados.")
                    for g in generos:
                        print(f"ID: {g.id} | Nombre: {g.nombre}")

                elif opcion == "3":
                    id_g = self._leer_int("ID a buscar: ")
                    g = self.repo_generos.leer_por_id(id_g)
                    if g:
                        print(f"ID: {g.id} | Nombre: {g.nombre}")
                    else:
                        print("❌ Género no encontrado.")

                elif opcion == "4":
                    id_g = self._leer_int("ID del Género a actualizar: ")
                    nombre = input("Nuevo Nombre: ").strip()
                    g = Genero(id=id_g, nombre=nombre)
                    self.repo_generos.actualizar(g)
                    print("✅ Género actualizado con éxito.")

                elif opcion == "5":
                    id_g = self._leer_int("ID a eliminar: ")
                    if self.repo_generos.eliminar(id_g):
                        print("✅ Género eliminado con éxito.")
                    else:
                        print("❌ No se encontró el género.")
            except Exception as e:
                print(f"❌ Error: {e}")

    # -------------------------------------------------------------------------
    # 2. CRUD Editoriales
    # -------------------------------------------------------------------------
    def _menu_editorial(self) -> None:
        while True:
            print("\n--- GESTIÓN DE EDITORIALES ---")
            print("1. Crear Editorial")
            print("2. Listar Editoriales")
            print("3. Buscar Editorial por ID")
            print("4. Actualizar Editorial")
            print("5. Eliminar Editorial")
            print("0. Volver")

            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                break

            try:
                if opcion == "1":
                    id_e = self._leer_int("ID de la Editorial: ")
                    nombre = input("Nombre: ").strip()
                    e = Editorial(id=id_e, nombre=nombre)
                    self.repo_editoriales.crear(e)
                    print("✅ Editorial creada con éxito.")

                elif opcion == "2":
                    editoriales = self.repo_editoriales.leer_todos()
                    if not editoriales:
                        print("No hay editoriales registradas.")
                    for e in editoriales:
                        print(f"ID: {e.id} | Nombre: {e.nombre}")

                elif opcion == "3":
                    id_e = self._leer_int("ID a buscar: ")
                    e = self.repo_editoriales.leer_por_id(id_e)
                    if e:
                        print(f"ID: {e.id} | Nombre: {e.nombre}")
                    else:
                        print("❌ Editorial no encontrada.")

                elif opcion == "4":
                    id_e = self._leer_int("ID de la Editorial a actualizar: ")
                    nombre = input("Nuevo Nombre: ").strip()
                    e = Editorial(id=id_e, nombre=nombre)
                    self.repo_editoriales.actualizar(e)
                    print("✅ Editorial actualizada con éxito.")

                elif opcion == "5":
                    id_e = self._leer_int("ID a eliminar: ")
                    if self.repo_editoriales.eliminar(id_e):
                        print("✅ Editorial eliminada con éxito.")
                    else:
                        print("❌ No se encontró la editorial.")
            except Exception as e:
                print(f"❌ Error: {e}")

    # -------------------------------------------------------------------------
    # 3. CRUD Monedas
    # -------------------------------------------------------------------------
    def _menu_moneda(self) -> None:
        while True:
            print("\n--- GESTIÓN DE MONEDAS ---")
            print("1. Crear Moneda")
            print("2. Listar Monedas")
            print("3. Buscar Moneda por ID")
            print("4. Actualizar Moneda")
            print("5. Eliminar Moneda")
            print("0. Volver")

            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                break

            try:
                if opcion == "1":
                    id_m = self._leer_int("ID de la Moneda: ")
                    codigo = input("Código (ej. ARS, USD): ").strip()
                    nombre = input("Nombre: ").strip()
                    m = Moneda(id=id_m, codigo=codigo, nombre=nombre)
                    self.repo_monedas.crear(m)
                    print("✅ Moneda creada con éxito.")

                elif opcion == "2":
                    monedas = self.repo_monedas.leer_todos()
                    if not monedas:
                        print("No hay monedas registradas.")
                    for m in monedas:
                        print(f"ID: {m.id} | Código: {m.codigo} | Nombre: {m.nombre}")

                elif opcion == "3":
                    id_m = self._leer_int("ID a buscar: ")
                    m = self.repo_monedas.leer_por_id(id_m)
                    if m:
                        print(f"ID: {m.id} | Código: {m.codigo} | Nombre: {m.nombre}")
                    else:
                        print("❌ Moneda no encontrada.")

                elif opcion == "4":
                    id_m = self._leer_int("ID a actualizar: ")
                    codigo = input("Nuevo Código: ").strip()
                    nombre = input("Nuevo Nombre: ").strip()
                    m = Moneda(id=id_m, codigo=codigo, nombre=nombre)
                    self.repo_monedas.actualizar(m)
                    print("✅ Moneda actualizada con éxito.")

                elif opcion == "5":
                    id_m = self._leer_int("ID a eliminar: ")
                    if self.repo_monedas.eliminar(id_m):
                        print("✅ Moneda eliminada con éxito.")
                    else:
                        print("❌ No se encontró la moneda.")
            except Exception as e:
                print(f"❌ Error: {e}")

    # -------------------------------------------------------------------------
    # 4. CRUD Tipos de Cotización
    # -------------------------------------------------------------------------
    def _menu_tipo_cotizacion(self) -> None:
        while True:
            print("\n--- GESTIÓN DE TIPOS DE COTIZACIÓN ---")
            print("1. Crear Tipo de Cotización")
            print("2. Listar Tipos de Cotización")
            print("3. Buscar por ID")
            print("4. Actualizar Tipo de Cotización")
            print("5. Eliminar Tipo de Cotización")
            print("0. Volver")

            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                break

            try:
                if opcion == "1":
                    id_tc = self._leer_int("ID del Tipo: ")
                    nombre = input("Nombre (ej. Oficial, Blue, MEP): ").strip()
                    tc = TipoCotizacion(id=id_tc, nombre=nombre)
                    self.repo_tipos_cotizacion.crear(tc)
                    print("✅ Tipo de cotización creado.")

                elif opcion == "2":
                    tipos = self.repo_tipos_cotizacion.leer_todos()
                    if not tipos:
                        print("No hay tipos de cotización registrados.")
                    for tc in tipos:
                        print(f"ID: {tc.id} | Nombre: {tc.nombre}")

                elif opcion == "3":
                    id_tc = self._leer_int("ID a buscar: ")
                    tc = self.repo_tipos_cotizacion.leer_por_id(id_tc)
                    if tc:
                        print(f"ID: {tc.id} | Nombre: {tc.nombre}")
                    else:
                        print("❌ Tipo de cotización no encontrado.")

                elif opcion == "4":
                    id_tc = self._leer_int("ID a actualizar: ")
                    nombre = input("Nuevo Nombre: ").strip()
                    tc = TipoCotizacion(id=id_tc, nombre=nombre)
                    self.repo_tipos_cotizacion.actualizar(tc)
                    print("✅ Tipo de cotización actualizado.")

                elif opcion == "5":
                    id_tc = self._leer_int("ID a eliminar: ")
                    if self.repo_tipos_cotizacion.eliminar(id_tc):
                        print("✅ Tipo de cotización eliminado.")
                    else:
                        print("❌ No se encontró el registro.")
            except Exception as e:
                print(f"❌ Error: {e}")

    # -------------------------------------------------------------------------
    # 5. CRUD Libros
    # -------------------------------------------------------------------------
    def _menu_libro(self) -> None:
        while True:
            print("\n--- GESTIÓN DE LIBROS ---")
            print("1. Crear Libro")
            print("2. Listar Libros")
            print("3. Buscar Libro por ID")
            print("4. Actualizar Libro")
            print("5. Eliminar Libro")
            print("0. Volver")

            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                break

            try:
                if opcion == "1":
                    id_l = self._leer_int("ID del Libro: ")
                    isbn = input("ISBN: ").strip()
                    titulo = input("Título: ").strip()
                    autor = input("Autor: ").strip()

                    id_e = self._leer_int("ID de la Editorial: ")
                    editorial = self.repo_editoriales.leer_por_id(id_e)
                    if not editorial:
                        print("❌ La editorial no existe.")
                        continue

                    id_g = self._leer_int("ID del Género: ")
                    genero = self.repo_generos.leer_por_id(id_g)
                    if not genero:
                        print("❌ El género no existe.")
                        continue

                    libro = Libro(
                        id=id_l,
                        isbn=isbn,
                        titulo=titulo,
                        autor=autor,
                        editorial=editorial,
                        genero=genero,
                    )
                    self.repo_libros.crear(libro)
                    print("✅ Libro creado con éxito.")

                elif opcion == "2":
                    libros = self.repo_libros.leer_todos()
                    if not libros:
                        print("No hay libros registrados.")
                    for l in libros:
                        print(
                            f"ID: {l.id} | ISBN: {l.isbn} | Título: {l.titulo} | "
                            f"Autor: {l.autor} | Editorial: {l.editorial.nombre} | "
                            f"Género: {l.genero.nombre}"
                        )

                elif opcion == "3":
                    id_l = self._leer_int("ID a buscar: ")
                    l = self.repo_libros.leer_por_id(id_l)
                    if l:
                        print(
                            f"ID: {l.id} | ISBN: {l.isbn} | Título: {l.titulo} | "
                            f"Autor: {l.autor} | Editorial: {l.editorial.nombre} | "
                            f"Género: {l.genero.nombre}"
                        )
                    else:
                        print("❌ Libro no encontrado.")

                elif opcion == "4":
                    id_l = self._leer_int("ID del Libro a actualizar: ")
                    isbn = input("Nuevo ISBN: ").strip()
                    titulo = input("Nuevo Título: ").strip()
                    autor = input("Nuevo Autor: ").strip()

                    id_e = self._leer_int("Nuevo ID de Editorial: ")
                    editorial = self.repo_editoriales.leer_por_id(id_e)
                    if not editorial:
                        print("❌ La editorial especificada no existe.")
                        continue

                    id_g = self._leer_int("Nuevo ID de Género: ")
                    genero = self.repo_generos.leer_por_id(id_g)
                    if not genero:
                        print("❌ El género especificado no existe.")
                        continue

                    libro = Libro(
                        id=id_l,
                        isbn=isbn,
                        titulo=titulo,
                        autor=autor,
                        editorial=editorial,
                        genero=genero,
                    )
                    self.repo_libros.actualizar(libro)
                    print("✅ Libro actualizado con éxito.")

                elif opcion == "5":
                    id_l = self._leer_int("ID a eliminar: ")
                    if self.repo_libros.eliminar(id_l):
                        print("✅ Libro eliminado con éxito.")
                    else:
                        print("❌ No se encontró el libro.")
            except Exception as e:
                print(f"❌ Error: {e}")

    # -------------------------------------------------------------------------
    # 6. CRUD Precios
    # -------------------------------------------------------------------------
    def _menu_precio(self) -> None:
        while True:
            print("\n--- GESTIÓN DE PRECIOS ---")
            print("1. Registrar Precio")
            print("2. Listar Precios")
            print("3. Buscar Precio por ID")
            print("4. Actualizar Precio")
            print("5. Eliminar Precio")
            print("0. Volver")

            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                break

            try:
                if opcion == "1":
                    id_p = self._leer_int("ID del Precio: ")

                    id_l = self._leer_int("ID del Libro: ")
                    libro = self.repo_libros.leer_por_id(id_l)
                    if not libro:
                        print("❌ El libro especificado no existe.")
                        continue

                    id_m = self._leer_int("ID de la Moneda: ")
                    moneda = self.repo_monedas.leer_por_id(id_m)
                    if not moneda:
                        print("❌ La moneda especificada no existe.")
                        continue

                    valor = self._leer_float("Valor/Monto: ")
                    p = Precio(id=id_p, libro=libro, moneda=moneda, valor=valor)
                    self.repo_precios.crear(p)
                    print("✅ Precio registrado con éxito.")

                elif opcion == "2":
                    precios = self.repo_precios.leer_todos()
                    if not precios:
                        print("No hay precios registrados.")
                    for p in precios:
                        print(
                            f"ID: {p.id} | Libro: {p.libro.titulo} | "
                            f"Moneda: {p.moneda.codigo} | Valor: ${p.valor:.2f}"
                        )

                elif opcion == "3":
                    id_p = self._leer_int("ID a buscar: ")
                    p = self.repo_precios.leer_por_id(id_p)
                    if p:
                        print(
                            f"ID: {p.id} | Libro: {p.libro.titulo} | "
                            f"Moneda: {p.moneda.codigo} | Valor: ${p.valor:.2f}"
                        )
                    else:
                        print("❌ Precio no encontrado.")

                elif opcion == "4":
                    id_p = self._leer_int("ID a actualizar: ")

                    id_l = self._leer_int("Nuevo ID del Libro: ")
                    libro = self.repo_libros.leer_por_id(id_l)
                    if not libro:
                        print("❌ Libro inexistente.")
                        continue

                    id_m = self._leer_int("Nuevo ID de Moneda: ")
                    moneda = self.repo_monedas.leer_por_id(id_m)
                    if not moneda:
                        print("❌ Moneda inexistente.")
                        continue

                    valor = self._leer_float("Nuevo Valor/Monto: ")
                    p = Precio(id=id_p, libro=libro, moneda=moneda, valor=valor)
                    self.repo_precios.actualizar(p)
                    print("✅ Precio actualizado.")

                elif opcion == "5":
                    id_p = self._leer_int("ID a eliminar: ")
                    if self.repo_precios.eliminar(id_p):
                        print("✅ Precio eliminado.")
                    else:
                        print("❌ Registro no encontrado.")
            except Exception as e:
                print(f"❌ Error: {e}")

    # -------------------------------------------------------------------------
    # 7. CRUD Stock
    # -------------------------------------------------------------------------
    def _menu_stock(self) -> None:
        while True:
            print("\n--- GESTIÓN DE STOCK ---")
            print("1. Registrar Stock")
            print("2. Buscar Stock por ID de Libro")
            print("3. Actualizar Stock")
            print("4. Eliminar Registro de Stock")
            print("0. Volver")

            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                break

            try:
                if opcion == "1":
                    id_l = self._leer_int("ID del Libro: ")
                    libro = self.repo_libros.leer_por_id(id_l)
                    if not libro:
                        print("❌ El libro especificado no existe.")
                        continue

                    cant = self._leer_int("Cantidad en Stock: ")
                    stk = Stock(libro=libro, cantidad=cant)
                    self.repo_stock.crear(stk)
                    print("✅ Stock registrado con éxito.")

                elif opcion == "2":
                    id_l = self._leer_int("ID del Libro a consultar: ")
                    stk = self.repo_stock.leer_por_libro(id_l)
                    if stk:
                        print(
                            f"Libro: {stk.libro.titulo} | Cantidad Disponible: {stk.cantidad}"
                        )
                    else:
                        print("❌ No hay registro de stock para ese libro.")

                elif opcion == "3":
                    id_l = self._leer_int("ID del Libro a actualizar stock: ")
                    libro = self.repo_libros.leer_por_id(id_l)
                    if not libro:
                        print("❌ Libro no encontrado.")
                        continue

                    cant = self._leer_int("Nueva Cantidad: ")
                    stk = Stock(libro=libro, cantidad=cant)
                    self.repo_stock.actualizar(stk)
                    print("✅ Stock actualizado.")

                elif opcion == "4":
                    id_l = self._leer_int("ID del Libro a eliminar stock: ")
                    if self.repo_stock.eliminar(id_l):
                        print("✅ Stock eliminado con éxito.")
                    else:
                        print("❌ Registro de stock no encontrado.")
            except Exception as e:
                print(f"❌ Error: {e}")

    # -------------------------------------------------------------------------
    # 8. CRUD Cotizaciones del Dólar
    # -------------------------------------------------------------------------
    def _menu_cotizacion_dolar(self) -> None:
        while True:
            print("\n--- GESTIÓN DE COTIZACIONES DEL DÓLAR ---")
            print("1. Registrar Cotización")
            print("2. Buscar por Tipo y Fecha")
            print("3. Ver Histórico por Tipo")
            print("4. Actualizar Cotización")
            print("5. Eliminar Cotización")
            print("0. Volver")

            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                break

            try:
                if opcion == "1":
                    id_tc = self._leer_int("ID del Tipo de Cotización: ")
                    tipo_cot = self.repo_tipos_cotizacion.leer_por_id(id_tc)
                    if not tipo_cot:
                        print("❌ Tipo de cotización inexistente.")
                        continue

                    fecha = self._leer_fecha("Fecha")
                    compra = self._leer_float("Valor Compra: ")
                    venta = self._leer_float("Valor Venta: ")

                    cot = CotizacionDolar(
                        fecha=fecha,
                        tipo_cotizacion=tipo_cot,
                        compra=compra,
                        venta=venta,
                    )
                    self.repo_cotizaciones.crear(cot)
                    print("✅ Cotización registrada con éxito.")

                elif opcion == "2":
                    id_tc = self._leer_int("ID del Tipo de Cotización: ")
                    fecha = self._leer_fecha("Fecha")
                    cot = self.repo_cotizaciones.leer_por_tipo_y_fecha(id_tc, fecha)
                    if cot:
                        print(
                            f"Tipo: {cot.tipo_cotizacion.nombre} | Fecha: {cot.fecha} | "
                            f"Compra: ${cot.compra:.2f} | Venta: ${cot.venta:.2f}"
                        )
                    else:
                        print("❌ No se encontró cotización para ese tipo y fecha.")

                elif opcion == "3":
                    id_tc = self._leer_int("ID del Tipo de Cotización: ")
                    historico = self.repo_cotizaciones.leer_historico_por_tipo(id_tc)
                    if not historico:
                        print("No hay histórico para el tipo seleccionado.")
                    for cot in historico:
                        print(
                            f"Fecha: {cot.fecha} | Tipo: {cot.tipo_cotizacion.nombre} | "
                            f"Compra: ${cot.compra:.2f} | Venta: ${cot.venta:.2f}"
                        )

                elif opcion == "4":
                    id_tc = self._leer_int("ID del Tipo de Cotización: ")
                    tipo_cot = self.repo_tipos_cotizacion.leer_por_id(id_tc)
                    if not tipo_cot:
                        print("❌ Tipo de cotización inexistente.")
                        continue

                    fecha = self._leer_fecha("Fecha")
                    compra = self._leer_float("Nuevo Valor Compra: ")
                    venta = self._leer_float("Nuevo Valor Venta: ")

                    cot = CotizacionDolar(
                        fecha=fecha,
                        tipo_cotizacion=tipo_cot,
                        compra=compra,
                        venta=venta,
                    )
                    self.repo_cotizaciones.actualizar(cot)
                    print("✅ Cotización actualizada.")

                elif opcion == "5":
                    id_tc = self._leer_int("ID del Tipo de Cotización: ")
                    fecha = self._leer_fecha("Fecha")
                    if self.repo_cotizaciones.eliminar(id_tc, fecha):
                        print("✅ Cotización eliminada.")
                    else:
                        print("❌ Cotización no encontrada.")
            except Exception as e:
                print(f"❌ Error: {e}")