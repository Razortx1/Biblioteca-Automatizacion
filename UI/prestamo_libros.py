from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QDateEdit, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QCheckBox, QHeaderView)

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor

from datetime import datetime, date

from PyQt5.QtCore import pyqtSignal

from connection.session import (selected_user_by_rut)
from connection.connection import insert_prestamos

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
        self.fecha = QLabel("Fecha Maxima a Entregar")
        self.rut = QLabel("Rut del Alumno/Profesor")
        self.nombre = QLabel("Nombre del Alumno/Profesor")
        self.curso = QLabel("Curso del Alumno/Profesor")

        #Definicion de los botones
        self.boton_volver = QPushButton("Volver")
        self.boton_buscar_rut = QPushButton("Buscar")
        self.boton_agregar_prestamo = QPushButton("Agregar Prestamo")

        #Definicion del LineEdit
        self.fecha_maxima = QDateEdit()
        self.fecha_maxima.setDisplayFormat("yyyy-MM-dd")
        self.fecha_maxima.setDateRange(date.today(), QDate.currentDate().addDays(3))
        self.fecha_maxima.setCalendarPopup(True)

        fecha = date.today()
        fecha.strftime("%Y-%m-%d")
        self.fecha_maxima.setDate(fecha)

        #Definicion de la tabla
        self.tabla_libros = QTableWidget()

        #Definicion de columnas para tabla
        self.tabla_libros.setColumnCount(6)
        item = QTableWidgetItem()
        item.setText("Nombre Libro")
        self.tabla_libros.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Autor")
        self.tabla_libros.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setText("Editorial")
        self.tabla_libros.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setText("Fecha Entrada Biblioteca")
        self.tabla_libros.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        item.setText("Estado del Libro")
        self.tabla_libros.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        item.setText("Id Interno")
        self.tabla_libros.setHorizontalHeaderItem(5, item)

        #Agregar los widgets a los layouts
        horizontal_layot_principal.addLayout(vertical_layout_1)
        vertical_layout_1.addLayout(horizontal_layot_1)
        vertical_layout_1.addWidget(self.tabla_libros)
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
        header = self.tabla_libros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        #Funcionamiento Boton
        self.boton_agregar_prestamo.clicked.connect(self.insertar_prestamos)
        self.boton_volver.clicked.connect(self.volver_principal.emit)
        self.boton_buscar_rut.clicked.connect(self.buscar_rut)

    def rellenar_tabla(self):
        try:
            self.tabla_libros.setRowCount(0)

            tablerow = 0

            column_count = self.tabla_libros.columnCount()-2

            mal_estado = QColor(255, 205, 0)
            buen_estado = QColor(90,255,90)
            dado_baja = QColor(255,50,50)
            estado_regular = QColor(255,255,0)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error {e}")

    def buscar_rut(self):
        rut = self.rut_.text()
        user = selected_user_by_rut(rut)
        if user:
            user = user[0][0]
            self.nombre_prestatario.setText(user.nombre)
            self.curso_prestatario.setText(user.curso)
            self.nombre_prestatario.setDisabled(True)
            self.curso_prestatario.setDisabled(True)
        else:
            self.nombre_prestatario.setDisabled(False)
            self.nombre_prestatario.clear()
            self.curso_prestatario.setDisabled(False)
            self.curso_prestatario.clear()
    
    def insertar_prestamos(self):
        fecha = datetime.now()
        fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
        fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        selected_rows = self.tabla_libros.selectionModel().selectedRows()
        fecha_ = self.fecha_maxima.dateTime().toPyDateTime().date()
        rut = self.rut_.text()
        nombre = self.nombre_prestatario.text()
        curso = self.curso_prestatario.text()
        if not selected_rows:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion erronea")
            msg.setText("No se ha seleccionado un libro")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
        msg = QMessageBox()
        msg.setWindowTitle("Confirmar Prestamo")
        msg.setText(f"¿Deseas guardar el prestamo de {len(selected_rows)} libro(s)?")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setIcon(QMessageBox.Question)
        msg.exec()
        if msg.standardButton(msg.clickedButton()) == QMessageBox.Save:
            for row in selected_rows:
                id_interno = int(self.tabla_libros.item(row.row(), 5).text())
                if id_interno:
                    insert_prestamos(fecha,fecha_, rut, nombre, curso, id_interno)
            self.nombre_prestatario.clear()
            self.curso_prestatario.clear()
            self.cod_barras.clear()
            self.tabla_libros.setRowCount(0)
            self.rut_.clear()
        elif msg.standardButton(msg.clickedButton()) == QMessageBox.Cancel:
            cancelAction = QMessageBox()
            cancelAction.setText("Se cancelo la accion")
            cancelAction.setStandardButtons(QMessageBox.Ok)
            cancelAction.setIcon(QMessageBox.Information)
            cancelAction.setWindowTitle("Accion Cancelada")
            cancelAction.exec()

    def traer_objeto(self, nombre, autor, editorial, fecha):
        if not nombre or not autor or not editorial or not fecha:
            return
        self.nombre_libro = nombre
        self.autor_libro = autor
        self.editorial_libro = editorial
        self.fecha_libro = fecha
        self.rellenar_tabla()
        return self.nombre_libro, self.autor_libro, self.editorial_libro, self.fecha_libro


    def check_event(self, event):
        if event == Qt.Checked:
            self.curso_prestatario.setDisabled(False)
        if event == Qt.Unchecked:
            self.curso_prestatario.setDisabled(True)