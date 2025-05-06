import traceback
from PyQt5.QtWidgets import QMessageBox, QErrorMessage
from connection.session import (session, selected_user_by_rut, selected_libro_by_cod,
                                update)

from datetime import date, datetime

from sql.models import Libro, Impresiones, Usuario, CopiasLibros, Prestamos

def insertar_libros(nombre_, codigo_, autor_, fecha_, stock_):
    try:
        libro_cod = selected_libro_by_cod(codigo_)
        if libro_cod:
            libro = libro_cod[0][0]
        else:
            libro = Libro(
                nombre_libro = nombre_,
                cod_barras = codigo_,
                autor = autor_,
                fecha_publicacion = fecha_
            )
            session.add(libro)
            session.commit()
        for _ in range(int(stock_)):
            copia = CopiasLibros(
                libro_id = libro.id_libro,
                estado_id = 1
            )
            session.add(copia)
        session.commit()
        msg = QMessageBox()
        msg.setWindowTitle("Guardar Libro")
        msg.setText("¿Deseas guardar este libro?")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setIcon(QMessageBox.Question)
        msg.exec()
        if msg.standardButton(msg.clickedButton()) == QMessageBox.Save:
            #session.add(libro)
            #session.commit()
            pass

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
    finally:
        session.close()

def ingresar_impresiones(nombre_, curso_, rut_,cant_copias, cant_paginas, descripcion_):
    fecha = datetime.now()
    fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
    fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    print(fecha)
    try:
        user_rut = selected_user_by_rut(rut_)
        if user_rut:
            user = user_rut[0][0]
        else:
            user = Usuario(
                nombre = nombre_,
                curso = curso_,
                rut = rut_
            )
            session.add(user)
            session.commit()
        impresion = Impresiones(
            descripcion = descripcion_,
            cantidad_copias = cant_copias,
            cantidad_paginas = cant_paginas,
            fecha_impresion = (fecha),
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
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            error_mensaje = QErrorMessage()
            error_mensaje.setWindowTitle("Error ingresado")
            error_mensaje.showMessage(f"A ocurrido un error al momento de hacer ingreso de la impresion.\
                                      Favor de volver a intentarlo. {e}")
            session.rollback()
        except:
            print("No se pudo obtener el error")
    finally:
        session.close()

def insert_prestamos(fecha_termino, rut_, nombre_, curso_, copia_):
    fecha = datetime.now()
    fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
    fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    try:
        user_rut = selected_user_by_rut(rut_)
        if user_rut:
            user = user_rut[0][0]
        else:
            user = Usuario(
                nombre = nombre_,
                curso = curso_,
                rut = rut_
            )
            session.add(user)
            session.commit()
        prestamo = Prestamos(
            fecha_inicio = fecha,
            fecha_termino = fecha_termino,
            estado_prestamo_id = 1,
            user_id = user.id_user,
            copia_id = copia_
        )
        msg = QMessageBox()
        msg.setWindowTitle("Guardar Impresion")
        msg.setText("¿Deseas guardar este Impresion?")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setIcon(QMessageBox.Question)
        msg.exec()
        if msg.standardButton(msg.clickedButton()) == QMessageBox.Save:
            session.execute(prestamo)
            session.commit()

        elif msg.standardButton(msg.clickedButton()) == QMessageBox.Cancel:
            cancelAction = QMessageBox()
            cancelAction.setText("Se cancelo la accion")
            cancelAction.setStandardButtons(QMessageBox.Ok)
            cancelAction.setIcon(QMessageBox.Information)
            cancelAction.setWindowTitle("Accion Cancelada")
            cancelAction.exec()   
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            error_mensaje = QErrorMessage()
            error_mensaje.setWindowTitle("Error ingresado")
            error_mensaje.showMessage(f"A ocurrido un error al momento de hacer un cambio en el estado del Libro.\
                                      Favor de volver a intentarlo. {e}")
            session.rollback()
        except:
            print("No se pudo obtener el error")
    finally:
        session.close()

def update_estado_libro(id, estado):
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
        except:
            print("No se pudo obtener el error")
    finally:
        session.close()

def update_estado_impresion(fecha, estado):
    try:
        print(f"Su futuro estado es: {estado}\
              y la fecha es: {fecha}")
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
        except:
            print("No se pudo obtener el error")
    finally:
        session.close()
