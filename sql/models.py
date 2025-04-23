import sys, os

from typing import List, Optional
from sqlalchemy.schema import MetaData
from sqlalchemy import (ForeignKey, String, create_engine, Date, DateTime)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column,
                            relationship)
from datetime import date, datetime

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS # for --onefile
        # bundle_dir = path.dirname(path.abspath(sys.executable)) # for --onedir
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(bundle_dir, relative_path)

base_datos = resource_path("biblioteca.db")

engine = create_engine(f"sqlite:///{base_datos}", echo=True)


class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = "usuario"

    id_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str]
    curso: Mapped[Optional[str]]
    rut: Mapped[str] = mapped_column(unique=True)

    impresion: Mapped[List["Impresiones"]] = relationship()
    prestamo: Mapped[List["Prestamos"]] = relationship()

    def __repr__(self):
        return f"User(id_user={self.id_user}, nombre={self.nombre},\
        curso={self.curso}, rut={self.rut})"

class Libro(Base):
    __tablename__ = "libro_biblioteca"

    id_libro: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_libro: Mapped[str]
    cod_barras: Mapped[str] = mapped_column(unique=True)
    autor: Mapped[str]
    fecha_publicacion: Mapped[date]
    stock: Mapped[int]
    estado_libro_id: Mapped[int] = mapped_column(ForeignKey("estado_libro.id_estadolibro"))

    estado_libro: Mapped["Estado_Libro"] = relationship()
    prestamos: Mapped[List["Prestamos"]] = relationship()

    def __repr__(self):
        return f"Libro(id_libro={self.id_libro}, nombre_libro={self.nombre_libro},\
            cod_barras={self.cod_barras}, editorial={self.editorial}, \
            stock={self.stock}, fecha_publicacion={self.fecha_publicacion})"

class Estado_Libro(Base):
    __tablename__ = "estado_libro"

    id_estadolibro: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado_libro: Mapped[str]




    def __repr__(self):
        return f"Estado_Libro(id_estadolibro={self.id_estadolibro}, estado_libro={self.estado_libro})"

class Impresiones(Base):
    __tablename__ = "impresion"

    id_impresion: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    descripcion: Mapped[str]
    cantidad_copias: Mapped[str]
    cantidad_paginas: Mapped[str]
    fecha_impresion: Mapped[datetime]
    estado_impresion_id: Mapped[int] = mapped_column(ForeignKey("estado_impresiones.id_estadoimpresiones"))

    estado_impresion: Mapped["Estado_Impresion"] = relationship()

    user_id: Mapped[int] = mapped_column(ForeignKey("usuario.id_user"))


    def __repr__(self):
        return f"Impresion(id_impresion={self.id_impresion}, descripcion={self.descripcion},\
            cantidad_copias={self.cantidad_copias}, cantidad_paginas={self.cantidad_paginas}, \
                fecha_impresion={self.fecha_impresion})"

class Estado_Impresion(Base):
    __tablename__ = "estado_impresiones"

    id_estadoimpresiones: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado_impresion: Mapped[str]

    def __repr__(self):
        return f"Estado_Impresion(id_estadoimpresiones={self.id_estadoimpresiones}, estado_impresion={self.estado_impresion})"
    

class Prestamos(Base):
    __tablename__ = "prestamos_libros"

    id_prestamos: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fecha_inicio: Mapped[datetime]
    fecha_termino: Mapped[date]
    estado_prestamo_id: Mapped[int] = mapped_column(ForeignKey("estado_prestamo.id_estadoprestamo"))

    estado_prestamo: Mapped["Estado_Prestamo"] = relationship()

    user_id: Mapped[int] = mapped_column(ForeignKey("usuario.id_user"))
    libro_id: Mapped[int] = mapped_column(ForeignKey("libro_biblioteca.id_libro"))

    def __repr__(self):
        return f"Prestamos(id_prestamos={self.id_prestamos}, fecha_inicio={self.fecha_inicio},\
            fecha_inicio={self.fecha_termino})"
    
class Estado_Prestamo(Base):
    __tablename__ = "estado_prestamo"

    id_estadoprestamo: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado_prestamo: Mapped[str]

    def __repr__(self):
        return f"Estado_Prestamo(id_estadoprestamo={self.id_estadoprestamo}, estado_prestamo={self.estado_prestamo})"

Base.metadata.create_all(bind=engine)

conn = engine.connect()
