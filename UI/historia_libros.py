from PyQt5.QtWidgets import (QSizePolicy, QWidget, QStackedWidget,
                             QPushButton, QTableWidgetItem, QTableWidget,
                             QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QApplication, QHeaderView)
from PyQt5.QtCore import (QLocale, QSize, Qt, QRect, QMetaObject,
                          QCoreApplication, pyqtSignal)

from PyQt5.QtGui import QColor

class HistorialLibros(QWidget):
    volver_principal = pyqtSignal()
    def __init__(self):
        super().__init__()            
        
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

        #Tamaño Columnas
        header = self.tabla_libros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        #Creacion botones
        self.cambiar_estado = QPushButton("Cambiar Estado Libro")
        self.volver_inicio = QPushButton("Volver a Inicio")

        #Agregar los Widget al layout principal
        vertical_layout.addWidget(self.tabla_libros)
        vertical_layout.addWidget(self.cambiar_estado)
        vertical_layout.addWidget(self.volver_inicio)
        vertical_layout.addLayout(void_layout_1)
        vertical_layout.addLayout(void_layout_2)
        
        #Vaciado de tabla
        self.tabla_libros.setRowCount(0)

        #Relleno de Tabla
        self.rellenar_tabla()

        #Agregar el layout a la respectiva lista
        self.setLayout(vertical_layout)

        #Funcionamiento Botones
        self.volver_inicio.clicked.connect(self.volver_principal.emit)


    def rellenar_tabla(self):
        pass