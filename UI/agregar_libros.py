from PyQt5.QtWidgets import (QWidget, 
                             QPushButton,
                             QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QDateEdit)

from datetime import date
from PyQt5.QtCore import (pyqtSignal)

from connection.session import selected_libro_by_cod

class AgregarLibros(QWidget):
    volver_principal = pyqtSignal()
    def __init__(self):
        super().__init__()

        #Definicion de Layout
        void_layout_1 = QVBoxLayout()
        vertical_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        void_layout_2 = QVBoxLayout()

        void_horizontal_1 = QHBoxLayout()
        void_horizontal_2 = QHBoxLayout()

        
        #Creacion de los Widgets
        #LineEdit
        self.agregar_nombre = QLineEdit()
        self.agregar_nombre.setPlaceholderText("Ingrese nombre del libro")
        self.agregar_nombre.setDisabled(True)

        self.agregar_codigo = QLineEdit()
        self.agregar_codigo.setPlaceholderText("Ingrese el Codigo de Barras")

        self.agregar_autor = QLineEdit()
        self.agregar_autor.setPlaceholderText("Ingrese el Autor")
        self.agregar_autor.setDisabled(True)

        self.fecha_publicacion = QDateEdit()
        self.fecha_publicacion.setDisplayFormat("yyyy-MM-dd")
        self.fecha_publicacion.setCalendarPopup(True)
        self.fecha_publicacion.setDisabled(True)
        
        self.stock_libro = QLineEdit()
        self.stock_libro.setPlaceholderText("Ingrese el Stock disponible")
        #Botones
        self.button_agregar = QPushButton("Agregar nuevo Libro")
        self.volver_atras = QPushButton("Volver Atras")
        self.button_buscar = QPushButton("Buscar")
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

        #Setear Fecha
        fecha = date.today()
        fecha.strftime("%y-%m-/d")
        self.fecha_publicacion.setDate(fecha)

        #Edit labels
        self.nombre.setText("Nombre del Libro")
        self.codigo_barras.setText("Codigo de Barras del Libro")
        self.autor.setText("Nombre del Autor del Libro")
        self.publicacion.setText("Fecha de Publicación")
        self.stock.setText("Stock del libro")

        #Agregar los widgets al horizontal layout
        horizontal_layout.addWidget(self.agregar_codigo)
        horizontal_layout.addWidget(self.button_buscar)

        #Agregar Widgets al Layout
        vertical_layout.addLayout(void_layout_1)
        vertical_layout.addLayout(void_horizontal_1)
        vertical_layout.addWidget(self.codigo_barras)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(self.nombre)
        vertical_layout.addWidget(self.agregar_nombre)
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


        #Funcionalidad botones
        self.button_agregar.clicked.connect(self.agregar_boton)
        self.volver_atras.clicked.connect(self.volver_principal.emit)
        self.button_buscar.clicked.connect(self.boton_buscar)


    def boton_buscar(self):
        libro = selected_libro_by_cod(self.agregar_codigo.text())
        if libro:
            libro = libro[0][0]
            self.agregar_nombre.setText(libro.nombre_libro)
            self.agregar_autor.setText(libro.autor)
            self.fecha_publicacion.setDate(libro.fecha_publicacion)
        else:
            self.agregar_nombre.setDisabled(True)
            self.agregar_autor.setDisabled(True)
            self.fecha_publicacion.setDisabled(True)

    def agregar_boton(self):
        self.agregar_nombre.clear()
        self.agregar_codigo.clear()
        self.agregar_autor.clear()
        self.stock_libro.clear()