from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from sql.models import engine
from sql.models import (Usuario, Libro, Estado_Libro,
                        Estado_Impresion, Estado_Prestamo, Prestamos,
                        Impresiones)


with Session(engine) as session:
    def select_libros_all():
        try:
            libros = session.execute(select(Libro, Estado_Libro)
                                     .join(Libro.estado_libro))
            return libros
        except Exception as e:
            print(f"Errores {e}")
    def select_prestamos_all():
        try:
            prestamos = session.execute(select(Prestamos, Estado_Prestamo,
                                        Usuario, Libro)
                                        .join(Prestamos.estado_prestamo)
                                        .join_from(Prestamos, Usuario, Prestamos.user_id == Usuario.id_user)
                                        .join_from(Prestamos, Libro, Prestamos.libro_id == Libro.id_libro)
                                        .order_by(Prestamos.id_prestamos.desc()))
            return prestamos
        except Exception as e:
            print(f"Errores {e}")
    
    def select_impresion_all():
        try:
            prestamos = session.execute(select(Impresiones, Estado_Impresion, Usuario)
                                        .join(Impresiones.estado_impresion)
                                        .join_from(Impresiones, Usuario, Impresiones.user_id == Usuario.id_user)
                                        .order_by(Impresiones.id_impresion.desc()))
            return prestamos
        except Exception as e:
            print(f"Error {e}")

    def selected_user_by_rut(rut_):
        user = session.execute(select(Usuario).where(Usuario.rut == rut_)).all()
        return user

