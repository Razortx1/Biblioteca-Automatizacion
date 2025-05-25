"""
    **Modulo agregar_impresiones.py**\n
    Es el modulo que se encarga de la parte visual con la cual el usuario
    podra hacer el ingreso de las impresiones que deba realizar\n

    **Importaciones del modulo**\n
    PyQt5.QtWidgets ----> Usado principalmente para obtener los widgets que serán
                            usados durante la creacion del libro\n
    PyQt5.QtCore ----> Usado para obtener, ya sean las señales, o algunas
                        configuraciones adicionales para los widgets\n

    modulo connection ----> Usado para traer la funcion ingresar_impresiones, esto con el fin
                            de poder ingresar la impresion a la base de datos, tomando los datos
                            encontrados en los widgets\n
    modulo session -----> Usado para poder obtener todos el usuario que pidio esa impresion

"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QHBoxLayout,
                             QTextEdit, QCheckBox, QMessageBox,
                             QComboBox)

from PyQt5.QtCore import (pyqtSignal, Qt, QTimer)

from connection.session import selected_user_by_rut
from connection.connection import ingresar_impresiones


class AgregarImpresiones(QWidget):
    """
    **Clase AgregarImpresiones**\n
    Permite el poder agregar las impresiones a la base de datos, a traves de una interfaz
    parecida a un formulario. Este formulario cuenta con los siguientes campos: \n

    - Nombre del solicitante de la impresion\n
    - Rut del solicitante de la impresion\n
    - Curso del solicitante de la impresion\n
    - Cantidad de copias a necesitar\n
    - Cantidad de paginas a necesitar\n
    - La descripcion de la impresion
    """
    volver_menu = pyqtSignal()

    def __init__(self):
        """
        **Funcion __ init __**\n
        Es la encargada de cargar los widgets apenas se detecta que el 
        usuario abrio el sistema
        """
        super().__init__()

        #Variable global para curso
        self.curso_user = ""

        # Definición de Layouts
        main_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        horizontal_layout_column = QHBoxLayout()
        column1 = QVBoxLayout()
        column2 = QVBoxLayout()
        button_layout = QHBoxLayout()
        curso_layout = QHBoxLayout()

        # Ajustar márgenes y espaciado para tener menos espacio entre los widgets
        main_layout.setContentsMargins(10, 10, 10, 10)  # Márgenes del layout principal
        main_layout.setSpacing(5)  # Espaciado entre los widgets

        horizontal_layout.setContentsMargins(5, 5, 5, 5)  # Márgenes de horizontal_layout
        horizontal_layout.setSpacing(5)  # Espaciado dentro de horizontal_layout

        self.setFixedHeight(600)

        # Creación de los Widgets
        self.nombre_solicitante = self.crear_line_edit("Ingrese el nombre del Alumno/Profesor", True)
        self.rut_solicitante = self.crear_line_edit("Ingrese el rut Alumno/Profesor", False, "00.000.000-n;_")
        self.rut_solicitante.setFocus()
        self.cursos = self.crear_line_edit("Ingrese Curso o Departamento", True)

        self.cambiar_curso = QCheckBox("Habilitar para cambiar departamento o curso")
        self.cambiar_curso.stateChanged.connect(self.check_event)

        self.cantidad_copias = self.crear_line_edit("Ingrese la cantidad de Copias", False)
        self.cantidad_paginas = self.crear_line_edit("Ingrese la cantidad de Paginas del documento", False)

        self.descripcion = QTextEdit()
        self.descripcion.setPlaceholderText("Ingrese la descripcion de la impresion")
        self.descripcion.setMaximumHeight(100)  # Limitar altura de la caja de texto

        self.combo_hoja = QComboBox()

        # Botones
        self.boton_agregar = QPushButton("Agregar Impresion")
        self.boton_volver = QPushButton("Volver al Menú de Impresiones")
        self.boton_buscar_usuario = QPushButton("Buscar")

        # Organizar en Layouts
        horizontal_layout.addWidget(self.rut_solicitante)
        horizontal_layout.addWidget(self.boton_buscar_usuario)

        self.nombre = self.crear_label("Nombre Alumno/Profesor *")
        self.rut = self.crear_label("Rut del alumno/profesor *")
        self.cantidad_c = self.crear_label("Cantidad de Copias a necesitar *")
        self.cantidad_p = self.crear_label("Cantidad de paginas que tiene el documento en total *")
        self.curso = self.crear_label("Curso/Departamento *")
        self.descip = self.crear_label("Descripcion de la Impresion *")
        self.hojas = self.crear_label("Tipo de Hoja *")

        # Configurar el Layout principal
        main_layout.addWidget(self.rut)
        main_layout.addLayout(horizontal_layout)

        column1.addWidget(self.nombre)
        column1.addWidget(self.nombre_solicitante)
        column1.addWidget(self.curso)
        curso_layout.addWidget(self.cursos)
        curso_layout.addWidget(self.cambiar_curso)
        column1.addLayout(curso_layout)
        column1.addWidget(self.cantidad_c)
        column1.addWidget(self.cantidad_copias)
        horizontal_layout_column.addLayout(column1)

        column2.addWidget(self.cantidad_p)
        column2.addWidget(self.cantidad_paginas)
        column2.addWidget(self.hojas)
        column2.addWidget(self.combo_hoja)
        horizontal_layout_column.addLayout(column2)


        main_layout.addLayout(horizontal_layout_column)
        main_layout.addWidget(self.descip)
        main_layout.addWidget(self.descripcion)
        
        button_layout.addWidget(self.boton_agregar)
        button_layout.addWidget(self.boton_volver)

        self.combo_hoja.addItem("Selecciona el tipo de hoja a usar")
        self.combo_hoja.addItem("Carta")
        self.combo_hoja.addItem("Oficio")
        
        # Agregar botones
        main_layout.setSpacing(15)
        main_layout.addLayout(button_layout)

        # Asignar el Layout
        self.setLayout(main_layout)

        # Conexiones de botones
        self.boton_buscar_usuario.clicked.connect(self.buscar_rut)
        self.boton_agregar.clicked.connect(self.agregar_impresiones)
        self.boton_volver.clicked.connect(self.volver_menu.emit)

    def crear_line_edit(self, placeholder, disabled, input_mask=""):
        """
        **Funcion crear_line_edit**\n
        Se encarga de crear los distintos lineedit\n

        **Parametros**\n
        - placeholder: str\n
        - disabled: str\n
        - input_mask: str | ""\n

        **Retorna**\n
        line_edit: Objeto Widget QLineEdit
        """
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        if disabled:
            line_edit.setDisabled(True)
        if input_mask:
            line_edit.setInputMask(input_mask)
        return line_edit

    def crear_label(self, text):
        """
        **Funcion crear_label**\n
        Se encarga de crear los distintos label\n

        **Parametros**\n
        - text: str\n

        **Retorna**\n
        label: Objeto Widget QLabel
        """
        label = QLabel()
        label.setText(text)
        return label

    # Función para buscar un usuario por su rut
    def buscar_rut(self):
        """
        **Funcion buscar_rut**\n
        Se utiliza para poder buscar el usuario a traves del rut, a traves de un tiempo de carga\n
        """
        rut = self.rut_solicitante.text()
        # Espera 500 ms antes de ejecutar la búsqueda
        QTimer.singleShot(500, lambda: self.buscar_usuario(rut))

    def buscar_usuario(self, rut):
        """
        **Funcion buscar_usuario**\n
        Se utiliza para poder obtener el usuario a traves del rut\n

        **Parametros**\n
        rut: str
        """
        user = selected_user_by_rut(rut)
        if user:
            user = user[0][0]
            self.nombre_solicitante.setText(user.nombre)
            self.cursos.setText(user.curso)
            self.curso_user = user.curso
            self.nombre_solicitante.setDisabled(True)
            self.cursos.setDisabled(True)
        else:
            self.nombre_solicitante.setDisabled(False)
            self.nombre_solicitante.clear()
            self.cursos.setDisabled(False)
            self.cursos.clear()

    # Función para agregar una impresión
    def agregar_impresiones(self):
        """
        **Funcion agregar_impresiones**\n
        Se encarga de tomar todos los datos escritos por el usuario para
        empezar el proceso de creacion de las impresiones
        """
        copias = self.cantidad_copias.text()
        paginas = self.cantidad_paginas.text()
        nombre = self.nombre_solicitante.text()
        curso = self.cursos.text()
        rut = self.rut_solicitante.text()
        descrip = self.descripcion.toPlainText()
        hoja = ""
        if self.combo_hoja.currentText() != "Selecciona el tipo de hoja a usar":
            hoja = self.combo_hoja.currentText()
        elif self.combo_hoja.currentText() == "Selecciona el tipo de hoja a usar":
            hoja = ""
        if not nombre or not curso or not descrip or not copias or not paginas or not hoja:
            msg = QMessageBox()
            msg.setWindowTitle("Error de Entrada")
            msg.setText("Por Favor, ingrese los datos necesarios para la impresion, estos estan marcados por un *")
            msg.setIcon(QMessageBox.Warning)
            msg.exec()
            return
        if not copias.isdigit() or not paginas.isdigit():
            msg = QMessageBox()
            msg.setWindowTitle("Error de Entrada")
            msg.setText("Por favor, ingrese números válidos en los campos de cantidad de copias y páginas.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec()
            return
        ingresar_impresiones(nombre, curso, rut, copias, paginas, descrip, hoja)

        # Limpiar campos después de agregar
        self.limpiar_campos()

    def limpiar_campos(self):
        """
        **Funcion limpiar_campos**\n
        Se encarga de devolver todos los valores a los predefinidos, esto para poder
        ingresar otra impresion en caso de ser necesario una vez ingresada la impresion
        """
        self.rut_solicitante.clear()
        self.nombre_solicitante.clear()
        self.cursos.clear()
        self.cantidad_copias.clear()
        self.cantidad_paginas.clear()
        self.descripcion.clear()
        self.cambiar_curso.setChecked(False)
        self.curso_user = ""

    # Función para habilitar o deshabilitar el campo de curso
    def check_event(self, event):
        """
        **Funcion check_event**\n
        Se utiliza para poder cambiar el curso del alumno o profesor si es que el usuario 
        lo permita\n

        **Parametros**\n
        - event: Bool
        """
        if event == Qt.Checked:
            self.cursos.setDisabled(False)
        if event == Qt.Unchecked:
            self.cursos.setDisabled(True)
            self.cursos.setText(self.curso_user)
