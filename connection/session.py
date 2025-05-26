"""
    **session.py**\n
    Modulo con el proposito de realizar las diversas conexiones con la base de
    datos, esto con el proposito de realizar todos los selects que serán utilizados
    ya sea para las tablas de la interfaz grafica de la aplicacion, o de las demas
    funciones dentro de todo el sistema\n

    **Imports del modulo**\n
    traceback -----> Usado para verificar errores fantasma\n
    sqlalchemy.orm -----> Usado para crear la session con la base de datos y
                          para las subconsultas\n
    sqlalchemy -------> Usado para traer los select, func, or_ y distinct\n
    modulo models -----> Se importo el modulo local models, el cual contiene todas las
                        las tablas mapeadas de la base de datos, ademas de su respectiva
                        conexion con la base de datos
"""

import traceback
from datetime import date
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, func, or_, distinct, update, extract
from sql.models import engine
from sql.models import (Usuario, Libro, Estado_Libro,
                        Estado_Impresion, Estado_Prestamo, Prestamos,
                        Impresiones, CopiasLibros)


with Session(engine) as session:
    """
    **With de Session**\n
    Especifica que, todas las funciones que estan dentro de este with
    solamente se ejecuten mientras la conexio esta activa.
    """

    def select_libros_available(nombre= None, 
                        autor= None, 
                        Editorial= None, 
                        SectorBiblio= None,
                        SectorEstanteria= None, 
                        Estado_= None,
                        offset=None,
                        limit=None):
        """
        **Funcion select_libros_avaible**\n
        Permite obtener todos los libros que existen en la base de datos, segun los parametros.\n

        **Parametros**\n
        nombre: str | None\n
        autor: str | None\n
        Editorial: str | None\n
        SectorBiblio: str | None\n
        SectorEstanteria: str | None\n
        Estado: str | None\n
        offset: int | None\n
        limit: int | None\n
        
        **Retorna**\n
        libro: Objetos Libro
        """
        try:
            # Subconsulta: obtener el último préstamo por copia
            ultimo_prestamo = (
                select(
                    Prestamos.copia_id,
                    func.max(Prestamos.id_prestamos).label("ultimo_prestamo_id")
                )
                .group_by(Prestamos.copia_id)
                .subquery()
            )

            p_alias = aliased(Prestamos)

            # Comenzamos a construir la consulta
            query = (
                select(
                    Libro.nombre_libro,
                    Libro.autor,
                    Libro.editorial,
                    Libro.fecha_entrada,
                    Libro.sector_biblioteca,
                    Libro.sector_estanteria,
                    Estado_Libro.estado_libro,
                    func.count(CopiasLibros.id_copia).label("stock")
                )
                .join(CopiasLibros.libro)
                .join(CopiasLibros.estado)
                .outerjoin(ultimo_prestamo, CopiasLibros.id_copia == ultimo_prestamo.c.copia_id)
                .outerjoin(p_alias, p_alias.id_prestamos == ultimo_prestamo.c.ultimo_prestamo_id)
                .where(
                    or_(
                        p_alias.id_prestamos == None,
                        p_alias.estado_prestamo_id.in_([2, 3])  # Devuelto o Extraviado
                    )
            ).offset(offset).limit(limit))

            # Filtros opcionales
            if nombre:
                query = query.where(Libro.nombre_libro.ilike(f"%{nombre}%"))
            if autor:
                query = query.where(Libro.autor.ilike(f"%{autor}%"))
            if Editorial:
                query = query.where(Libro.editorial.ilike(f"%{Editorial}%"))
            if SectorBiblio:
                query = query.where(Libro.sector_biblioteca.ilike(f"%{SectorBiblio}%"))
            if SectorEstanteria:
                query = query.where(Libro.sector_estanteria.ilike(f"%{SectorEstanteria}%"))
            if Estado_:
                query = query.where(Estado_Libro.estado_libro.contains(Estado_))

            query = query.group_by(
                Libro.nombre_libro,
                Libro.autor,
                Libro.editorial,
                Libro.sector_biblioteca,
                Libro.sector_estanteria,
                Estado_Libro.estado_libro
            )

            result = session.execute(query)
            return result
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error {e}")

    def select_libros_equal(nombre, autor, editorial, sectorbiblioteca, sectorestanteria, fecha):
        """
        **Funcion select_libros_equal**\n
        Permite obtener todos los libros que tengan, en sus datos, los parametros pasados a la funcion\n

        **Parametros**\n
        nombre: str\n
        autor: str\n
        editorial: str\n
        sectorbiblioteca: str\n
        sectorestanteria: str\n
        fecha: str\n

        **Retorna**\n
        libro: Objetos Libro
        """
        try:
            query = (select(Libro)
                    .where(Libro.nombre_libro == nombre)
                    .where(Libro.autor == autor)
                    .where(Libro.editorial == editorial)
                    .where(Libro.sector_biblioteca == sectorbiblioteca)
                    .where(Libro.sector_estanteria == sectorestanteria)
                    .where(Libro.fecha_entrada == fecha))
                
            libros = session.execute(query).all()
            return libros
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_impresion_all(estado=None, papel=None, departamento=None, offset=None, limit=None):
        """
        **Funcion select_impresion_all**\n
        Permite obtener todas las impresiones que existan dentro de la tabla de Impresiones, a su vez
        cuenta con parametros para la implementacion de filtros\n

        **Parametros**\n
        estado: int | None\n
        papel: str | None\n
        departamento: str | None\n
        offset: int | None\n
        limit: int | None\n

        **Retorna**\n
        impresion: Objetos Impresion
        """
        try:
            query = (select(Impresiones, Estado_Impresion, Usuario)
                                        .join(Impresiones.estado_impresion)
                                        .join_from(Impresiones, Usuario, Impresiones.user_id == Usuario.id_user))
            if estado:
                query = query.where(Impresiones.estado_impresion_id == estado)

            if papel:
                query = query.where(Impresiones.tipo_papel == papel)
            if departamento:
                query = query.where(Usuario.curso.contains(departamento))
                    
            query = query.order_by(Impresiones.fecha_impresion.desc())
            query = query.offset(offset).limit(limit)
            impresion = session.execute(query).all()
            return impresion
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_prestamos_all(estado=None, 
                            rut=None, 
                            nombre_libro=None,
                            nombre_user=None,
                            curso=None,fecha=None,
                            offset=None,
                            limit=None):
        """
        **Funcion select_prestamos_all**\n
        Permite obtener todos los prestamos que corresponden en base a los parametros de esta\n

        **Parametros**\n
        estado: int | None\n
        rut: str | None\n
        nombre_libro: str | None\n
        nombre_user: str | None\n
        curso: str | None\n
        fecha: str | date | None\n
        offset: int | None\n
        limit: int | None\n

        **Retorna**\n
        prestamos: Objeto Prestamos
        """
        try:
            query = (select(Prestamos.fecha_inicio, Prestamos.fecha_termino, Estado_Prestamo.estado_prestamo,
                                            Usuario.nombre, Usuario.curso, Usuario.rut, Libro.nombre_libro,
                                            func.count(Libro.nombre_libro).label("stock"))
                                            .join(Prestamos.estado_prestamo)
                                            .join(Prestamos.user)
                                            .outerjoin(Prestamos.copia)
                                            .join_from(CopiasLibros, Libro, CopiasLibros.libro_id == Libro.id_libro)
                                            .group_by(Usuario.nombre, Libro.nombre_libro,Prestamos.fecha_inicio, Estado_Prestamo.estado_prestamo)
                                            .order_by(Prestamos.fecha_inicio.desc()))
            if estado:
                query = query.where(Prestamos.estado_prestamo_id == estado)
            if rut:
                query = query.where(Usuario.rut.contains(rut))
            if nombre_libro:
                query = query.where(Libro.nombre_libro.contains(nombre_libro))
            if nombre_user:
                query = query.where(Usuario.nombre.contains(nombre_user))
            if curso:
                query = query.where(Usuario.curso.contains(curso))
            if fecha:
                query = query.where(Prestamos.fecha_termino == fecha)
            query = query.offset(offset).limit(limit)
            prestamos = session.execute(query)
            return prestamos
        except Exception as e:
            traceback.print_exc()
            print(f"Errores {e}")

    def selected_user_by_rut(rut_):
        """
        **Funcion selected_user_by_rut**\n
        Permite obtener todos los usuarios que tengan el parametro necesario para la funcion\n

        **Parametro**\n
        rut: str | None\n

        **Retorna**\n
        user: Objeto Usuario
        """
        try:
            user = session.execute(select(Usuario).where(Usuario.rut == rut_)).all()
            return user
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_estado_libro_all():
        """
        **Funcion select_estado_libro_all**\n
        Permite obtener todos los estados de los libros\n

        **Retorna**\n
        estado_libro: Objeto Estado_Libro
        """
        try:
            estado_libro = session.execute(select(Estado_Libro)).all()
            return estado_libro

        except Exception as e:
            traceback.print_exc()
            print(f"Errores {e}")

    def select_copia_libros_by_id(id):
        """
        **Funcion select_copia_libros_by_id**\n
        Permite obtener todas las copias de los libros a partir del parametro\n

        **Parametro**\n
        id: int | None\n

        **Retorna**\n
        libro: Objetos Libro
        """
        try:
            # Subconsulta: último préstamo por copia
            ultimo_prestamo = (
                select(
                    Prestamos.copia_id,
                    func.max(Prestamos.id_prestamos).label("ultimo_prestamo_id")
                )
                .group_by(Prestamos.copia_id)
                .subquery()
            )

            # Alias para Prestamos
            p_alias = aliased(Prestamos)

            # Consulta principal
            libros = session.execute(
                select(
                    CopiasLibros.id_copia,
                    Libro.nombre_libro,
                    Libro.autor,
                    Libro.editorial,
                    Libro.fecha_entrada,
                    Estado_Libro.estado_libro
                )
                .join(CopiasLibros.libro)
                .join(CopiasLibros.estado)
                .outerjoin(ultimo_prestamo, CopiasLibros.id_copia == ultimo_prestamo.c.copia_id)
                .outerjoin(p_alias, p_alias.id_prestamos == ultimo_prestamo.c.ultimo_prestamo_id)
                .where(CopiasLibros.libro_id == id)
                .where(
                    or_(
                        p_alias.id_prestamos == None,  # nunca ha sido prestado
                        p_alias.estado_prestamo_id.in_([2, 3])  # Devuelto o Extraviado
                    )
                )
            ).all()
            return libros

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error {e}")

    def select_prestamo_by_fecha(fecha):
        """
        **Funcion select_prestamo_by_fecha**\n
        Devuelve todos los prestamos a traves del parametro obtenido\n
        
        **Parametros**\n
        fecha: str | datetime\n

        **Retorna**\n
        prestamo_fecha: Objetos Prestamo
        """
        try:
            prestamo_fecha = session.execute(select(Usuario.nombre, Libro.nombre_libro, Libro.editorial, Libro.autor,
                                                    Prestamos.fecha_inicio, Prestamos.fecha_termino,
                                                    Estado_Libro.estado_libro, CopiasLibros.id_copia, Prestamos.id_prestamos,
                                                    Estado_Prestamo.estado_prestamo)
                                                    .join(Prestamos.estado_prestamo)
                                                    .join(Prestamos.copia)
                                                    .join(Prestamos.user)
                                                    .join_from(CopiasLibros, Libro, CopiasLibros.libro_id == Libro.id_libro)
                                                    .join_from(CopiasLibros, Estado_Libro, CopiasLibros.estado_id == Estado_Libro.id_estadolibro)
                                                    .outerjoin(Prestamos.estado_prestamo)
                                                    .where(Prestamos.fecha_inicio.contains(fecha))
                                                    .where(or_(Estado_Prestamo.estado_prestamo == "Prestado",
                                                            Estado_Prestamo.estado_prestamo == "Extraviado")))
            return prestamo_fecha
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_prestamo_libro(nombre, autor, editorial):
        """
        **Funcion select_prestamo_libro** \n
        Devuelve todos los libros con su respectivo prestamo, en base a los parametros que necesita la funcion

        **Parametros** \n
        nombre: str \n
        autor: str \n
        editorial: str \n

        **Retorna**\n
        prestamos: Objeto Libro
        """
        try:
            # Subconsulta: último préstamo por copia
            ultimo_prestamo = (
                select(
                    Prestamos.copia_id,
                    func.max(Prestamos.id_prestamos).label("ultimo_prestamo_id")
                )
                .group_by(Prestamos.copia_id)
                .subquery()
            )

            # Alias para Prestamos
            p_alias = aliased(Prestamos)

            # Datos de prestamos
            prestamos = session.execute(select(Libro.nombre_libro, Libro.autor, Libro.editorial,
                                            Libro.fecha_entrada, Estado_Libro.estado_libro, CopiasLibros.id_copia,
                                            Libro.id_libro)
                                            .join(Libro.copias)
                                            .join(CopiasLibros.estado)
                                            .outerjoin(ultimo_prestamo, CopiasLibros.id_copia == ultimo_prestamo.c.copia_id)
                                            .outerjoin(p_alias, p_alias.id_prestamos == ultimo_prestamo.c.ultimo_prestamo_id)
                                            .where(Libro.nombre_libro == nombre)
                                            .where(Libro.autor == autor)
                                            .where(Libro.editorial == editorial)
                                            .where(
                                                    or_(
                                                            p_alias.id_prestamos == None,  # nunca ha sido prestado
                                                            p_alias.estado_prestamo_id.in_([2, 3])  # Devuelto o Extraviado
                                                        )
                                                    )
                                            .order_by(Libro.fecha_entrada.desc())).all()
            return prestamos
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_cursos_user():
        """
        **Funcion select_cursos_user**\n
        Permite obtener todos los cursos disponibles dentro de la tabla Usuario\n
        No trae datos repetidos

        **Retorna**\n
        curso: Objeto Usuario, columna curso -> str
        """
        try:
            curso = session.execute(select(distinct(Usuario.curso)))
            return curso
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")
    def select_all_estado_prestamos():
        """
        **Funcion select_all_estado_prestamos**\n
        Permite obtener todos los estados de prestamos existentes en la base de datos

        **Retorna**\n
        estado: Objeto Estado_Prestamo
        """
        try:
            estado = session.execute(select(Estado_Prestamo)).all()
            return estado
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_all_estado_impresion():
        """
        **Funcion select_all_estado_impresion**\n
        Permite obtener todos los estados pertenecientes a las impresiones\n
        
        **Retorna**\n
        estado: Objeto Estado_Impresion
        """
        try:
            estado = session.execute(select(Estado_Impresion)).all()
            return estado
        except Exception as e:
            traceback.print_exc()
            print(f"Errores {e}")

    def select_type_sheet():
        """
        **Funcion select_type_sheet**\n
        Permite obtener todos los tipos de hojas que existen dentro de impresiones\n
        No trae datos repetidos

        **Retorna**\n
        hoja: Objeto Impresiones, columna tipo_papel -> Tuple[str]
        """
        try:
            hoja = session.execute(select(distinct(Impresiones.tipo_papel)))
            return hoja
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_distinct_nombre_libro():
        """
        **Funcion select_distinct_nombre_libro**\n
        Permite obtener todos los nombres de los libros pertenecientes a la tabla Libro\n
        No trae datos repetidos\n

        **Retorna**\n
        nombre_libro: Objeto Libro, columna nombre_libro -> Tuple[str]
        """
        try:
            nombre_libro = session.execute(select(distinct(Libro.nombre_libro).label("nombre_libro")))
            return nombre_libro
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_distinct_autor_libro():
        """
        **Funcion select_distinct_autor_libro**\n
        Permite obtener todos los autores que se encuentran almacenados en la tabla Libros\n
        No trae datos repetidos\n

        **Retorna**\n
        autor: Objeto Libro, columna autor -> Tuple[str]
        """
        try:
            autor = session.execute(select(distinct(Libro.autor).label("autor")))
            return autor
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_distinct_editorial_libro():
        """
        **Funcion select_distinct_editorial_libro**\n
        Permite obtener todas las editoriales existentes dentro de la tabla Libro\n
        No trae datos repetidos\n

        **Retorna**\n
        editorial: Objeto Libro, columna editorial -> Tuple[str]
        """
        try:
            editorial = session.execute(select(distinct(Libro.editorial).label("editorial")))
            return editorial
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_distinct_estanteria_libro():
        """
        **Funcion select_distinct_estanteria_libro**\n
        Permite obtener todos los campos de sector estanteria dentro de la tabla Libro\n
        No trae datos repetidos\n

        **Retorna**\n
        estanteria: Objeto Libro, columna sector_estanteria -> Tuple[str]
        """
        try:
            estanteria = session.execute(select(distinct(Libro.sector_estanteria).label("sector_estanteria")))
            return estanteria
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_distinct_biblioteca_libro():
        """
        **Funcion select_distinct_biblioteca_libro**\n
        Permite obtener todos los campos de sector biblioteca dentro de la tabla Libro\n
        No trae datos repetidos\n

        **Retorna**\n
        estanteria: Objeto Libro, columna sector_biblioteca -> Tuple[str]
        """
        try:
            biblioteca = session.execute(select(distinct(Libro.sector_biblioteca).label("sector_biblioteca")))
            return biblioteca
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def count_pages_printed_in_month():
        """
        **Funcion count_pages_printed_in_month**\n
        Permite la posibilidad de contar la cantidad de pagina que han sido impresas durante
        el mes actual\n

        **Retorna**\n
        cantidad: Objeto Impresion
        """
        try:
            today_month = date.today().strftime("%m")
            cantidad = session.execute(select(Impresiones.cantidad_copias, Impresiones.cantidad_paginas)
                                       .join(Impresiones.estado_impresion)
                                       .where(extract("month", Impresiones.fecha_impresion) == today_month)
                                       .where(Estado_Impresion.estado_impresion == "Ya Impreso"))
            return cantidad
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")