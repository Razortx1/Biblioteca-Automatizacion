from PyQt5.QtWidgets import (QSizePolicy, QWidget, QStackedWidget,
                             QPushButton, QTableWidgetItem, QTableWidget,
                             QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QApplication, QHeaderView)
from PyQt5.QtCore import (QLocale, QSize, Qt, QRect, QMetaObject,
                          QCoreApplication)

class HistorialLibros(QWidget):
    def __init__(self):
        super().__init__()

        #Definicion de variable para cambios en los botones
        style_sheet = "background-color: #C7FF9C; " \
        "border-radius:25px; " \
        "width: 50; " \
        "height: 50;" \
        "border: 1px solid black;"

        #Definicion del layout
        void_layout_1 = QVBoxLayout()
        void_layout_2 = QVBoxLayout()
        vertical_layout = QVBoxLayout()

        self.voidLabel_1 = QLabel()
        self.voidLabel_2 = QLabel()
        void_layout_1.addWidget(self.voidLabel_1)
        void_layout_2.addWidget(self.voidLabel_2)
        #Creacion de la tabla
        self.tabla_libros = QTableWidget()
        self.tabla_libros.setColumnCount(6)
        item = QTableWidgetItem()
        item.setText("Nombre Libro")
        self.tabla_libros.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Codigo de Barras")
        self.tabla_libros.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setText("Autor")
        self.tabla_libros.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setText("Fecha Publicacion")
        self.tabla_libros.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        item.setText("Stock de Libros")
        self.tabla_libros.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        item.setText("Estado del Libro")
        self.tabla_libros.setHorizontalHeaderItem(5, item)
        self.tabla_libros.setStyleSheet("background-color: rgb(255, 241, 184)")

        #Tamaño Columnas
        header = self.tabla_libros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        #Creacion botones
        self.cambiar_estado = QPushButton("Cambiar Estado Libro")
        self.cambiar_estado.setStyleSheet(style_sheet)
        self.volver_inicio = QPushButton("Volver a Inicio")
        self.volver_inicio.setStyleSheet(style_sheet)

        #Agregar los Widget al layout principal
        vertical_layout.addWidget(self.tabla_libros)
        vertical_layout.addWidget(self.cambiar_estado)
        vertical_layout.addWidget(self.volver_inicio)
        vertical_layout.addLayout(void_layout_1)
        vertical_layout.addLayout(void_layout_2)

        #Agregar el layout a la respectiva lista
        self.setLayout(vertical_layout)
