"""
    **Modulo historia_impresiones**\n
    Es el modulo que se encarga de la parte visual con la cual el usuario
    podra revisar el historial de las impresiones que haya dentro del sistema\n

    **Importaciones del modulo**\n
    PyQt5.QtWidgets ----> Usado principalmente para obtener los widgets que serán
                            usados durante observacion del historial de las impresiones\n
    PyQt5.QtCore ----> Usado para obtener, ya sean las señales, o algunas
                        configuraciones adicionales para los widgets\n
    PyQt.QtGui -----> Usado para cambiar los colores de la ultima columna de la tabla

    modulo session -----> Usado para poder obtener todas las impresiones que hayan en la
                        base de datos, ademas de sus estados, el tipo de hoja usada o los
                        cursos pertenecientes a la tabla Usuarios
    modulo connection ----> Usado principalmente para poder actualizar el estado de las
                            impresiones

"""

from PyQt5.QtWidgets import (QWidget, QPushButton, QTableWidget,
                             QTableWidgetItem, QLabel, QVBoxLayout,
                             QHeaderView, QMessageBox, QAbstractItemView,
                             QComboBox, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor

from connection.session import (select_impresion_all, select_all_estado_impresion,
                                select_type_sheet,
                                select_cursos_user, count_pages_printed_in_month)
from connection.connection import update_estado_impresion


class HistorialImpresiones(QWidget):
    """
    **Clase HistorialImpresiones**\n
    Permite el poder observar las distintas impresiones presentes en la base de datos, esto
    a traves de filtros y paginaciones
    """
    volver_menu = pyqtSignal()

    def __init__(self):
        """
        **Funcion __ init __**\n
        Permite la carga de todos y cada uno de los widgets que se utilizaran durante el ciclo
        de vida de esta ventana
        """
        super().__init__()

        # Definición de Layout
        main_layout = QVBoxLayout()
        filter_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        other_layout = QVBoxLayout()

        # Widgets para Filtros
        self.filtrar = QPushButton("Aplicar Filtro(s)")
        self.borrar_filtro = QPushButton("Quitar Filtro(s)")
        self.filtro_estado = QComboBox()
        self.filtro_tipo_papel = QComboBox()
        self.filtro_curso = QComboBox()

        self.filtros_actuales ={
            "estado_seleccionado": "",
            "papel": "",
            "curso": ""
        }

        # PushButton Paginaciones
        self.anterior = QPushButton("Pagina Anterior")
        self.siguiente = QPushButton("Pagina Siguiente")
        self.anterior.setDisabled(True)

        # Label para cantidad de paginas
        self.cantidad_paginas = QLabel()

        # Label para paginaciones
        self.pagina = QLabel("Pagina 1")
        self.pagina.setAlignment(Qt.AlignCenter)

        # Crear la tabla de impresiones
        self.tabla_impresiones = QTableWidget()
        self.tabla_impresiones.setColumnCount(9)
        self.tabla_impresiones.setMinimumHeight(339)
        self.tabla_impresiones.setMaximumHeight(339)
        headers = ["Nombre Alumno/Profesor", "Curso/Departamento", "Cantidad de Páginas",
                   "Cantidad de Copias", "Hojas Usadas en Total", "Fecha de Impresión",
                   "Descripción","Tipo de Hoja" ,"Estado de la Impresión"]
        for i, header in enumerate(headers):
            item = QTableWidgetItem(header)
            self.tabla_impresiones.setHorizontalHeaderItem(i, item)

        
        self.tabla_impresiones.setWordWrap(True)

        # Tamaño de las columnas
        header = self.tabla_impresiones.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.tabla_impresiones.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_impresiones.setSelectionMode(QAbstractItemView.MultiSelection)


        # Crear botones
        self.cambiar_estado = QPushButton("Cambiar Estado")
        self.volver_atras = QPushButton("Volver al Menu de Impresiones")

        paginacion_layout = QHBoxLayout()

        # Layout para los filtros
        filter_layout.addWidget(self.filtro_curso)
        filter_layout.addWidget(self.filtro_tipo_papel)
        filter_layout.addWidget(self.filtro_estado)
        filter_layout.addWidget(self.filtrar)
        filter_layout.addWidget(self.borrar_filtro)

        other_layout.addWidget(self.cantidad_paginas)
        paginacion_layout.addWidget(self.anterior)
        paginacion_layout.addWidget(self.pagina)
        paginacion_layout.addWidget(self.siguiente)
        other_layout.addLayout(paginacion_layout)

        # Layout principal
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.tabla_impresiones)
        button_layout.addWidget(self.cambiar_estado)
        button_layout.addWidget(self.volver_atras)
        main_layout.addLayout(other_layout)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(5)

        self.page_size = 7
        self.current_page = 0

        # Establecer el layout principal
        self.setLayout(main_layout)

        # Conexiones de botones
        self.cambiar_estado.clicked.connect(self.actualizar_estado)
        self.volver_atras.clicked.connect(self.volver_menu.emit)
        self.filtrar.clicked.connect(self.filtrar_tabla)
        self.borrar_filtro.clicked.connect(self.vaciar_filtrado)

        self.anterior.clicked.connect(self.anterior_funcion)
        self.siguiente.clicked.connect(self.siguiente_funcion)

    def actualizar_paginas(self):
        self.cantidad_total = 0
        contador = count_pages_printed_in_month()
        for total in contador:
            self.cantidad_total = (total[0] * total[1]) + self.cantidad_total
        self.cantidad_paginas.setText(f"Cantidad de Paginas Impresas este mes: {self.cantidad_total}")

    def anterior_funcion(self):
        """
        **Funcion anterior_funcion**\n
        Permite poder manejar las paginaciones con los respectivos botones,
        ademas del label utilizado para mostrar la pagina actual
        Se usa normalmente para disminuir la cantidad de paginas
        """
        if self.current_page > 0:
            self.current_page -=1
            self.pagina.setText(f"Pagina {self.current_page +1}")
            self.rellenar_tabla(**self.filtros_actuales)

    def siguiente_funcion(self):
        """
        **Funcion siguiente_funcion**\n
        Permite poder manejar las paginaciones con los respectivos botones,
        ademas del label utilizado para mostrar la pagina actual.\n
        Se usa normalmente para incrementar la cantidad de paginas
        """
        self.current_page+=1
        self.pagina.setText(f"Pagina {self.current_page +1}")
        self.anterior.setDisabled(False)
        self.rellenar_tabla(**self.filtros_actuales)

    def vaciar_filtrado(self):
        """
        **Funcion vaciar_filtrado**\n
        Es la encargada de devolver todos los valores de los filtros a vacio, o en caso de ser un combobox,
        se regresa a su indice 0, el cual esta establecido como 'Selecciona...'
        """
        self.filtro_estado.setCurrentIndex(0)
        self.filtro_tipo_papel.setCurrentIndex(0)
        self.filtro_curso.setCurrentIndex(0)
        self.filtros_actuales = {
            "estado_seleccionado": "",
            "papel": "",
            "curso": "" 
        }
        self.current_page = 0
        self.rellenar_tabla(**self.filtros_actuales)
        self.pagina.setText("Pagina 1")

    # Rellenar ComboBox con los estados de impresión
    def rellenar_combobox(self):
        """
        **Funcion rellenar_combobox**\n
        Permite el poder rellenar los combobox que se encuentran como filtros
        """
        self.filtro_estado.clear()
        self.filtro_tipo_papel.clear()
        self.filtro_curso.clear()
        estados = select_all_estado_impresion()
        self.filtro_estado.addItem("Selecciona un estado")
        for es in estados:
            self.filtro_estado.insertItem(es[0].id_estadoimpresiones, es[0].estado_impresion)

        hoja = select_type_sheet()
        self.filtro_tipo_papel.addItem("Selecciona un tipo de papel")
        for ho in hoja:
            self.filtro_tipo_papel.addItem(ho[0])

        curso = select_cursos_user()
        self.filtro_curso.addItem("Selecciona un curso")
        for cur in curso:
            self.filtro_curso.addItem(cur[0])

    def rellenar_tabla(self, estado_seleccionado=None, papel=None, curso=None):
        """
        **Funcion rellenar_tabla**\n
        Es la encargada de traer todas las impresiones que actualmente hay en biblioteca ademas de
        permitir la opcion de filtrado en los datos

        **Parametros**\n
        - estado_seleccionado: int | None\n
        - papel: str | None\n
        - curso: str | None
        """
        self.actualizar_paginas()
        offset = self.current_page * self.page_size
        impresiones = list(select_impresion_all(estado=estado_seleccionado, 
                                                   papel=papel,
                                                   departamento=curso,
                                                   limit=self.page_size+1, offset=offset))
        if len(impresiones) > self.page_size:
            self.siguiente.setDisabled(False)
            impresiones = impresiones[:self.page_size]
        else:
            self.siguiente.setDisabled(True)
        if self.current_page == 0:
            self.anterior.setDisabled(True)
        else:
            self.anterior.setDisabled(False)
        self.tabla(impresiones)

    def actualizar_estado(self):
        """
        **Funcion actualizar_estado**\n
        Permite poder actualizar los estados de las impresiones las cuales hayan sido seleccionadas en la tabla
        """
        selected_row = self.tabla_impresiones.selectionModel().selectedRows()
        if not selected_row:
            msg = QMessageBox()
            msg.setWindowTitle("Error de selección")
            msg.setText("Se debe seleccionar por lo menos una impresión")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
        else:
            for row in selected_row:
                item = self.tabla_impresiones.item(row.row(), 5).text()
                estado = self.tabla_impresiones.item(row.row(), 8).text()
                if estado == "Aun no Impreso":
                    estado = 2
                elif estado == "Ya Impreso":
                    estado = 1
                if item:
                    update_estado_impresion(item, estado)
            msg = QMessageBox()
            msg.setWindowTitle("Estado Actualizado")
            msg.setText("El estado de la impresión ha sido actualizado correctamente.")
            msg.setIcon(QMessageBox.Information)
            msg.exec()

            self.rellenar_tabla()

    def filtrar_tabla(self):
        """
        **Funcion filtrar_tabla**\n
        Permite poder hacer uso de filtros a los datos mostrados en la tabla
        """
        estado_seleccionado = self.filtro_estado.currentIndex()
        papel = self.filtro_tipo_papel.currentText()
        curso = self.filtro_curso.currentText()
        self.current_page = 0
        self.pagina.setText("Pagina 1")
        if estado_seleccionado == 0:
            estado_seleccionado = ""
        if papel == "Selecciona un tipo de papel":
            papel = ""
        if curso == "Selecciona un curso":
            curso = ""
        self.filtros_actuales ={
            "estado_seleccionado": estado_seleccionado,
            "papel": papel,
            "curso": curso
        }
        self.rellenar_tabla(**self.filtros_actuales)

    def tabla(self, impresiones):
        """
        **Funcion tabla**\n
        Permite poder rellenar la tabla

        **Parametros**\n
        - impresiones: List[Impresion]
        """
        self.tabla_impresiones.setRowCount(0)
        column_count = self.tabla_impresiones.columnCount()
        tablerow = 0
        no_impreso = QColor("#ff6b6b")
        ya_impreso = QColor("#b2f7b2")

        if impresiones:
            for i in impresiones:
                row_position = self.tabla_impresiones.rowCount()
                self.tabla_impresiones.insertRow(row_position)
                suma = int(i.Impresiones.cantidad_copias * i.Impresiones.cantidad_paginas)

                self.tabla_impresiones.setItem(tablerow, 0, QTableWidgetItem(i.Usuario.nombre))
                self.tabla_impresiones.setItem(tablerow, 1, QTableWidgetItem(i.Usuario.curso))
                self.tabla_impresiones.setItem(tablerow, 2, QTableWidgetItem(str(i.Impresiones.cantidad_paginas)))
                self.tabla_impresiones.setItem(tablerow, 3, QTableWidgetItem(str(i.Impresiones.cantidad_copias)))
                self.tabla_impresiones.setItem(tablerow, 4, QTableWidgetItem(str(suma)))
                self.tabla_impresiones.setItem(tablerow, 5, QTableWidgetItem(str(i.Impresiones.fecha_impresion)))
                self.tabla_impresiones.setItem(tablerow, 6, QTableWidgetItem(i.Impresiones.descripcion))
                self.tabla_impresiones.setItem(tablerow, 7, QTableWidgetItem(i.Impresiones.tipo_papel))
                self.tabla_impresiones.setItem(tablerow, 8, QTableWidgetItem(i.Estado_Impresion.estado_impresion))

                texto_tabla = self.tabla_impresiones.item(tablerow, column_count-1).text()

                # Colorear las celdas según el estado
                if texto_tabla == "Aun no Impreso":
                    self.tabla_impresiones.item(tablerow, column_count-1).setBackground(no_impreso)
                elif texto_tabla == "Ya Impreso":
                    self.tabla_impresiones.item(tablerow, column_count-1).setBackground(ya_impreso)

                tablerow += 1
        else:
            pass
        
        self.tabla_impresiones.resizeRowsToContents()
