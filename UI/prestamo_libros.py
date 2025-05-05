from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QDateEdit, QHBoxLayout,
                             QTableWidget, QSpacerItem, QSizePolicy)

from PyQt5.QtCore import Qt

from datetime import date

from PyQt5.QtCore import pyqtSignal

class PrestamoLibros(QWidget):
    volver_principal = pyqtSignal()
    def __init__(self):
        super().__init__()

        #Definicion de layouts principal
        vertical_layout_principal = QVBoxLayout()

        #Definicion de Layout
        vertical_layout_1 = QVBoxLayout()

        vertical_layout_2 = QVBoxLayout()
        horizontal_layot_principal = QHBoxLayout()
        horizontal_layot_1 = QHBoxLayout()
        horizontal_layot_2 = QHBoxLayout()

        #Definicion de los LineEdit
        self.cod_barras = QLineEdit()
        self.cod_barras.setPlaceholderText("Ingrese el codigo de barras")
        self.rut_ = QLineEdit()
        self.rut_.setPlaceholderText("Ingrese el Rut del Alumno o Profesor")
        self.nombre_prestatario = QLineEdit()
        self.nombre_prestatario.setPlaceholderText("Ingrese el nombre del Alumno o Profesor")
        self.curso_prestatario = QLineEdit()
        self.curso_prestatario.setPlaceholderText("Ingrese el curso del prestatario")

        #Creacion de los labes
        self.codigo = QLabel("Codigo de Barras del Libro")
        self.fecha = QLabel("Fecha Maxima a Entregar")
        self.rut = QLabel("Rut del Alumno/Profesor")
        self.nombre = QLabel("Nombre del Alumno/Profesor")
        self.curso = QLabel("Curso del Alumno/Profesor")

        #Definicion de los botones
        self.boton_volver = QPushButton("Volver")
        self.boton_buscar_libro = QPushButton("Buscar")
        self.boton_buscar_rut = QPushButton("Buscar")
        self.boton_agregar_prestamo = QPushButton("Agregar Prestamo")

        #Definicion del LineEdit
        self.fecha_maxima = QDateEdit()
        self.fecha_maxima.setDisplayFormat("yyyy-MM-dd")
        self.fecha_maxima.setCalendarPopup(True)

        fecha = date.today()
        fecha.strftime("%Y-%m-%d")
        self.fecha_maxima.setDate(fecha)

        #Definicion de la tabla
        self.tabla_libros = QTableWidget()
        self.tabla_libros.setMaximumHeight(200)

        vertical_layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)

        


        #Agregar los widgets a los layouts
        horizontal_layot_principal.addLayout(vertical_layout_1)
        vertical_layout_1.addWidget(self.codigo)
        horizontal_layot_1.addWidget(self.cod_barras)
        horizontal_layot_1.addWidget(self.boton_buscar_libro)
        vertical_layout_1.addLayout(horizontal_layot_1)
        vertical_layout_1.addWidget(self.fecha)
        vertical_layout_1.addWidget(self.fecha_maxima)
        vertical_layout_1.addWidget(self.tabla_libros)
        horizontal_layot_principal.addLayout(vertical_layout_2)
        vertical_layout_2.addWidget(self.rut)
        vertical_layout_2.addLayout(horizontal_layot_2)
        horizontal_layot_2.addWidget(self.rut_)
        horizontal_layot_2.addWidget(self.boton_buscar_rut)
        vertical_layout_2.addWidget(self.nombre)
        vertical_layout_2.addWidget(self.nombre_prestatario)
        vertical_layout_2.addWidget(self.curso)
        vertical_layout_2.addWidget(self.curso_prestatario)
        vertical_layout_principal.addLayout(horizontal_layot_principal)
        vertical_layout_principal.addWidget(self.boton_agregar_prestamo)
        vertical_layout_principal.addWidget(self.boton_volver)

        vertical_layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout_principal.setContentsMargins(10,10,10,10)
        vertical_layout_principal.setSpacing(0)

        self.setLayout(vertical_layout_principal)
        
        fecha = date.today()
        fecha.strftime("%y-%m-/d")
        #Funcionamiento Boton
        self.boton_volver.clicked.connect(self.volver_principal.emit)

        self.setFixedSize(1000, 650)

