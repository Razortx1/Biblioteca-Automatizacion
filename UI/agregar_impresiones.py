from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QHBoxLayout,
                             QTextEdit)

from PyQt5.QtCore import (pyqtSignal)
from connection.session import selected_user_by_rut
from connection.connection import ingresar_impresiones

class AgregarImpresiones(QWidget):
    volver_menu = pyqtSignal()
    def __init__(self):
        super().__init__()

        #Definicion de Layout
        horizontal_layout = QHBoxLayout()
        vertical_layout = QVBoxLayout()
        void_layout_1 = QVBoxLayout()
        void_layout_2 = QVBoxLayout()

        self.voidLabel_1 = QLabel()
        self.voidLabel_2 = QLabel()

        #Creacion de los Widgets
        #LineEdit
        self.nombre_solicitante = QLineEdit()
        self.nombre_solicitante.setPlaceholderText("Ingrese el nombre del Alumno/Profesor")
        self.nombre_solicitante.setDisabled(True)

        self.rut_solicitante = QLineEdit()
        self.rut_solicitante.setPlaceholderText("Ingrese el rut Alumno/Profesor")
        self.rut_solicitante.setInputMask("00.000.000-n;_")

        self.cursos = QLineEdit()
        self.cursos.setPlaceholderText("Ingrese Curso o Departamento")
        self.cursos.setDisabled(True)

        self.cantidad_copias = QLineEdit()
        self.cantidad_copias.setPlaceholderText("Ingrese la cantidad de Copias")

        self.cantidad_paginas = QLineEdit()
        self.cantidad_paginas.setPlaceholderText("Ingrese la cantidad de Paginas del documento")

        self.descripcion = QTextEdit()
        self.descripcion.setPlaceholderText("Ingrese la descripcion de la impresion")

        #Creacion de los botones
        self.boton_agregar = QPushButton("Agregar Impresion")
        self.boton_volver = QPushButton("Volver al menu de Impresiones")
        self.boton_buscar_usuario = QPushButton("Buscar")

        horizontal_layout.addWidget(self.rut_solicitante)
        horizontal_layout.addWidget(self.boton_buscar_usuario)

        #Lables
        self.nombre = QLabel()
        self.rut = QLabel()
        self.cantidad_c = QLabel()
        self.cantidad_p = QLabel()
        self.curso = QLabel()
        self.descip = QLabel()

        void_layout_1.addWidget(self.voidLabel_1)
        void_layout_2.addWidget(self.voidLabel_2)

        #Asignar text a los labels
        self.nombre.setText("Nombre Alumno/Profesor")
        self.rut.setText("Rut del alumno/profesor")
        self.cantidad_c.setText("Cantidad de Copias a necesitar")
        self.cantidad_p.setText("Cantidad de paginas que tiene el documento en total")
        self.curso.setText("Curso/Departamento")
        self.descip.setText("Descripcion de la Impresion")

        #Asignar los Widgets al Layout
        vertical_layout.addWidget(self.rut)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(self.nombre)
        vertical_layout.addWidget(self.nombre_solicitante)
        vertical_layout.addWidget(self.curso)
        vertical_layout.addWidget(self.cursos)        
        vertical_layout.addWidget(self.cantidad_c)
        vertical_layout.addWidget(self.cantidad_copias)
        vertical_layout.addWidget(self.cantidad_p)
        vertical_layout.addWidget(self.cantidad_paginas)
        vertical_layout.addWidget(self.descip)
        vertical_layout.addWidget(self.descripcion)
        vertical_layout.addWidget(self.boton_agregar)
        vertical_layout.addWidget(self.boton_volver)
        vertical_layout.addLayout(void_layout_1)
        vertical_layout.addLayout(void_layout_2)

        self.setLayout(vertical_layout)

        #Agregar funcionalidades al boton
        self.boton_buscar_usuario.clicked.connect(self.buscar_rut)
        self.boton_agregar.clicked.connect(self.agregar_prestamo)
        self.boton_volver.clicked.connect(self.volver_menu.emit)

    #Funcionalidades que tendran los botones
    def buscar_rut(self):
        rut = self.rut_solicitante.text()
        user = selected_user_by_rut(rut)
        if user:
            user = user[0][0]
            self.nombre_solicitante.setText(user.nombre)
            self.cursos.setText(user.curso)
        else:
            self.nombre_solicitante.setDisabled(False)
            self.nombre_solicitante.clear()
            self.cursos.setDisabled(False)
            self.cursos.clear()

    def agregar_prestamo(self):
        nombre = self.nombre_solicitante.text()
        curso = self.cursos.text()
        rut = self.rut_solicitante.text()
        copias = self.cantidad_copias.text()
        paginas = self.cantidad_paginas.text()
        descrip = self.descripcion.toPlainText()
        ingresar_impresiones(nombre, curso, rut ,copias, paginas, descrip)
        self.rut_solicitante.clear()
        self.nombre_solicitante.clear()
        self.cursos.clear()
        self.cantidad_copias.clear()
        self.cantidad_paginas.clear()
        self.descripcion.clear()

    
        