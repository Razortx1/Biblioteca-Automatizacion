from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel)
from PyQt5.QtCore import pyqtSignal

class PrestamoLibros(QWidget):
    volver_principal = pyqtSignal()
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
        self.nombre_solicitante.setPlaceholderText("Ingrese el nombre del solicitante")

        self.curso_solicitante = QLineEdit()
        self.curso_solicitante.setPlaceholderText("Ingrese el curso o departamento que pertenezca")

        self.rut_solicitante = QLineEdit()
        self.rut_solicitante.setPlaceholderText("Ingresa el rut del solicitante")
        
        self.fecha_maxima = QLineEdit()

        self.codigo_barras = QLineEdit()
        self.codigo_barras.setPlaceholderText("Ingrese el codigo de barras del libro")

        #Botones
        self.boton_agregar = QPushButton("Inscribir Prestamo")
        self.boton_volver = QPushButton("Volver al Inicio")

        #Labels
        self.nombre = QLabel()
        self.curso = QLabel()
        self.rut = QLabel()
        self.maximo = QLabel()
        self.barras = QLabel()

        #Asignar texto a los labels
        self.nombre.setText("Nombre del Alumno")
        self.curso.setText("Curso del Solicitante")
        self.rut.setText("Ingrese el rut del solicitante")
        self.maximo.setText("Ingrese plazo maximo para entregar el libro")
        self.barras.setText("Ingrese el codigo de barras")

        void_layout_1.addWidget(self.voidLabel_1)
        void_layout_2.addWidget(self.voidLabel_2)

        vertical_layout.addWidget(self.nombre)
        vertical_layout.addWidget(self.nombre_solicitante)
        vertical_layout.addWidget(self.curso)
        vertical_layout.addWidget(self.curso_solicitante)
        vertical_layout.addWidget(self.rut)
        vertical_layout.addWidget(self.rut_solicitante)
        vertical_layout.addWidget(self.maximo)
        vertical_layout.addWidget(self.fecha_maxima)
        vertical_layout.addWidget(self.barras)
        vertical_layout.addWidget(self.codigo_barras)
        vertical_layout.addWidget(self.boton_agregar)
        vertical_layout.addWidget(self.boton_volver)
        vertical_layout.addLayout(void_layout_1)
        vertical_layout.addLayout(void_layout_2)

        self.setLayout(vertical_layout)

        #Funcionamiento Boton
        self.boton_volver.clicked.connect(self.volver_principal.emit)

