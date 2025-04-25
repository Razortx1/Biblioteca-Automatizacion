from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel)
from PyQt5.QtCore import (pyqtSignal)

class AgregarImpresiones(QWidget):
    volver_menu = pyqtSignal()
    def __init__(self):
        super().__init__()

        #Definicion de Layout
        vertical_layout = QVBoxLayout()
        void_layout_1 = QVBoxLayout()
        void_layout_2 = QVBoxLayout()

        self.voidLabel_1 = QLabel()
        self.voidLabel_2 = QLabel()

        #Creacion de los Widgets
        #LineEdit
        self.nombre_solicitante = QLineEdit()
        self.nombre_solicitante.setPlaceholderText("Ingrese el nombre del Alumno/Profesor")

        self.rut_solicitante = QLineEdit()
        self.rut_solicitante.setPlaceholderText("Ingrese el rut Alumno/Profesor")

        self.cantidad_copias = QLineEdit()
        self.cantidad_copias.setPlaceholderText("Ingrese la cantidad de Copias")

        self.cantidad_paginas = QLineEdit()
        self.cantidad_paginas.setPlaceholderText("Ingrese la cantidad de Paginas del documento")

        #Creacion de los botones
        self.boton_volver = QPushButton("Volver al menu de Impresiones")

        #Lables
        self.nombre = QLabel()
        self.rut = QLabel()
        self.cantidad_c = QLabel()
        self.cantidad_p = QLabel()

        void_layout_1.addWidget(self.voidLabel_1)
        void_layout_2.addWidget(self.voidLabel_2)

        #Asignar text a los labels
        self.nombre.setText("Nombre Alumno/Profesor")
        self.rut.setText("Rut del alumno/profesor")
        self.cantidad_c.setText("Cantidad de Copias a necesitar")
        self.cantidad_p.setText("Cantidad de paginas que tiene el documento en total")

        #Asignar los Widgets al Layout
        vertical_layout.addWidget(self.nombre)
        vertical_layout.addWidget(self.nombre_solicitante)
        vertical_layout.addWidget(self.rut)
        vertical_layout.addWidget(self.rut_solicitante)
        vertical_layout.addWidget(self.cantidad_c)
        vertical_layout.addWidget(self.cantidad_copias)
        vertical_layout.addWidget(self.cantidad_p)
        vertical_layout.addWidget(self.cantidad_paginas)
        vertical_layout.addWidget(self.boton_volver)
        vertical_layout.addLayout(void_layout_1)
        vertical_layout.addLayout(void_layout_2)

        self.setLayout(vertical_layout)

        self.boton_volver.clicked.connect(self.volver_menu.emit)