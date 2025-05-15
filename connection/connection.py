import traceback
from PyQt5.QtWidgets import QMessageBox, QErrorMessage

from datetime import datetime

from connection.session import (session, selected_user_by_rut,
                                update, select_libros_equal)
from sql.models import Libro, Impresiones, Usuario, CopiasLibros, Prestamos

def get_create_libros(nombre_, autor_, editorial_, fecha_, sector_b, sector_es):
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
        except:
            print("No se pudo obtener el error")

def insert_prestamos(fecha_i,fecha_m, rut_, nombre_, curso_, copia_):
    try:
        user_rut = selected_user_by_rut(rut_)
        if user_rut:
            user = user_rut[0][0]
            if user.curso != curso_:
                update_usuario(user.id_user, curso_)
        else:
            user = Usuario(
                nombre = nombre_,
                curso = curso_,
                rut = rut_
            )
            session.add(user)
            session.flush()
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
        except:
            print("No se pudo obtener el error")

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

def update_estado_impresion(fecha, estado):
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
        except:
            print("No se pudo obtener el error")

def update_estado_prestamos(id, estado):
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
        except:
            print("No se pudo obtener el error")

def update_usuario(id, curso_):
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
        except:
            print("No se pudo obtener el error")