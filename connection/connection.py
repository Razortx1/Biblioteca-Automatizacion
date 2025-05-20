"""
    **connection.py**\n

    Modulo con el proposito de realizar las diversas conexiones a la base
    de datos, esto con el proposito de realizar los inserts y los update
    a las tablas de Usuario, Prestamos, CopiasLibros, Libro y Impresion\n

    **Imports del modulo**\n

    traceback ----> Usado para verificar errores fantasma\n
    PyQt5.QtWidgets -----> Usado para traer los widgets necesarios\n
                            QMessageBox ---> Ventana Pop Up para verificacion con usuario\n
                            QErrorMessage ---> Ventana Pop Up para mostrar errores al usuario\n
    datetime -----> Para obtener la fecha de hoy, junto con sus horas, minutos y segundos\n

    modulo session ---> Se importo el modulo local session con el proposito de usar los select que este
                        posee\n
    modulo models ----> Se importo el modulo local models, el cual contiene los mapeos, a traves de clases
                        de las tablas de la base de datos\n
"""

import traceback
from PyQt5.QtWidgets import QMessageBox, QErrorMessage

from datetime import datetime

from connection.session import (session, selected_user_by_rut,
                                update, select_libros_equal)
from sql.models import Libro, Impresiones, Usuario, CopiasLibros, Prestamos

def get_create_libros(nombre_, autor_, editorial_, fecha_, sector_b, sector_es):
    """
        **Funcion get_create_libros**\n
        Permite comprobar si el libro existe o no en la base de datos\n

        **Parametros**\n
        - nombre: str\n
        - autor: str\n
        - editorial: str\n
        - fecha: str | date\n
        - sector_b: str\n
        - sector_es: str\n

        **Retorna**\n
        libro: Un objeto Libro
    """
    libro_ = select_libros_equal(nombre=nombre_,
                                 autor=autor_,
                                 editorial=editorial_,
                                 fecha=fecha_,
                                 sectorbiblioteca=sector_b,
                                 sectorestanteria=sector_es)
    if libro_:
        libro = libro_[0].Libro
        return libro
    else:
        libro = Libro(
                nombre_libro = nombre_,
                autor = autor_,
                editorial = editorial_,
                fecha_entrada = fecha_,
                sector_biblioteca = sector_b,
                sector_estanteria = sector_es
            )
        session.add(libro)
        session.flush()
        return libro

def insertar_libros(nombre_, autor_, editorial_, fecha_,sector_b, sector_es, stock_):
    """
    **Funcion insertar_libros**\n
        
    Añade a la base de datos, el libro si es que no existe con su respectivo stock\n

    **Parametros**\n
    - nombre: str\n
    - autor: str\n
    - editorial: str\n
    - fecha: str | date\n
    - sector_b: str\n
    - sector_es: str\n
    - stock: int\n
    """
    try:
        libro = get_create_libros(nombre_,autor_,editorial_,fecha_,sector_b,sector_es)
        for _ in range(int(stock_)):
            copia = CopiasLibros(
                libro_id = libro.id_libro,
                estado_id = 1
            )
            session.add(copia)
        msg = QMessageBox()
        msg.setWindowTitle("Guardar Libro")
        msg.setText("¿Deseas guardar este libro?")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setIcon(QMessageBox.Question)
        msg.exec()
        if msg.standardButton(msg.clickedButton()) == QMessageBox.Save:
            msg_ok = QMessageBox()
            msg_ok.setWindowTitle("Libro Agregado")
            msg_ok.setText("El libro se ha agregado correctamente.")
            msg_ok.setIcon(QMessageBox.Information)
            msg_ok.exec()
            session.commit()
            

        elif msg.standardButton(msg.clickedButton()) == QMessageBox.Cancel:
            cancelAction = QMessageBox()
            cancelAction.setText("Se cancelo la accion")
            cancelAction.setStandardButtons(QMessageBox.Ok)
            cancelAction.setIcon(QMessageBox.Information)
            cancelAction.setWindowTitle("Accion Cancelada")
            cancelAction.exec()

    except Exception as e:
        traceback.print_exc()
        error_mensaje = QErrorMessage()
        error_mensaje.setWindowTitle("Error de agregado")
        error_mensaje.showMessage(f"A ocurrido un error al momento de insertar el libro.\
                                  Favor de volver a intentarlo. {e}")
        session.rollback()

def get_or_create_user(nombre_, curso_, rut_):
    """
    **Funcion get_or_create_user**\n
    Permite comprobar si existe un usuario en la base de datos.\n
    Si existe, pero no se detecta que tenga su mismo curso, se actualiza
    con la funcion update_usuario. Sino existe se crea uno nuevo\n

    **Parametros**\n
    - nombre: str\n
    - curso: str\n
    - - rut: str\n

    **Retorna**\n
    user: Un objeto Usuario
    """
    user_rut = selected_user_by_rut(rut_)
    if user_rut:
        user = user_rut[0].Usuario
        if user.curso != curso_:
            update_usuario(user.id_user, curso_)
        return user
    else:
        user = Usuario(
            nombre = nombre_,
            curso = curso_,
            rut = rut_
        )
        session.add(user)
        session.flush()
        return user

def ingresar_impresiones(nombre_, curso_, rut_,cant_copias, cant_paginas, descripcion_, tipo_hoja):
    """
    **Funcion ingresar_impresiones**\n
    Permite agregar una impresion que esta enlazada a un usuario\n

    **Parametros**\n
    - nombre: str\n
    - curso: str\n
    - rut: str\n
    - cant_copias: str\n
    - cant_paginas: str\n
    - descripcion: str\n
    - tipo_hoja: str\n

    **Excepcion**\n
    Devuelve un mensaje, a traves de un QErrorMessage, que no se pudo ingresar
    la impresion
    """
    fecha = datetime.now()
    fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
    fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    try:
        user = get_or_create_user(nombre_, curso_, rut_)
        impresion = Impresiones(
            descripcion = descripcion_,
            cantidad_copias = cant_copias,
            cantidad_paginas = cant_paginas,
            fecha_impresion = (fecha),
            tipo_papel = tipo_hoja,
            estado_impresion_id = 1,
            user_id = user.id_user
        )
        msg = QMessageBox()
        msg.setWindowTitle("Guardar Impresion")
        msg.setText("¿Deseas guardar este Impresion?")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setIcon(QMessageBox.Question)
        msg.exec()
        if msg.standardButton(msg.clickedButton()) == QMessageBox.Save:
            session.add(impresion)
            session.commit()

        elif msg.standardButton(msg.clickedButton()) == QMessageBox.Cancel:
            cancelAction = QMessageBox()
            cancelAction.setText("Se cancelo la accion")
            cancelAction.setStandardButtons(QMessageBox.Ok)
            cancelAction.setIcon(QMessageBox.Information)
            cancelAction.setWindowTitle("Accion Cancelada")
            cancelAction.exec()
            session.rollback()
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            error_mensaje = QErrorMessage()
            error_mensaje.setWindowTitle("Error ingresado")
            error_mensaje.showMessage(f"A ocurrido un error al momento de hacer ingreso de la impresion.\
                                      Favor de volver a intentarlo. {e}")
            session.rollback()
        except Exception as e:
            print(f"Error {e}")

def insert_prestamos(fecha_i,fecha_m, rut_, nombre_, curso_, copia_):
    """
    **Funcion insert_prestamos**\n
    Permite agregar un prestamo a la base de datos, con un usuario asignado a esta\n

    **Parametros**\n
    - fecha_i: str | datetime\n
    - fecha_m: str | date\n
    - rut: str\n
    - nombre: str\n
    - curso: str\n
    - copia: int\n

    **Excepcion**\n
    Devuelve un mensaje, a traves de un QErrorMessage, que no se pudo ingresar
    el prestamo
    """
    try:
        user = get_or_create_user(nombre_, curso_, rut_)
        prestamo = Prestamos(
            fecha_inicio = fecha_i,
            fecha_termino = fecha_m,
            estado_prestamo_id = 1,
            user_id = user.id_user,
            copia_id = copia_
        )
        session.add(prestamo)
        session.commit()
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            error_mensaje = QErrorMessage()
            error_mensaje.setWindowTitle("Error ingresado")
            error_mensaje.showMessage(f"A ocurrido un error al momento de hacer un cambio en el estado del Libro.\
                                      Favor de volver a intentarlo. {e}")
            session.rollback()
        except Exception as e:
            print(f"Error {e}")

def update_estado_libro(id, estado):
    """
    **Funcion update_estado_libro**\n
    Permite el poder actualizar el estado de un libro\n

    **Parametros**\n
    - id: int\n
    - estado: int\n

    **Excepcion**\n
    Devuelve un mensaje, a traves de un QErrorMessage, que no se pudo actualizar el estado del libro
    """
    try:
        session.execute(update(CopiasLibros)
                        .where(CopiasLibros.id_copia == id)
                        .values(estado_id = estado))
        session.commit()
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            error_mensaje = QErrorMessage()
            error_mensaje.setWindowTitle("Error ingresado")
            error_mensaje.showMessage(f"A ocurrido un error al momento de hacer un cambio en el estado del Libro.\
                                      Favor de volver a intentarlo. {e}")
            session.rollback()
        except Exception as e:
            print(f"Error {e}")

def update_estado_impresion(fecha, estado):
    """
    **Funcion update_estado_impresion**\n
    Permite el poder actualizar el estado de una impresion\n

    **Parametros**\n
    - fecha: str | datetime\n
    - estado: int\n

    **Excepcion**\n
    Devuelve un mensaje, a traves de un QErrorMessage, que no se pudo actualizar el estado de
    la impresion
    """
    try:
        session.execute(update(Impresiones)
                        .where(Impresiones.fecha_impresion.contains(fecha))
                        .values(estado_impresion_id = estado))
        session.commit()
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            error_mensaje = QErrorMessage()
            error_mensaje.setWindowTitle("Error ingresado")
            error_mensaje.showMessage(f"A ocurrido un error al momento de hacer un cambio en el estado de la Impresion.\
                                      Favor de volver a intentarlo. {e}")
            session.rollback()
        except Exception as e:
            traceback.print_exc()
            print("No se pudo obtener el error")

def update_estado_prestamos(id, estado):
    """
    **Funcion update_estado_prestamos**\n
    Permite poder actualizar el estado del prestamo\n
    
    **Parametros**\n
    - - id: int\n
    - estado: int\n

    **Excepcion**\n
    Devuelve un mensaje, a traves de un QErrorMessage, que no se pudo actualizar el estado del prestamo
    """
    try:
        session.execute(update(Prestamos)
                        .where(Prestamos.id_prestamos == id)
                        .values(estado_prestamo_id = estado))
        session.commit()
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            error_mensaje = QErrorMessage()
            error_mensaje.setWindowTitle("Error ingresado")
            error_mensaje.showMessage(f"A ocurrido un error al momento de hacer un cambio en el estado de la Impresion.\
                                      Favor de volver a intentarlo. {e}")
            session.rollback()
        except Exception as e:
            print(f"Error {e}")

def update_usuario(id, curso_):
    """
    **Funcion update_usuario**\n
    Permite el poder actualizar el curso de un usuario\n

    **Parametros**\n
    - id: int\n
    - curso: str\n

    **Excepcion**\n
    Devuelve un mensaje, a traves de un QErrorMessage, que no se pudo actualizar el usuario
    """
    try:
        session.execute(update(Usuario)
                        .where(Usuario.id_user == id)
                        .values(curso = curso_)
                        .execution_options(synchronize_session="fetch"))
        session.commit()
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            error_mensaje = QErrorMessage()
            error_mensaje.setWindowTitle("Error ingresado")
            error_mensaje.showMessage(f"A ocurrido un error al momento de hacer un cambio en el estado de la Impresion.\
                                      Favor de volver a intentarlo. {e}")
            session.rollback()
        except Exception as e:
            print(f"Error {e}")