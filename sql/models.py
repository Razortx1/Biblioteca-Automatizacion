"""
    Archivo models.py

    Es un archivo .py donde se encuentra toda la logica para poder
    realizar la creacion de las tablas.

    Para poder crear las tablas, se hace uso de la libreria SQLAlchemy a traves de su
    ORM
"""

"""
    Importacion de librerias sys y os
"""

import sys, os

"""
    Importacion de las librerias de sqlalchemy para poder crear las clases para las tablas
    con ORM
"""

from typing import List, Optional
from sqlalchemy import (ForeignKey, String, create_engine)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column,
                            relationship, sessionmaker)
"""
    Importacion de la libreria datetime con el fin de poder crear columnas
    para fechas ya sea con año/mes/dia o con año/mes/dia hora/minuto/segundo
"""

from datetime import date, datetime

"""
    Se realiza una funcion con el fin de poder encontrar la base de datos
    dentro de las carpetas dentro de un computador
"""

def resource_path(relative_path):
    """
        if statement el cual necesita la libreria sys, 'frozen', el cual tiene como funcion de
        comprobar si es un archivo ejecutable o no, y False
    """
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS # for --onefile
        # bundle_dir = path.dirname(path.abspath(sys.executable)) # for --onedir
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(bundle_dir, relative_path)

"""
    Se asigna dentro de una variable, la url de donde se encuentra el archivo
    a buscar, siendo en este caso la base de datos SQLite
"""
base_datos = resource_path("biblioteca.db")

"""
    Se crea la base de datos sqlite
    
    echo sirve para verificar el codigo sql y comprobar si hay problemas o no
    (para realizar debug)
"""

engine = create_engine(f"sqlite:///{base_datos}", echo=True)

"""
    class Base
    Es la clase que se utilizará como base para poder crear las tablas
"""
class Base(DeclarativeBase):
    pass

"""
    Class Usuario
    Es la clase con la cual el ORM mapeara para poder crear la tabla de usuario.

    Esta tabla tiene como columnas:
    - id_user como numero, primary key y autoincremento
    - nombre como texto
    - curso como un texto opcional
    - rut como un texto
    
    Ademas esta tabla tiene las referencias para las futuras tablas de impresion y prestamo

"""

class Usuario(Base):
    __tablename__ = "usuario"

    id_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str]
    curso: Mapped[Optional[str]]
    rut: Mapped[str] = mapped_column(unique=True)

    impresion: Mapped[List["Impresiones"]] = relationship()
    prestamo: Mapped[List["Prestamos"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id_user={self.id_user!r}, nombre={self.nombre!r},\
        curso={self.curso!r}, rut={self.rut!r})"
    
"""
    Class Libro
    Es la clase con la cual el ORM mapeara para poder crear la tabla de libro.

    Esta tabla tiene como columnas:
    - id_libro como numero, primary key y autoincremento
    - nombre del libro como un texto
    - cod_barra como un texto
    - autor como un texto
    - fecha_publicacion como una fecha de solo año-mes-dia
    - stock como un numero
    - estado_libro_id como un numero que conecta con la futura tabla de estado_libro

    Ademas esta tabla tiene las referencias para las futuras tablas de estado_libro y prestamos_libros
"""

class Libro(Base):
    __tablename__ = "libro_biblioteca"

    id_libro: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_libro: Mapped[str]
    cod_barras: Mapped[str] = mapped_column(unique=True)
    autor: Mapped[Optional[str]]
    fecha_publicacion: Mapped[date]

    copias: Mapped[List["CopiasLibros"]] = relationship(back_populates="libro")

    def __repr__(self) -> str:
        return f"Libro(id_libro={self.id_libro!r}, nombre_libro={self.nombre_libro!r},\
            cod_barras={self.cod_barras!r}, editorial={self.autor!r}, \
            fecha_publicacion={self.fecha_publicacion!r})"
    
class CopiasLibros(Base):
    __tablename__ = "copia_libro"

    id_copia: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    libro_id: Mapped[int] = mapped_column(ForeignKey("libro_biblioteca.id_libro"))
    estado_id: Mapped[int] = mapped_column(ForeignKey("estado_libro.id_estadolibro"))

    libro: Mapped["Libro"] = relationship(back_populates="copias")
    estado: Mapped["Estado_Libro"] = relationship()
    prestamos: Mapped[List["Prestamos"]] = relationship(back_populates="copia")

    def __repr__(self):
        return f"CopiasLibros(id_copia={self.id_copia}, libro={self.libro}, estado={self.estado}, prestamo={self.prestamos})"

"""
    Class Estado_Libro
    Es la clase con la cual el ORM mapeara para poder crear la tabla de libro.

    Esta tabla tiene como columnas:
    - id_estadolibro como numero, primary key y autoincremento
    - estado_libro como un texto
"""

class Estado_Libro(Base):
    __tablename__ = "estado_libro"

    id_estadolibro: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado_libro: Mapped[str]

    def __repr__(self) -> str:
        return f"Estado_Libro(id_estadolibro={self.id_estadolibro!r}, estado_libro={self.estado_libro!r})"
    
"""
    Class Impresiones
    Es la clase con la cual el ORM mapeara para poder crear la tabla de impresion.

    Esta tabla tiene como columnas:
    - id_impresion como numero, primary key y autoincremento
    - descripcion como un texto
    - cantidad_copias como un numero
    - cantidad_pagina como un numero
    - fecha_impresion como una fecha de solo año-mes-dia hora-minutos-segundos
    - estado_impresion_id como un numero que conecta con la tabla estado_impresiones
    - user_id como un numero que conecta con la tabla usuario

    Ademas esta tabla tiene las referencias para la futura tabla de estado impresion
"""

class Impresiones(Base):
    __tablename__ = "impresion"

    id_impresion: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    descripcion: Mapped[str]
    cantidad_copias: Mapped[int]
    cantidad_paginas: Mapped[int]
    fecha_impresion: Mapped[datetime]
    estado_impresion_id: Mapped[int] = mapped_column(ForeignKey("estado_impresiones.id_estadoimpresiones"))

    estado_impresion: Mapped["Estado_Impresion"] = relationship()

    user_id: Mapped[int] = mapped_column(ForeignKey("usuario.id_user"))


    def __repr__(self) -> str:
        return f"Impresion(id_impresion={self.id_impresion!r}, descripcion={self.descripcion!r},\
            cantidad_copias={self.cantidad_copias!r}, cantidad_paginas={self.cantidad_paginas!r}, \
                fecha_impresion={self.fecha_impresion!r})"
    
"""
    Class Estado_Impresiones
    Es la clase con la cual el ORM mapeara para poder crear la tabla de estado_impresion.

    Esta tabla tiene como columnas:
    - id_estadoimpresiones como numero, primary key y autoincremento
    - estado_impresion como texto
"""

class Estado_Impresion(Base):
    __tablename__ = "estado_impresiones"

    id_estadoimpresiones: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado_impresion: Mapped[str]

    def __repr__(self) -> str:
        return f"Estado_Impresion(id_estadoimpresiones={self.id_estadoimpresiones!r}, estado_impresion={self.estado_impresion!r})"
    
"""
    Class Prestamos
        Es la clase con la cual el ORM mapeara para poder crear la tabla de prestamos_libros.

        Esta tabla tiene como columnas:
        - id_prestamos como numero, primary key y autoincremento
        - fecha_inicio como fecha con solo año-mes-dia hora-minutos-segundos
        - fecha_termino como fecha con solo año-mes-dia
        - estado_prestamo_id como numero conectando con la futura tabla de estado_prestamo
        - user_id como numero conectando con la tabla de usuarios
        - libro_id como numero conectando con la tabla de libro_biblioteca

        Ademas esta tabla tiene las referencias para la futura tabla de estado estado_prestamo
"""

class Prestamos(Base):
    __tablename__ = "prestamos_libros"

    id_prestamos: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fecha_inicio: Mapped[datetime]
    fecha_termino: Mapped[date]
    estado_prestamo_id: Mapped[int] = mapped_column(ForeignKey("estado_prestamo.id_estadoprestamo"))

    estado_prestamo: Mapped["Estado_Prestamo"] = relationship()

    user_id: Mapped[int] = mapped_column(ForeignKey("usuario.id_user"))
    copia_id: Mapped[int] = mapped_column(ForeignKey("copia_libro.id_copia"))

    copia: Mapped["CopiasLibros"] = relationship(back_populates="prestamos")
    user: Mapped["Usuario"] = relationship(back_populates="prestamo")

    def __repr__(self) -> str:
        return f"Prestamos(id_prestamos={self.id_prestamos!r}, fecha_inicio={self.fecha_inicio!r},\
            fecha_inicio={self.fecha_termino!r})"
    
"""
    Class Estado_Prestamo
        Es la clase con la cual el ORM mapeara para poder crear la tabla de estado_prestamo.

        Esta tabla tiene como columnas:
        - id_estadoprestamo como numero, primary key y autoincremento
        - estado_prestamo como un texto
"""
    
class Estado_Prestamo(Base):
    __tablename__ = "estado_prestamo"

    id_estadoprestamo: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado_prestamo: Mapped[str]

    def __repr__(self) -> str:
        return f"Estado_Prestamo(id_estadoprestamo={self.id_estadoprestamo!r}, estado_prestamo={self.estado_prestamo!r})"

"""
    A traves de la clase creada al principio de este archivo, se toma todos los metadatos
    que se detectaron y con ello se crea todo al motor de base de datos realizado anteriormente
"""

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

try:
    estados = [{
        'id_estadolibro': 1,
        'estado_libro': "Buen Estado"
    },
    {
        'id_estadolibro': 2,
        'estado_libro': "Estado Regular"
    },
    {
        'id_estadolibro': 3,
        'estado_libro': "Mal Estado"
    },
    {
        'id_estadolibro': 4,
        'estado_libro': "Dado de Baja"
    }]
    session.bulk_insert_mappings(Estado_Libro, estados)

    estados = [{
        'id_estadolibro': 1,
        'estado_impresion': "Aun no Impreso"
    },
    {
        'id_estadolibro': 2,
        'estado_impresion': "Ya Impreso"
    }]
    session.bulk_insert_mappings(Estado_Impresion, estados)

    estados = [{
        'id_estadolibro': 1,
        'estado_prestamo': "Prestado"
    },
    {
        'id_estadolibro': 2,
        'estado_prestamo': "Devuelto"
    },
    {
        'id_estadolibro': 3,
        'estado_prestamo': "Extraviado"
    }]
    session.bulk_insert_mappings(Estado_Prestamo, estados)
    session.commit()
except Exception as e:
    pass