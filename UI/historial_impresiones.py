from PyQt5.QtWidgets import (QWidget, QPushButton, QTableWidget,
                             QTableWidgetItem, QLabel, QVBoxLayout,
                             QHeaderView, QMessageBox, QAbstractItemView,
                             QComboBox, QHBoxLayout, QSizePolicy)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor

from connection.session import (select_impresion_all, select_all_estado_impresion,
                                select_type_sheet,
                                select_cursos_user)
from connection.connection import update_estado_impresion


class HistorialImpresiones(QWidget):
    volver_menu = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Definición de Layout
        main_layout = QVBoxLayout()
        filter_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Widgets para Filtros
        self.filtrar = QPushButton("Aplicar Filtro(s)")
        self.borrar_filtro = QPushButton("Quitar Filtro(s)")
        self.filtro_estado = QComboBox()
        self.filtro_tipo_papel = QComboBox()
        self.filtro_curso = QComboBox()

        # PushButton Paginaciones
        self.anterior = QPushButton("Pagina Anterior")
        self.siguiente = QPushButton("Pagina Siguiente")
        self.anterior.setDisabled(True)

        # Label para paginaciones
        self.pagina = QLabel("Pagina 1")
        self.pagina.setAlignment(Qt.AlignCenter)

        # Crear la tabla de impresiones
        self.tabla_impresiones = QTableWidget()
        self.tabla_impresiones.setColumnCount(9)
        self.tabla_impresiones.setMinimumHeight(300)
        self.tabla_impresiones.setMaximumHeight(300)
        headers = ["Nombre Alumno/Profesor", "Curso/Departamento", "Cantidad de Páginas",
                   "Cantidad de Copias", "Hojas Usadas en Total", "Fecha de Impresión",
                   "Descripción","Tipo de Hoja" ,"Estado de la Impresión"]
        for i, header in enumerate(headers):
            item = QTableWidgetItem(header)
            self.tabla_impresiones.setHorizontalHeaderItem(i, item)

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

        paginacion_layout.addWidget(self.anterior)
        paginacion_layout.addWidget(self.pagina)
        paginacion_layout.addWidget(self.siguiente)

        # Layout principal
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.tabla_impresiones)
        button_layout.addWidget(self.cambiar_estado)
        button_layout.addWidget(self.volver_atras)
        main_layout.addLayout(paginacion_layout)
        main_layout.addLayout(button_layout)

        self.page_size = 7
        self.current_page = 0
        self.number = 0

        # Establecer el layout principal
        self.setLayout(main_layout)

        # Conexiones de botones
        self.cambiar_estado.clicked.connect(self.actualizar_estado)
        self.volver_atras.clicked.connect(self.volver_menu.emit)
        self.filtrar.clicked.connect(self.filtrar_tabla)
        self.borrar_filtro.clicked.connect(self.vaciar_filtrado)

        self.anterior.clicked.connect(self.anterior_funcion)
        self.siguiente.clicked.connect(self.siguiente_funcion)


    def anterior_funcion(self):
        if self.current_page > 0:
            self.current_page -=1
            self.pagina.setText(f"Pagina {self.current_page +1}")
            self.rellenar_tabla()

    def siguiente_funcion(self):
        self.current_page+=1
        self.pagina.setText(f"Pagina {self.current_page +1}")
        self.anterior.setDisabled(False)
        self.rellenar_tabla()

    def vaciar_filtrado(self):
        self.filtro_estado.setCurrentIndex(0)
        self.filtro_tipo_papel.setCurrentIndex(0)
        self.filtro_curso.setCurrentIndex(0)
        self.rellenar_tabla()

    # Rellenar ComboBox con los estados de impresión
    def rellenar_combobox(self):
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

    def rellenar_tabla(self):
        offset = self.current_page * self.page_size
        impresiones = select_impresion_all(limit=self.page_size, offset=offset)
        self.siguiente.setDisabled(False)
        self.anterior.setDisabled(False)
        if self.current_page == 0:
            self.siguiente.setDisabled(False)
            self.anterior.setDisabled(True)
        self.tabla(impresiones)
        if self.tabla_impresiones.rowCount() > self.number:
            self.siguiente.setDisabled(False)
        if self.tabla_impresiones.rowCount() < self.page_size:
            self.siguiente.setDisabled(True)

    def actualizar_estado(self):
        selected_row = self.tabla_impresiones.selectionModel().selectedRows()
        if not selected_row:
            msg = QMessageBox()
            msg.setWindowTitle("Error de selección")
            msg.setText("No se ha seleccionado una fila")
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
        self.siguiente.setDisabled(True)
        self.anterior.setDisabled(True)
        estado_seleccionado = self.filtro_estado.currentIndex()
        papel = self.filtro_tipo_papel.currentText()
        curso = self.filtro_curso.currentText()
        if estado_seleccionado == 0:
            estado_seleccionado = ""
        if papel == "Selecciona un tipo de papel":
            papel = ""
        if curso == "Selecciona un curso":
            curso = ""
        datos_tabla = select_impresion_all(estado=estado_seleccionado, 
                                                   papel=papel,
                                                   departamento=curso,
                                                   limit=self.page_size)
        self.tabla(impresiones=datos_tabla)

    def tabla(self, impresiones):
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
