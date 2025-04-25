from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QSizePolicy, QWidget,
                             QPushButton, QTableWidgetItem, QTableWidget,
                             QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import (QLocale, QSize, Qt, QRect, QMetaObject,
                          QCoreApplication, pyqtSignal)


class PaginaPrincipal(QWidget):
    #Definicion de señales
    ir_a_agregar_libros = pyqtSignal()
    ir_a_historia_libros = pyqtSignal()
    ir_prestamo_libro = pyqtSignal()
    ir_a_menu_impresiones = pyqtSignal()
    ir_a_historial_prestamo = pyqtSignal()

    def __init__(self):

        super().__init__()
        
        #Definicion de Layout
        vertical_layout_left = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        vertical_layout_right = QVBoxLayout()

        #Creacion de los botones
        self.registro_libros = QPushButton("Registro de Libros")
        self.prestamos_libro = QPushButton("Prestamo del Libro")
        self.inventario_libros = QPushButton("Inventario de Libros")
        self.impresion = QPushButton("Menu de Impresiones")
        self.historial_prestamos = QPushButton("Historial de Prestamos")

        #Agregando los botones al layout
        vertical_layout_left.addWidget(self.registro_libros)
        vertical_layout_left.addWidget(self.prestamos_libro)
        horizontal_layout.addLayout(vertical_layout_left)
        horizontal_layout.addWidget(self.inventario_libros)
        vertical_layout_right.addWidget(self.impresion)
        vertical_layout_right.addWidget(self.historial_prestamos)
        horizontal_layout.addLayout(vertical_layout_right)

        #Agregar los layouts en la respectiva vista
        self.setLayout(horizontal_layout)

        #Funciones del Boton
        self.registro_libros.clicked.connect(self.ir_a_agregar_libros.emit)
        self.inventario_libros.clicked.connect(self.ir_a_historia_libros.emit)
        self.prestamos_libro.clicked.connect(self.ir_prestamo_libro.emit)
        self.impresion.clicked.connect(self.ir_a_menu_impresiones.emit)
        self.historial_prestamos.clicked.connect(self.ir_a_historial_prestamo.emit)