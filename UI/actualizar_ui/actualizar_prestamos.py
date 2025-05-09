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

style_sheet = "QWidget{background-color: #B4E7FF;}" "QPushButton{\
        background-color: #C7FF9C;\
        border-radius:5px;\
        border: 1px solid black;\
        }\
        \
        QPushButton:pressed{\
            background-color: greenyellow;\
            color: white\
        }" "QLineEdit{\
        background-color: white;\
        border-radius: 10;\
        border: 1px solid black;\
    }" "QTableWidget{\
        background-color: rgb(255, 241, 184);\
    }"

class ActualizarPrestamos(QWidget):
    actualizar_datos = pyqtSignal()
    cerrar_ventana = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Biblioteca | ACTUALIZACION ESTADO DE PRESTAMOS")
        self.setStyleSheet(style_sheet)
        self.setGeometry(20,200,980,700)

        #Layouts
        horizontal_layout_1 = QHBoxLayout()
        vertical_layout = QVBoxLayout()

        #Creacion del Combobox
        self.estados = QComboBox()
        self.estados.setStyleSheet("background-color: #FFFFFF;")

        #Creacion del checkbox
        self.validacion_usuario = QCheckBox()
        self.validacion_usuario.setText("Cerrar ventana luego de cambios")

        #Creacion de los botones
        self.boton_cambiar = QPushButton("Cambiar estados")

        #Creacion de la tabla
        self.tabla_prestamos = QTableWidget()
        self.tabla_prestamos.setColumnCount(8)

        item = QTableWidgetItem()
        item.setText("Nombre Alumno")
        self.tabla_prestamos.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Nombre Libro")
        self.tabla_prestamos.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setText("Codigo Barras")
        self.tabla_prestamos.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setText("Fecha Inicio Prestamo")
        self.tabla_prestamos.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        item.setText("Fecha Maxima de Prestamo")
        self.tabla_prestamos.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        item.setText("Estado Libro")
        self.tabla_prestamos.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        item.setText("Id Interno")
        self.tabla_prestamos.setHorizontalHeaderItem(6, item)
        item = QTableWidgetItem()
        item.setText("Id Interno Prestamos")
        self.tabla_prestamos.setHorizontalHeaderItem(7, item)

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

        self.setLayout(vertical_layout)

        #Funcionalidad del boton
        self.boton_cambiar.clicked.connect(self.actualizar_estado)

        #Rellenar ComboBox
        estado_prestamos = select_all_estado_prestamos()
        for es in estado_prestamos:
            self.estados.insertItem(es[0].id_estadoprestamo, es[0].estado_prestamo)

    def rellenar_tabla(self):
        self.tabla_prestamos.setRowCount(0)
        prestamos = select_prestamo_by_fecha(self.fechas)
        tablerow = 0
        self.tabla_prestamos.setRowCount(50)

        mal_estado = QColor(255, 205, 0)
        buen_estado = QColor(90,255,90)
        dado_baja = QColor(255,50,50)
        estado_regular = QColor(255,255,0)

        column_count = self.tabla_prestamos.columnCount()-3

        if prestamos:
            for p in prestamos:
                self.tabla_prestamos.setItem(tablerow, 0, QTableWidgetItem(p.nombre))
                self.tabla_prestamos.setItem(tablerow, 1, QTableWidgetItem(p.nombre_libro))
                self.tabla_prestamos.setItem(tablerow, 2, QTableWidgetItem(p.cod_barras))
                self.tabla_prestamos.setItem(tablerow, 3, QTableWidgetItem(str(p.fecha_inicio)))
                self.tabla_prestamos.setItem(tablerow, 4, QTableWidgetItem(str(p.fecha_termino)))
                self.tabla_prestamos.setItem(tablerow, 5, QTableWidgetItem(p.estado_libro))
                self.tabla_prestamos.setItem(tablerow, 6, QTableWidgetItem(str(p.id_copia)))
                self.tabla_prestamos.setItem(tablerow, 7, QTableWidgetItem(str(p.id_prestamos)))

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
        is_true = self.validacion_usuario.isChecked()
        if is_true is not True:
            self.camb_estado_pres_libro()
        else:
            self.camb_estado_pres_libro()
            self.cerrar_ventana.emit()
            self.close()

    def traer_fecha(self, fecha_item):
        self.fechas = fecha_item
        self.rellenar_tabla()
        return self.fechas
    
    def closeEvent(self, a0):
        self.cerrar_ventana.emit()
        a0.accept()

    def camb_estado_pres_libro(self):
        selected_rows = self.tabla_prestamos.selectionModel().selectedRows()
        if not selected_rows:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion erronea")
            msg.setText("No se ha seleccionado un libro")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
        estado_id = self.estados.currentIndex() + 1
        for row in selected_rows:
            id_copia = self.tabla_prestamos.item(row.row(), 6).text()
            id_prestamos = self.tabla_prestamos.item(row.row(), 7).text()
            if estado_id != 3:
                update_estado_prestamos(id_prestamos, estado_id)
            else:
                update_estado_prestamos(id_prestamos, estado_id)
                update_estado_libro(id_copia, 4)
        self.rellenar_tabla()
        self.actualizar_datos.emit()