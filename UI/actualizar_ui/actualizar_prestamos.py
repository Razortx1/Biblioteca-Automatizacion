"""
    **Modulo actualizar_prestamos**\n
    Es el modulo que se encarga de la parte visual con la cual el usuario
    podra hacer la actualizaciones con respecto a los estados de los prestamos\n

    **Importaciones del modulo**\n
    PyQt5.QtWidgets ----> Usado principalmente para obtener los widgets que serán
                            usados durante la actualizacion del estado del prestamo\n
    PyQt5.QtCore ----> Usado para obtener, ya sean las señales, o algunas
                        configuraciones adicionales para los widgets\n
    PyQt.QtGui -----> Usado para cambiar los colores de la ultima columna de la tabla

    modulo connection ----> Usado para traer la funcion update_estado_libro y el
                            update_estado_prestamos, esto con el fin
                            de poder actualizar el estado del libro a la base de datos, tomando los datos
                            encontrados en los widgets\n
    modulo session -----> Usado para poder obtener todos los estados del prestamo y los libros que 
                            pertenezcan al prestamo

"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QMessageBox, QComboBox, QCheckBox,
                             QTableWidget, QTableWidgetItem,
                             QAbstractItemView, QPushButton,
                             QHeaderView)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor

from connection.session import (select_all_estado_prestamos,
                                select_prestamo_by_fecha)
from connection.connection import update_estado_libro, update_estado_prestamos

style_sheet = """
QWidget#ActualizarPrestamos {
    background-color: #6ec1e4;
}

QPushButton {
    background-color: #61ce70;
    color: #000000;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 14px;
    border: 1px solid #009c88;
    outline: none;
    height: 25px;
}

QPushButton:hover {
    background-color: #79db8a;
}

QPushButton:pressed {
    background-color: #4fa75e
}

QLineEdit,
QComboBox {
    background-color: #ffffff;
    border: 1px solid #bbb;
    border-radius: 8px;
    padding: 10px;
}
QTableWidget {
    background-color: #fdf9e3;
    border: 1px solid #ccc;
    font-size: 14px;
}

QHeaderView::section {
    background-color: #f7bc09;
    font-weight: bold;
    padding: 6px;
    border: none;
    color: #54595F
}
"""

class ActualizarPrestamos(QWidget):
    """
    **Clase ActualizarPrestamos**\n
    Permite el poder actualizar los estados del prestamo de los diferentes libros que se encuentran
    actualmente prestados, a traves una interfaz algo parecida a los formularios. Este formulario
    cuenta con los siguientes campos:\n

    - Datos pertenecientes a la tabla\n
    - Estado del prestamo a partir de ComboBox
    """
    actualizar_datos = pyqtSignal()
    cerrar_ventana = pyqtSignal()
    def __init__(self):
        """
        **Funcion __ init __**
        Se encarga de cargar tanto los widgets como los datos correspondientes a estos,
        donde a penas se detecta que el usuario presiono actualizar prestamos
        """
        super().__init__()
        self.setWindowTitle("Sistema Biblioteca | ACTUALIZACION ESTADO DE PRESTAMOS")
        self.setObjectName("ActualizarPrestamos")
        self.setAutoFillBackground(True)
        self.setStyleSheet(style_sheet)
        self.setGeometry(20,200,980,700)

        #Layouts
        horizontal_layout_1 = QHBoxLayout()
        vertical_layout = QVBoxLayout()

        #Creacion del Combobox
        self.estados = QComboBox()

        #Creacion del checkbox
        self.validacion_usuario = QCheckBox()
        self.validacion_usuario.setText("Cerrar ventana luego de cambios")

        #Creacion de los botones
        self.boton_cambiar = QPushButton("Cambiar el estado del prestamo(s)")

        #Creacion de la tabla
        self.tabla_prestamos = QTableWidget()
        self.tabla_prestamos.setColumnCount(9)

        item = QTableWidgetItem()
        item.setText("Nombre Alumno")
        self.tabla_prestamos.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Nombre Libro")
        self.tabla_prestamos.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setText("Autor")
        self.tabla_prestamos.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setText("Editorial")
        self.tabla_prestamos.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        item.setText("Fecha Inicio Prestamo")
        self.tabla_prestamos.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        item.setText("Fecha Maxima de Prestamo")
        self.tabla_prestamos.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        item.setText("Estado Libro")
        self.tabla_prestamos.setHorizontalHeaderItem(6, item)
        item = QTableWidgetItem()
        item.setText("Id Interno")
        self.tabla_prestamos.setHorizontalHeaderItem(7, item)
        item = QTableWidgetItem()
        item.setText("Id Interno Prestamos")
        self.tabla_prestamos.setHorizontalHeaderItem(8, item)

        self.tabla_prestamos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_prestamos.setSelectionMode(QAbstractItemView.MultiSelection)


        #Cambios en el header de la tabla
        header = self.tabla_prestamos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        vertical_layout.addWidget(self.tabla_prestamos)
        horizontal_layout_1.addWidget(self.boton_cambiar)
        horizontal_layout_1.addWidget(self.estados)
        horizontal_layout_1.addWidget(self.validacion_usuario)
        vertical_layout.addLayout(horizontal_layout_1)
        self.tabla_prestamos.setColumnHidden(7, True)
        self.tabla_prestamos.setColumnHidden(8, True)

        self.setLayout(vertical_layout)

        #Funcionalidad del boton
        self.boton_cambiar.clicked.connect(self.actualizar_estado)

        #Rellenar ComboBox
        estado_prestamos = select_all_estado_prestamos()
        for es in estado_prestamos:
            self.estados.insertItem(es[0].id_estadoprestamo, es[0].estado_prestamo)

    def rellenar_tabla(self):
        """
        **Funcion rellenar_tabla**\n
        Es la encargada de obtener todos los datos de los libros para luego cargalos a la tabla\n
        """
        self.tabla_prestamos.setRowCount(0)
        prestamos = select_prestamo_by_fecha(self.fechas)
        tablerow = 0

        mal_estado = QColor("#ffd62e")  # Mal estado
        buen_estado = QColor("#b2f7b2")  # Buen estado
        dado_baja = QColor("#ff6b6b")  # Dado de baja
        estado_regular = QColor("#ffe066")  # Estado regular

        column_count = self.tabla_prestamos.columnCount()-3

        if prestamos:
            for p in prestamos:
                row_position = self.tabla_prestamos.rowCount()
                self.tabla_prestamos.insertRow(row_position)
                self.tabla_prestamos.setItem(tablerow, 0, QTableWidgetItem(p.nombre))
                self.tabla_prestamos.setItem(tablerow, 1, QTableWidgetItem(p.nombre_libro))
                self.tabla_prestamos.setItem(tablerow, 2, QTableWidgetItem(p.autor))
                self.tabla_prestamos.setItem(tablerow, 3, QTableWidgetItem(p.editorial))
                self.tabla_prestamos.setItem(tablerow, 4, QTableWidgetItem(str(p.fecha_inicio)))
                self.tabla_prestamos.setItem(tablerow, 5, QTableWidgetItem(str(p.fecha_termino)))
                self.tabla_prestamos.setItem(tablerow, 6, QTableWidgetItem(p.estado_libro))
                self.tabla_prestamos.setItem(tablerow, 7, QTableWidgetItem(str(p.id_copia)))
                self.tabla_prestamos.setItem(tablerow, 8, QTableWidgetItem(str(p.id_prestamos)))

                texto_tabla = self.tabla_prestamos.item(tablerow, column_count).text()

                if texto_tabla == "Buen Estado":
                    self.tabla_prestamos.item(tablerow, column_count).setBackground(buen_estado)
                elif texto_tabla == "Mal Estado":
                    self.tabla_prestamos.item(tablerow, column_count).setBackground(mal_estado)
                elif texto_tabla == "Estado Regular":
                    self.tabla_prestamos.item(tablerow, column_count).setBackground(estado_regular)
                elif texto_tabla == "Dado de Baja":
                    self.tabla_prestamos.item(tablerow, column_count).setBackground(dado_baja)

                tablerow+=1



    def actualizar_estado(self):
        """
        **Funcion actualizar_estado**\n
        Es la encargada de comprobar el estado actual del checkbox, esto con el fin de poder
        cerrar o no cerrar la ventana si es que el usuario no lo desea
        """
        is_true = self.validacion_usuario.isChecked()
        if is_true is not True:
            self.camb_estado_pres_libro()
            print("Cambiando")
        else:
            self.camb_estado_pres_libro()
            self.cerrar_ventana.emit()
            print("cambiando y cerrando")
            self.close()

    def traer_fecha(self, fecha_item):
        """
        **Funcion traer_fecha**\n
        Se encarga de traer los datos de los libros a traves de la señal propuesta por historial_prestamo

        **Parametros**\n
        - fecha_item: str | datetime

        **Retorna**\n
        fechas: str | datetime
        """
        self.fechas = fecha_item
        self.rellenar_tabla()
        return self.fechas
    
    def closeEvent(self, a0):
        """
        **Funcion closeEvent**\n
        Detecta si la ventana se cierra ya sea a traves de un boton o si se cierra
        por el boton de la X. Esto permite que se pueda volver a abrir sin necesidad
        de cerrar la aplicacion
        """
        self.cerrar_ventana.emit()
        a0.accept()

    def camb_estado_pres_libro(self):
        """
        **Funcion camb_estado_pres_libro**\n
        Permite la actualizacion de los prestamos con respecto a su estado, con
        diversos validadores para poder comprobar si fue seleccionado un prestamo o no,
        o si en caso que el usuario no desee actualizar ahora el prestamo
        """
        selected_rows = self.tabla_prestamos.selectionModel().selectedRows()
        if not selected_rows:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion erronea")
            msg.setText("Debe seleccionar al menos un libro")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
        estado_id = self.estados.currentIndex() + 1
        for row in selected_rows:
            id_copia = self.tabla_prestamos.item(row.row(), 7).text()
            id_prestamos = self.tabla_prestamos.item(row.row(), 8).text()
            if estado_id != 3:
                update_estado_prestamos(id_prestamos, estado_id)
            elif estado_id == 3:
                update_estado_prestamos(id_prestamos, estado_id)
                update_estado_libro(id_copia, 4)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Error de Logica")
                msg.setText("Se cometio un error de logica dentro del programa. Favor de llamar a tecnico a cargo")
                msg.setIcon(QMessageBox.Warning)
                msg.exec()
        self.rellenar_tabla()
        self.actualizar_datos.emit()