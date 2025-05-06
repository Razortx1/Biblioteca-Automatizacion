from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QLineEdit, QComboBox, QCheckBox,
                             QTableWidget, QTableWidgetItem,
                             QAbstractItemView, QPushButton)
from PyQt5.QtCore import pyqtSignal

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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Biblioteca | ACTUALIZACION ESTADO DE PRESTAMOS")
        self.setStyleSheet(style_sheet)
        self.setGeometry(20,200,700,700)

        #Layouts
        horizontal_layout_1 = QHBoxLayout()
        vertical_layout = QVBoxLayout()
        horizontal_layout_2 = QHBoxLayout()

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
        self.tabla_prestamos.setColumnCount(4)

        item = QTableWidgetItem()
        item.setText("Nombre Libro")
        self.tabla_prestamos.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Codigo de Barras")
        self.tabla_prestamos.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setText("Autor")
        self.tabla_prestamos.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setText("Fecha Publicacion")
        self.tabla_prestamos.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        item.setText("Estado del Libro")
        self.tabla_prestamos.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        item.setText("Id Interno")
        self.tabla_prestamos.setHorizontalHeaderItem(5, item)

        self.tabla_prestamos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_prestamos.setSelectionMode(QAbstractItemView.MultiSelection)

        vertical_layout.addWidget(self.tabla_prestamos)
        horizontal_layout_1.addWidget(self.boton_cambiar)
        horizontal_layout_1.addWidget(self.estados)
        horizontal_layout_1.addWidget(self.validacion_usuario)
        vertical_layout.addLayout(horizontal_layout_1)

        self.setLayout(vertical_layout)




        