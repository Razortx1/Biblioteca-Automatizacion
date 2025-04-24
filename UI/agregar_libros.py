from PyQt5.QtWidgets import (QSizePolicy, QWidget, QStackedWidget,
                             QPushButton, QTableWidgetItem, QTableWidget,
                             QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QApplication)
from PyQt5.QtCore import (QLocale, QSize, Qt, QRect, QMetaObject,
                          QCoreApplication)

class AgregarLibros(QWidget):
    def __init__(self):
        super().__init__()

        #Definicion de los estilos para boton y lineEdit
        style_sheet_button = "background-color: #C7FF9C; " \
        "border-radius:25px; " \
        "width: 50; " \
        "height: 50;" \
        "border: 1px solid black;"
        style_sheet_lineedit = "border-radius: 10; border:1px solid black;" \
        "background-color: #FFFFFFFF; height: 40;"

        #Definicion de Layout
        void_layout_1 = QVBoxLayout()
        vertical_layout = QVBoxLayout()
        void_layout_2 = QVBoxLayout()

        void_horizontal_1 = QHBoxLayout()
        void_horizontal_2 = QHBoxLayout()

        
        #Creacion de los Widgets
        #LineEdit
        self.agregar_nombre = QLineEdit()
        self.agregar_nombre.setStyleSheet(style_sheet_lineedit)
        self.agregar_nombre.setPlaceholderText("Ingrese nombre del libro")
        self.agregar_codigo = QLineEdit()
        self.agregar_codigo.setStyleSheet(style_sheet_lineedit)
        self.agregar_codigo.setPlaceholderText("Ingrese el Codigo de Barras")
        self.agregar_autor = QLineEdit()
        self.agregar_autor.setStyleSheet(style_sheet_lineedit)
        self.agregar_autor.setPlaceholderText("Ingrese el Autor")
        self.fecha_publicacion = QLineEdit()
        self.fecha_publicacion.setStyleSheet(style_sheet_lineedit)
        self.stock_libro = QLineEdit()
        self.stock_libro.setStyleSheet(style_sheet_lineedit)
        self.stock_libro.setPlaceholderText("Ingrese el Stock disponible")
        #Botones
        self.button_agregar = QPushButton("Agregar nuevo Libro")
        self.button_agregar.setStyleSheet(style_sheet_button)
        self.volver_atras = QPushButton("Volver a Inicio")
        self.volver_atras.setStyleSheet(style_sheet_button)
        #Labels
        self.nombre = QLabel()
        self.codigo_barras = QLabel()
        self.autor = QLabel()
        self.publicacion = QLabel()
        self.stock = QLabel()

        self.voidLabel_1 = QLabel()
        self.voidLabel_2 = QLabel()
        self.voidLabel_3 = QLabel()
        self.voidLabel_4 = QLabel()
        void_layout_1.addWidget(self.voidLabel_1)
        void_layout_2.addWidget(self.voidLabel_2)
        void_horizontal_1.addWidget(self.voidLabel_3)
        void_horizontal_2.addWidget(self.voidLabel_4)

        #Edit labels
        self.nombre.setText("Nombre del Libro")
        self.codigo_barras.setText("Codigo de Barras del Libro")
        self.autor.setText("Nombre del Autor del Libro")
        self.publicacion.setText("Fecha de Publicación")
        self.stock.setText("Stock del libro")

        #Agregar Widgets al Layout
        vertical_layout.addLayout(void_layout_1)
        vertical_layout.addLayout(void_horizontal_1)
        vertical_layout.addWidget(self.nombre)
        vertical_layout.addWidget(self.agregar_nombre)
        vertical_layout.addWidget(self.codigo_barras)
        vertical_layout.addWidget(self.agregar_codigo)
        vertical_layout.addWidget(self.autor)
        vertical_layout.addWidget(self.agregar_autor)
        vertical_layout.addWidget(self.publicacion)
        vertical_layout.addWidget(self.fecha_publicacion)
        vertical_layout.addWidget(self.stock)
        vertical_layout.addWidget(self.stock_libro)
        vertical_layout.addWidget(self.button_agregar)
        vertical_layout.addWidget(self.volver_atras)
        vertical_layout.addLayout(void_layout_2)
        vertical_layout.addLayout(void_horizontal_2)
        self.setLayout(vertical_layout)