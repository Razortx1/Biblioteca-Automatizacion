from PyQt5.QtWidgets import QMessageBox, QErrorMessage
from connection.session import session

from datetime import date, datetime

from sql.models import Libro, Impresiones

def insertar_libros(nombre, codigo, autor_, fecha:date, stock):
    try:
        libro = Libro(
            nombre_libro = nombre,
            cod_barras = codigo,
            autor = autor_,
            fecha_publicacion = fecha,
            stock = stock,
            estado_libro_id = 1
        )
        msg = QMessageBox()
        msg.setWindowTitle("Guardar Libro")
        msg.setText("¿Deseas guardar este libro?")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setIcon(QMessageBox.Question)
        msg.exec()
        if msg.standardButton(msg.clickedButton()) == QMessageBox.Save:
            session.add(libro)
            session.commit()

        elif msg.standardButton(msg.clickedButton()) == QMessageBox.Cancel:
            cancelAction = QMessageBox()
            cancelAction.setText("Se cancelo la accion")
            cancelAction.setStandardButtons(QMessageBox.Ok)
            cancelAction.setIcon(QMessageBox.Information)
            cancelAction.setWindowTitle("Accion Cancelada")
            cancelAction.exec()

    except Exception as e:
        error_mensaje = QErrorMessage()
        error_mensaje.setWindowTitle("Error de agregado")
        error_mensaje.showMessage(f"A ocurrido un error al momento de insertar el libro.\
                                  Favor de volver a intentarlo. {e}")
        session.rollback()
    finally:
        session.close()

def ingresar_impresiones(id_ ,cant_copias, cant_paginas, descripcion):
    fecha = datetime.now()
    try:
        impresion = Impresiones(
            descripcion = descripcion,
            cantidad_copias = cant_copias,
            cantidad_paginas = cant_paginas,
            fecha_impresion = fecha,
            estado_impresion_id = 1,
            user_id = id_
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
    except Exception as e:
        error_mensaje = QErrorMessage()
        error_mensaje.setWindowTitle("Error ingresado")
        error_mensaje.showMessage(f"A ocurrido un error al momento de hacer ingreso de la impresion.\
                                  Favor de volver a intentarlo. {e}")
        session.rollback()
    finally:
        session.close()