"""
    **Modulo prestamo_libros.py**\n
    Es el modulo encarga de la parte visual con la cual el usuario
    podra hacer el ingreso de las impresiones que deba realizar

    **Importaciones del modulo**\n
    PyQt5.QtWidgets ----> Usado principalmente para obtener los widgets que serán
                            usados durante la creacion del libro\n
    PyQt5.QtCore ----> Usado para obtener, ya sean las señales, o algunas
                        configuraciones adicionales para los widgets\n
    datetime ----> Usado para obtener la fecha y la fecha con las horas, minutos y segundos\n
    modulo connection ----> Usado para traer la funcion ingresar_impresiones, esto con el fin
                            de poder ingresar la impresion a la base de datos, tomando los datos
                            encontrados en los widgets\n
    modulo session -----> Usado para poder obtener todos los usuario que pidio esa impresion
                            y para obtener los libros del prestamo
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QDateEdit, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QCheckBox, QHeaderView, QAbstractItemView)

from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QColor

from datetime import datetime, date

from PyQt5.QtCore import pyqtSignal

from connection.session import (selected_user_by_rut, select_prestamo_libro)
from connection.connection import insert_prestamos

class PrestamoLibros(QWidget):
    """
    **Clase PrestamoLibros**\n
    Permite el poder agregar los prestamos a la base de datos, a traves de una interfaz parecida a un formulario.
    Este formulario cuenta con los siguientes campos:\n

    - Rut del prestatario\n
    - Nombre del prestatario\n
    - Curso del Prestatario\n
    - Fecha Maxima del pretamo\n
    - Datos del libro a traves de la tabla
    """
    volver_principal = pyqtSignal()
    actualizar_datos = pyqtSignal()
    def __init__(self, parent = None):
        """
        **Funcion __ init __**\n
        Es la encargada de cargar tanto los widgets como sus datos correspondientes
        los cuales se cargan apenas se detecta que el usuairo abrio el sistema\n
        """
        super().__init__(parent)

        #Variable global para curso
        self.curso_user = ""

        #Definicion de layouts principal
        vertical_layout_principal = QVBoxLayout()

        #Definicion de Layout
        vertical_layout_1 = QVBoxLayout()

        vertical_layout_2 = QVBoxLayout()
        horizontal_layot_principal = QHBoxLayout()
        horizontal_layot_1 = QHBoxLayout()
        horizontal_layot_2 = QHBoxLayout()
        horizontal_layot_3 = QHBoxLayout()

        #Definicion de los LineEdit
        self.rut_ = QLineEdit()
        self.rut_.setPlaceholderText("Ingrese el Rut del Alumno o Profesor")
        self.rut_.setInputMask("00.000.000-n;_")
        self.nombre_prestatario = QLineEdit()
        self.nombre_prestatario.setPlaceholderText("Ingrese el nombre del Alumno o Profesor")
        self.nombre_prestatario.setDisabled(True)
        self.curso_prestatario = QLineEdit()
        self.curso_prestatario.setPlaceholderText("Ingrese el curso del prestatario")
        self.curso_prestatario.setDisabled(True)

        #Creacion de los Checkbox
        self.cambiar_curso = QCheckBox("Habilitar para cambiar departamento o curso")
        self.cambiar_curso.stateChanged.connect(self.check_event)

        #Creacion de los labes
        self.fecha = QLabel("Fecha Maxima a Entregar *")
        self.rut = QLabel("Rut del Alumno/Profesor *")
        self.nombre = QLabel("Nombre del Alumno/Profesor *")
        self.curso = QLabel("Curso del Alumno/Profesor *")

        #Definicion de los botones
        self.boton_volver = QPushButton("Ir al Inventario de Libros")
        self.boton_buscar_rut = QPushButton("Buscar")
        self.boton_agregar_prestamo = QPushButton("Agregar Prestamo")

        #Definicion del LineEdit
        self.fecha_maxima = QDateEdit()
        self.fecha_maxima.setDisplayFormat("yyyy-MM-dd")
        self.fecha_maxima.setDateRange(date.today(), QDate.currentDate().addDays(7))
        self.fecha_maxima.setCalendarPopup(True)

        fecha = date.today()
        fecha.strftime("%Y-%m-%d")
        self.fecha_maxima.setDate(fecha)

        #Definicion de la tabla
        self.tabla_libro_prestamo = QTableWidget()

        #Definicion de columnas para tabla
        self.tabla_libro_prestamo.setColumnCount(6)
        item = QTableWidgetItem()
        item.setText("Nombre Libro")
        self.tabla_libro_prestamo.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Autor")
        self.tabla_libro_prestamo.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setText("Editorial")
        self.tabla_libro_prestamo.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setText("Fecha Entrada Biblioteca")
        self.tabla_libro_prestamo.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        item.setText("Estado del Libro")
        self.tabla_libro_prestamo.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        item.setText("Id Interno")
        self.tabla_libro_prestamo.setHorizontalHeaderItem(5, item)

        self.tabla_libro_prestamo.setColumnHidden(5, True)


        #Agregar los widgets a los layouts
        horizontal_layot_principal.addLayout(vertical_layout_1)
        vertical_layout_1.addLayout(horizontal_layot_1)
        vertical_layout_1.addWidget(self.tabla_libro_prestamo)
        vertical_layout_1.addWidget(self.fecha)
        vertical_layout_1.addWidget(self.fecha_maxima)
        horizontal_layot_principal.addLayout(vertical_layout_2)
        vertical_layout_2.addWidget(self.rut)
        vertical_layout_2.addLayout(horizontal_layot_2)
        horizontal_layot_2.addWidget(self.rut_)
        horizontal_layot_2.addWidget(self.boton_buscar_rut)
        vertical_layout_2.addWidget(self.nombre)
        vertical_layout_2.addWidget(self.nombre_prestatario)
        vertical_layout_2.addWidget(self.curso)
        horizontal_layot_3.addWidget(self.curso_prestatario)
        horizontal_layot_3.addWidget(self.cambiar_curso)
        vertical_layout_2.addLayout(horizontal_layot_3)
        vertical_layout_principal.addLayout(horizontal_layot_principal)
        vertical_layout_principal.addWidget(self.boton_agregar_prestamo)
        vertical_layout_principal.addWidget(self.boton_volver)

        vertical_layout_principal.addStretch()

        self.setLayout(vertical_layout_principal)
        header = self.tabla_libro_prestamo.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.tabla_libro_prestamo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_libro_prestamo.setSelectionMode(QAbstractItemView.MultiSelection)

        #Funcionamiento Boton
        self.boton_agregar_prestamo.clicked.connect(self.insertar_prestamos)
        self.boton_volver.clicked.connect(self.volver_principal.emit)
        self.boton_buscar_rut.clicked.connect(self.buscar_rut)

    def rellenar_tablas(self):
        """
        **Funcion rellenar_tablas**\n
        Se encarga de obtener todos los datos de los libros para luego cargarlos a la tabla

        **Excepcion**\n
        Se implementa traceback para errores fantasmas ademas de imprimir el error por consola
        """
        try:
            self.tabla_libro_prestamo.setRowCount(0)
            libros = select_prestamo_libro(self.nombre_libro, self.autor_libro, self.editorial_libro)

            column_count = self.tabla_libro_prestamo.columnCount()-2

            mal_estado = QColor("#ffd62e")  # Mal estado
            buen_estado = QColor("#b2f7b2")  # Buen estado
            dado_baja = QColor("#ff6b6b")  # Dado de baja
            estado_regular = QColor("#ffe066")  # Estado regular

            if libros:
                for li in libros:
                    row_position = self.tabla_libro_prestamo.rowCount()
                    self.tabla_libro_prestamo.insertRow(row_position)

                    self.tabla_libro_prestamo.setItem(row_position, 0, QTableWidgetItem(li.nombre_libro))
                    self.tabla_libro_prestamo.setItem(row_position, 1, QTableWidgetItem(li.autor))
                    self.tabla_libro_prestamo.setItem(row_position, 2, QTableWidgetItem(li.editorial))
                    self.tabla_libro_prestamo.setItem(row_position, 3, QTableWidgetItem(str(li.fecha_entrada)))
                    self.tabla_libro_prestamo.setItem(row_position, 4, QTableWidgetItem(li.estado_libro))
                    self.tabla_libro_prestamo.setItem(row_position, 5, QTableWidgetItem(str(li.id_copia)))

                    texto_tabla = self.tabla_libro_prestamo.item(row_position, column_count).text()

                    if texto_tabla == "Buen Estado":
                        self.tabla_libro_prestamo.item(row_position, column_count).setBackground(buen_estado)
                    elif texto_tabla == "Mal Estado":
                        self.tabla_libro_prestamo.item(row_position, column_count).setBackground(mal_estado)
                    elif texto_tabla == "Estado Regular":
                        self.tabla_libro_prestamo.item(row_position, column_count).setBackground(estado_regular)
                    elif texto_tabla == "Dado de Baja":
                        self.tabla_libro_prestamo.item(row_position, column_count).setBackground(dado_baja)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error {e}")
        # Función para buscar un usuario por su rut
    def buscar_rut(self):
        """
        **Funcion buscar_rut**\n
        Se utiliza para poder buscar el usuario a traves del rut, a traves de un tiempo de carga\n
        """
        rut = self.rut_.text()
        # Espera 500 ms antes de ejecutar la búsqueda
        QTimer.singleShot(500, lambda: self.buscar_usuario(rut))

    def buscar_usuario(self, rut):
        """
        **Funcion buscar_rut**\n
        Se utiliza para poder buscar y cargar los datos del usuario a traves del rut indicado por el usuario
        """
        user = selected_user_by_rut(rut)
        if user:
            user = user[0][0]
            self.nombre_prestatario.setText(user.nombre)
            self.curso_prestatario.setText(user.curso)
            self.curso_user = user.curso
            self.nombre_prestatario.setDisabled(True)
            self.curso_prestatario.setDisabled(True)
        else:
            self.nombre_prestatario.setDisabled(False)
            self.nombre_prestatario.clear()
            self.curso_prestatario.setDisabled(False)
            self.curso_prestatario.clear()
    
    def insertar_prestamos(self):
        """
        **Funcion insertar_prestamos**\n
        Permite el ingreso de los prestamos a la base de datos, con sus respectivos
        validadores en caso que algunos datos esten vacios o si el usuario no desea ingresar dicho prestamo
        """
        fecha = datetime.now()
        fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
        fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        selected_rows = self.tabla_libro_prestamo.selectionModel().selectedRows()
        fecha_ = self.fecha_maxima.dateTime().toPyDateTime().date()
        rut = self.rut_.text()
        if rut == "..-":
            rut = ""
        nombre = self.nombre_prestatario.text()
        curso = self.curso_prestatario.text()
        if not selected_rows:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion erronea")
            msg.setText("Debe seleccionar al menos un libro")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
            return
        if not nombre or not rut or not curso:
                msg = QMessageBox()
                msg.setWindowTitle("Usuario invalido")
                msg.setText("No se especificado un alumno o profesor")
                msg.setIcon(QMessageBox.Information)
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle("Confirmar Prestamo")
        msg.setText(f"¿Deseas guardar el prestamo de {len(selected_rows)} libro(s)?")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setIcon(QMessageBox.Question)
        msg.exec()
        if msg.standardButton(msg.clickedButton()) == QMessageBox.Save:
            for row in selected_rows:
                id_interno = int(self.tabla_libro_prestamo.item(row.row(), 5).text())
                if id_interno:
                    insert_prestamos(fecha,fecha_, rut, nombre, curso, id_interno)
            self.nombre_prestatario.clear()
            self.curso_prestatario.clear()
            self.rellenar_tablas()
            self.rut_.clear()
            msg_ok = QMessageBox()
            msg_ok.setWindowTitle("Accion ingresada correctamente")
            msg_ok.setText(f"El prestamo se ingreso correctamente")
            msg_ok.setIcon(QMessageBox.Information)
            msg_ok.exec()
        elif msg.standardButton(msg.clickedButton()) == QMessageBox.Cancel:
            cancelAction = QMessageBox()
            cancelAction.setText("Se cancelo la accion")
            cancelAction.setStandardButtons(QMessageBox.Ok)
            cancelAction.setIcon(QMessageBox.Information)
            cancelAction.setWindowTitle("Accion Cancelada")
            cancelAction.exec()
            return

    def traer_objeto(self, nombre, autor, editorial):
        """
        **Funcion traer_objeto**\n
        Se encarga de traer los datos de los libros a traves de la señal propuesta por historial_libro

        **Parametros**\n
        - nombre: str\n
        - autor: str\n
        - editorial: str\n

        **Retorna**\n
        nombre_libro: str\n
        autor_libro: str\n
        editorial_libro: str\n
        """
        if not nombre or not autor or not editorial:
            return
        self.nombre_libro = nombre
        self.autor_libro = autor
        self.editorial_libro = editorial
        self.rellenar_tablas()
        return self.nombre_libro, self.autor_libro, self.editorial_libro


    def check_event(self, event):
        """
        **Funcion check_event**\n
        Es la funcion que permite el poder cambiar el curso del alumno o profesor si es que el usuario asi lo permite
        """
        if event == Qt.Checked:
            self.curso_prestatario.setDisabled(False)
        if event == Qt.Unchecked:
            self.curso_prestatario.setDisabled(True)
            self.curso_prestatario.setText(self.curso_user)