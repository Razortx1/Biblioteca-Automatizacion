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
        **Funcion resource_path**\n
        if statement el cual necesita la libreria sys, 'frozen', el cual tiene como funcion de
        comprobar si es un archivo ejecutable o no, devolviendo True si no lo es, y False en caso que si sea

        **Parametros**\n
        relative_path: str
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

engine = create_engine(f"sqlite:///{base_datos}", echo=True)
"""
    **Variable engine**\n

    Sirve para poder crear la base de datos sqlite\n

    **Parametros**\n
    - url de la base de datos -> str
    - echo: Booleano -> True para entorno de desarrollo | False en entorno de despliegue

    **Mas informacion**\n
    echo es usado para poder revisar las sentencias SQL que vaya realizando el ORM
"""

class Base(DeclarativeBase):
    """
    **Clase Base**\n
    Es la clase que se utilizará como base para poder crear las tablas\n

    **Parametro**\n
    DeclarativeBase -> Clase Padre desde SQLAlchemy
    """
    pass


class Usuario(Base):
    """
    **Clase Usuario**\n
    Es la clase con la cual el ORM mapeara para poder crear la tabla de usuario.\n

    **Columnas**\n
    - id_user como numero, primary key y autoincremento\n
    - nombre como texto\n
    - curso como un texto opcional\n
    - rut como un texto\n
    
    **Referencias**\n
    Ademas esta tabla tiene las referencias para las futuras tablas de impresion y prestamo

    """
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
    
class Libro(Base):
    """
    **Class Libro**\n
    Es la clase con la cual el ORM mapeara para poder crear la tabla de libro.\n

    **Columnas**\n
    - id_libro como numero, primary key y autoincremento\n
    - nombre del libro como un texto\n
    - cod_barra como un texto\n
    - autor como un texto\n
    - fecha_publicacion como una fecha de solo año-mes-dia\n
    - stock como un numero\n
    - estado_libro_id como un numero que conecta con la futura tabla de estado_libro\n

    **Referencias**\n
    Ademas esta tabla tiene las referencias para la tabla de copias libro
    """
    __tablename__ = "libro_biblioteca"

    id_libro: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_libro: Mapped[str]
    autor: Mapped[Optional[str]]
    editorial : Mapped[Optional[str]]
    fecha_entrada: Mapped[date]
    sector_biblioteca : Mapped[str]
    sector_estanteria: Mapped[str]

    copias: Mapped[List["CopiasLibros"]] = relationship(back_populates="libro")

    def __repr__(self) -> str:
        return f"Libro(id_libro={self.id_libro!r}, nombre_libro={self.nombre_libro!r},\
            autor={self.autor!r},editorial={self.editorial!r}, \
            fecha_entrada={self.fecha_entrada!r}, sector_biblioteca={self.sector_biblioteca!r}\
            sector_estanteria={self.sector_estanteria!r})"
    
class CopiasLibros(Base):
    """
    **Class CopiaLibros**\n
    Es la clase con la cual el ORM mapeara para poder crear la tabla para la copia de
    los libros.\n

    **Columnas**\n
    - id_copia como numero, primary key y autoincremento\n
    - libro_id como un numero, foreing key\n
    - estado_id como un numero, foreing key\n

    **Referencias**\n
    Ademas esta tabla tiene las referencias para las futuras tablas de estado_libro, prestamos_libros
    y libro
    """
    __tablename__ = "copia_libro"

    id_copia: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    libro_id: Mapped[int] = mapped_column(ForeignKey("libro_biblioteca.id_libro"))
    estado_id: Mapped[int] = mapped_column(ForeignKey("estado_libro.id_estadolibro"))

    libro: Mapped["Libro"] = relationship(back_populates="copias")
    estado: Mapped["Estado_Libro"] = relationship()
    prestamos: Mapped[List["Prestamos"]] = relationship(back_populates="copia")

    def __repr__(self):
        return f"CopiasLibros(id_copia={self.id_copia}, libro={self.libro}, estado={self.estado}, prestamo={self.prestamos})"

class Estado_Libro(Base):
    """
        **Clase Estado_Libro**\n
        Es la clase con la cual el ORM mapeara para poder crear la tabla para el estado del libro.\n

        **Columna**\n
        - id_estadolibro como numero, primary key y autoincremento\n
        - estado_libro como un texto
    """
    __tablename__ = "estado_libro"

    id_estadolibro: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado_libro: Mapped[str]

    def __repr__(self) -> str:
        return f"Estado_Libro(id_estadolibro={self.id_estadolibro!r}, estado_libro={self.estado_libro!r})"
    
class Impresiones(Base):
    """
        **Clase Impresiones**\n
        Es la clase con la cual el ORM mapeara para poder crear la tabla de impresion.\n

        **Columnas**\n
        - id_impresion como numero, primary key y autoincremento\n
        - descripcion como un texto\n
        - cantidad_copias como un numero\n
        - cantidad_pagina como un numero\n
        - fecha_impresion como una fecha de solo año-mes-dia hora-minutos-segundos\n
        - estado_impresion_id como un numero que conecta con la tabla estado_impresiones\n
        - user_id como un numero que conecta con la tabla usuario\n

        **Referencias**\n
        Ademas esta tabla tiene las referencias para la futura tabla de estado impresion
    """
    __tablename__ = "impresion"

    id_impresion: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    descripcion: Mapped[str]
    cantidad_copias: Mapped[int]
    cantidad_paginas: Mapped[int]
    fecha_impresion: Mapped[datetime]
    tipo_papel: Mapped[str]
    estado_impresion_id: Mapped[int] = mapped_column(ForeignKey("estado_impresiones.id_estadoimpresiones"))

    estado_impresion: Mapped["Estado_Impresion"] = relationship()

    user_id: Mapped[int] = mapped_column(ForeignKey("usuario.id_user"))


    def __repr__(self) -> str:
        return f"Impresion(id_impresion={self.id_impresion!r}, descripcion={self.descripcion!r},\
            cantidad_copias={self.cantidad_copias!r}, cantidad_paginas={self.cantidad_paginas!r}, \
                fecha_impresion={self.fecha_impresion!r})"

class Estado_Impresion(Base):
    """
        **Clase Estado_Impresiones**\n
        Es la clase con la cual el ORM mapeara para poder crear la tabla de estado_impresion.\n

        **Columnas**\n
        - id_estadoimpresiones como numero, primary key y autoincremento\n
        - estado_impresion como texto
    """
    __tablename__ = "estado_impresiones"

    id_estadoimpresiones: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado_impresion: Mapped[str]

    def __repr__(self) -> str:
        return f"Estado_Impresion(id_estadoimpresiones={self.id_estadoimpresiones!r}, estado_impresion={self.estado_impresion!r})"

class Prestamos(Base):
    """
        **Clase Prestamos**\n
            Es la clase con la cual el ORM mapeara para poder crear la tabla de prestamos_libros.\n

        **Columnas**\n
        - id_prestamos como numero, primary key y autoincremento\n
        - fecha_inicio como fecha con solo año-mes-dia hora-minutos-segundos\n
        - fecha_termino como fecha con solo año-mes-dia\n
        - estado_prestamo_id como numero conectando con la futura tabla de estado_prestamo\n
        - user_id como numero conectando con la tabla de usuarios\n
        - libro_id como numero conectando con la tabla de libro_biblioteca\n

        **Referencias**\n
        Ademas esta tabla tiene las referencias para la futura tabla de estado estado_prestamo
    """
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
    
class Estado_Prestamo(Base):
    """
        **Clase Estado_Prestamo**\n
            Es la clase con la cual el ORM mapeara para poder crear la tabla de estado_prestamo.\n

        **Columnas**\n
        - id_estadoprestamo como numero, primary key y autoincremento\n
        - estado_prestamo como un texto
    """
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
session.close()

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
        'id_estadoimpresiones': 1,
        'estado_impresion': "Aun no Impreso"
    },
    {
        'id_estadoimpresiones': 2,
        'estado_impresion': "Ya Impreso"
    }]
    session.bulk_insert_mappings(Estado_Impresion, estados)

    estados = [{
        'id_estadoprestamo': 1,
        'estado_prestamo': "Prestado"
    },
    {
        'id_estadoprestamo': 2,
        'estado_prestamo': "Devuelto"
    },
    {
        'id_estadoprestamo': 3,
        'estado_prestamo': "Extraviado"
    }]
    session.bulk_insert_mappings(Estado_Prestamo, estados)
    session.commit()
except Exception as e:
    print(f"Error {e}")