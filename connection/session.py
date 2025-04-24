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
    except Exception as e:
        print(f"Errores {e}")

