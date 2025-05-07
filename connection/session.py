import traceback
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update, func, or_
from sql.models import engine
from sql.models import (Usuario, Libro, Estado_Libro,
                        Estado_Impresion, Estado_Prestamo, Prestamos,
                        Impresiones, CopiasLibros)


with Session(engine) as session:
    def select_libros_available():
        try:
            libros = session.execute(select(Libro.nombre_libro, Libro.cod_barras, Libro.autor,Libro.fecha_publicacion,Estado_Libro.estado_libro
                                            ,func.count(CopiasLibros.id_copia).label("stock"))
                                     .join(CopiasLibros.libro)
                                     .join(CopiasLibros.estado)
                                     .outerjoin(CopiasLibros.prestamos)
                                     .where(or_(Prestamos.copia_id == None, 
                                                Prestamos.estado_prestamo_id == 2,
                                                Prestamos.estado_prestamo_id == 3))
                                     .group_by(Libro.nombre_libro, Estado_Libro.estado_libro))
            return libros
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_impresion_all():
        try:
            impresion = session.execute(select(Impresiones, Estado_Impresion, Usuario)
                                        .join(Impresiones.estado_impresion)
                                        .join_from(Impresiones, Usuario, Impresiones.user_id == Usuario.id_user)
                                        .order_by(Impresiones.id_impresion.desc()))
            return impresion
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_prestamos_all():
        try:
            prestamos = session.execute(select(Prestamos.fecha_inicio, Prestamos.fecha_termino, Estado_Prestamo.estado_prestamo,
                                               Usuario.nombre, Usuario.curso, Usuario.rut, Libro.nombre_libro,
                                               func.count(Libro.nombre_libro).label("stock"))
                                               .join(Prestamos.estado_prestamo)
                                               .join(Prestamos.user)
                                               .outerjoin(Prestamos.copia)
                                               .join_from(CopiasLibros, Libro, CopiasLibros.libro_id == Libro.id_libro)
                                               .group_by(Usuario.nombre, Libro.nombre_libro,Prestamos.fecha_inicio, Estado_Prestamo.estado_prestamo)
                                               .order_by(Prestamos.fecha_inicio.desc()))
            return prestamos
        except Exception as e:
            traceback.print_exc()
            print(f"Errores {e}")

    def selected_user_by_rut(rut_):
        try:
            user = session.execute(select(Usuario).where(Usuario.rut == rut_)).all()
            return user
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def selected_libro_by_cod(barras):
        try:
            libro = session.execute(select(Libro).where(Libro.cod_barras == barras)).all()
            return libro
        except Exception as e:
            traceback.print_exc()
            print(f"Errores {e}")

    def select_estado_libro_all():
        try:
            estado_libro = session.execute(select(Estado_Libro)).all()
            return estado_libro

        except Exception as e:
            traceback.print_exc()
            print(f"Errores {e}")

    def select_copia_libros_by_id(id):
        try:
            libros = session.execute(select(CopiasLibros.id_copia,Libro.nombre_libro, Libro.cod_barras, 
                                            Libro.autor,Libro.fecha_publicacion,
                                            Estado_Libro.estado_libro)
                                     .join(CopiasLibros.libro)
                                     .join(CopiasLibros.estado)
                                     .outerjoin(CopiasLibros.prestamos)
                                     .where(CopiasLibros.libro_id == id)
                                     .where(Prestamos.id_prestamos == None))
            return libros
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_prestamo_by_fecha(fecha):
        try:
            prestamo_fecha = session.execute(select(Usuario.nombre, Libro.nombre_libro, Libro.cod_barras,
                                                    Prestamos.fecha_inicio, Prestamos.fecha_termino,
                                                    Estado_Libro.estado_libro, CopiasLibros.id_copia, Prestamos.id_prestamos)
                                                    .join(Prestamos.copia)
                                                    .join(Prestamos.user)
                                                    .join_from(CopiasLibros, Libro, CopiasLibros.libro_id == Libro.id_libro)
                                                    .join_from(CopiasLibros, Estado_Libro, CopiasLibros.estado_id == Estado_Libro.id_estadolibro)
                                                    .outerjoin(Prestamos.estado_prestamo)
                                                    .where(Prestamos.fecha_inicio.contains(fecha))
                                                    .where(Estado_Prestamo.estado_prestamo == "Prestado"))
            return prestamo_fecha
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")

    def select_all_estado_prestamos():
        try:
            estado = session.execute(select(Estado_Prestamo)).all()
            return estado
        except Exception as e:
            traceback.print_exc()
            print(f"Error {e}")
