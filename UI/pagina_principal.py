from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QSizePolicy, QWidget, QStackedWidget,
                             QPushButton, QTableWidgetItem, QTableWidget,
                             QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QApplication)
from PyQt5.QtCore import (QLocale, QSize, Qt, QRect, QMetaObject,
                          QCoreApplication)


class PaginaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        #Definicion de variable para cambios en los botones
        style_sheet = "background-color: #C7FF9C; " \
        "border-radius:25px; " \
        "width: 50; " \
        "height: 50;" \
        "border: 1px solid black;" \
        

        #Definicion de Layout
        vertical_layout_left = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        vertical_layout_right = QVBoxLayout()

        #Creacion de los botones
        self.registro_libros = QPushButton("Registro de Libros")
        self.registro_libros.setStyleSheet(style_sheet)
        self.prestamos_libro = QPushButton("Prestamo del Libro")
        self.prestamos_libro.setStyleSheet(style_sheet)
        self.inventario_libros = QPushButton("Inventario de Libros")
        self.inventario_libros.setStyleSheet(style_sheet)
        self.impresion = QPushButton("Menu de Impresiones")
        self.impresion.setStyleSheet(style_sheet)
        self.historial_prestamos = QPushButton("Historial de Prestamos")
        self.historial_prestamos.setStyleSheet(style_sheet)

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
