from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from sql.models import engine
from sql.models import (Usuario, Libro, Estado_Libro,
                        Estado_Impresion, Estado_Prestamo, Prestamos,
                        Impresiones)


with Session(engine) as session:
    try:
        def select_libros_all():
            libros = session.execute(select(Libro, Estado_Libro)
                                     .join(Libro.estado_libro))
            return libros
        def select_prestamos_all():
            prestamos = session.execute(select(Prestamos, Estado_Prestamo,
                                               Usuario, Libro)
                                               .join(Prestamos.estado_prestamo)
                                               .join_from(Prestamos, Usuario, Prestamos.user_id == Usuario.id_user)
                                               .join_from(Prestamos, Libro, Prestamos.libro_id == Libro.id_libro)
                                               .order_by(Prestamos.id_prestamos.asc()))
            return prestamos
    except Exception as e:
        print(f"Errores {e}")

