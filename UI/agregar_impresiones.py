from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QHBoxLayout,
                             QTextEdit, QCheckBox, QSizePolicy)

from PyQt5.QtCore import (pyqtSignal, Qt)

from connection.session import selected_user_by_rut
from connection.connection import ingresar_impresiones


class AgregarImpresiones(QWidget):
    volver_menu = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Definición de Layouts
        main_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Ajustar márgenes y espaciado para tener menos espacio entre los widgets
        main_layout.setContentsMargins(10, 10, 10, 10)  # Márgenes del layout principal
        main_layout.setSpacing(5)  # Espaciado entre los widgets

        horizontal_layout.setContentsMargins(5, 5, 5, 5)  # Márgenes de horizontal_layout
        horizontal_layout.setSpacing(5)  # Espaciado dentro de horizontal_layout

        self.setFixedHeight(600)

        # Creación de los Widgets
        self.nombre_solicitante = self.crear_line_edit("Ingrese el nombre del Alumno/Profesor", True)
        self.rut_solicitante = self.crear_line_edit("Ingrese el rut Alumno/Profesor", False, "00.000.000-n;_")
        self.cursos = self.crear_line_edit("Ingrese Curso o Departamento", True)

        self.cambiar_curso = QCheckBox("Habilitar para cambiar departamento o curso")
        self.cambiar_curso.stateChanged.connect(self.check_event)

        self.cantidad_copias = self.crear_line_edit("Ingrese la cantidad de Copias", False)
        self.cantidad_paginas = self.crear_line_edit("Ingrese la cantidad de Paginas del documento", False)

        self.descripcion = QTextEdit()
        self.descripcion.setPlaceholderText("Ingrese la descripcion de la impresion")
        self.descripcion.setMaximumHeight(100)  # Limitar altura de la caja de texto

        # Botones
        self.boton_agregar = QPushButton("Agregar Impresion")
        self.boton_volver = QPushButton("Volver al menu de Impresiones")
        self.boton_buscar_usuario = QPushButton("Buscar")

        # Organizar en Layouts
        horizontal_layout.addWidget(self.rut_solicitante)
        horizontal_layout.addWidget(self.boton_buscar_usuario)

        self.nombre = self.crear_label("Nombre Alumno/Profesor")
        self.rut = self.crear_label("Rut del alumno/profesor")
        self.cantidad_c = self.crear_label("Cantidad de Copias a necesitar")
        self.cantidad_p = self.crear_label("Cantidad de paginas que tiene el documento en total")
        self.curso = self.crear_label("Curso/Departamento")
        self.descip = self.crear_label("Descripcion de la Impresion")

        # Configurar el Layout principal
        main_layout.addWidget(self.rut)
        main_layout.addLayout(horizontal_layout)
        main_layout.addWidget(self.nombre)
        main_layout.addWidget(self.nombre_solicitante)
        main_layout.addWidget(self.curso)
        main_layout.addWidget(self.cursos)
        main_layout.addWidget(self.cantidad_c)
        main_layout.addWidget(self.cantidad_copias)
        main_layout.addWidget(self.cantidad_p)
        main_layout.addWidget(self.cantidad_paginas)
        main_layout.addWidget(self.descip)
        main_layout.addWidget(self.descripcion)
        
        button_layout.addWidget(self.boton_agregar)
        button_layout.addWidget(self.boton_volver)

        
        # Agregar botones
        main_layout.addLayout(button_layout)

        # Asignar el Layout
        self.setLayout(main_layout)

        # Conexiones de botones
        self.boton_buscar_usuario.clicked.connect(self.buscar_rut)
        self.boton_agregar.clicked.connect(self.agregar_impresiones)
        self.boton_volver.clicked.connect(self.volver_menu.emit)

    def crear_line_edit(self, placeholder, disabled, input_mask=""):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        if disabled:
            line_edit.setDisabled(True)
        if input_mask:
            line_edit.setInputMask(input_mask)
        return line_edit

    def crear_label(self, text):
        label = QLabel()
        label.setText(text)
        return label

    # Función para buscar un usuario por su rut
    def buscar_rut(self):
        rut = self.rut_solicitante.text()
        user = selected_user_by_rut(rut)
        if user:
            user = user[0][0]
            self.nombre_solicitante.setText(user.nombre)
            self.cursos.setText(user.curso)
            self.nombre_solicitante.setDisabled(True)
            self.cursos.setDisabled(True)
        else:
            self.nombre_solicitante.setDisabled(False)
            self.nombre_solicitante.clear()
            self.cursos.setDisabled(False)
            self.cursos.clear()

    # Función para agregar una impresión
    def agregar_impresiones(self):
        nombre = self.nombre_solicitante.text()
        curso = self.cursos.text()
        rut = self.rut_solicitante.text()
        copias = self.cantidad_copias.text()
        paginas = self.cantidad_paginas.text()
        descrip = self.descripcion.toPlainText()
        ingresar_impresiones(nombre, curso, rut, copias, paginas, descrip)

        # Limpiar campos después de agregar
        self.limpiar_campos()

    def limpiar_campos(self):
        self.rut_solicitante.clear()
        self.nombre_solicitante.clear()
        self.cursos.clear()
        self.cantidad_copias.clear()
        self.cantidad_paginas.clear()
        self.descripcion.clear()
        self.cambiar_curso.setChecked(False)

    # Función para habilitar o deshabilitar el campo de curso
    def check_event(self, event):
        if event == Qt.Checked:
            self.cursos.setDisabled(False)
        if event == Qt.Unchecked:
            self.cursos.setDisabled(True)
