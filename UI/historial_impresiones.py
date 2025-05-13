from PyQt5.QtWidgets import (QWidget, QPushButton, QTableWidget,
                             QTableWidgetItem, QLabel, QVBoxLayout,
                             QHeaderView, QMessageBox, QAbstractItemView,
                             QComboBox, QHBoxLayout, QSizePolicy)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor

from connection.session import (select_impresion_all, select_all_estado_impresion,
                                select_impresiones_filtradas, select_type_sheet)
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

        # Crear la tabla de impresiones
        self.tabla_impresiones = QTableWidget()
        self.tabla_impresiones.setColumnCount(9)
        self.tabla_impresiones.setMaximumHeight(400)
        headers = ["Nombre Alumno/Profesor", "Curso/Departamento", "Cantidad de Páginas",
                   "Cantidad de Copias", "Hojas Usadas en Total", "Fecha de Impresión",
                   "Descripción","Tipo de Hoja" ,"Estado de la Impresión"]
        for i, header in enumerate(headers):
            item = QTableWidgetItem(header)
            self.tabla_impresiones.setHorizontalHeaderItem(i, item)

        # Tamaño de las columnas
        header = self.tabla_impresiones.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_impresiones.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.tabla_impresiones.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_impresiones.setSelectionMode(QAbstractItemView.MultiSelection)


        # Crear botones
        self.cambiar_estado = QPushButton("Cambiar Estado")
        self.volver_atras = QPushButton("Volver al Menu de Impresiones")

        # Layout para los filtros
        filter_layout.addWidget(self.filtro_estado)
        filter_layout.addWidget(self.filtro_tipo_papel)
        filter_layout.addWidget(self.filtrar)
        filter_layout.addWidget(self.borrar_filtro)

        # Layout principal
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.tabla_impresiones)
        button_layout.addWidget(self.cambiar_estado)
        button_layout.addWidget(self.volver_atras)
        main_layout.addLayout(button_layout)

        # Establecer el layout principal
        self.setLayout(main_layout)

        # Conexiones de botones
        self.cambiar_estado.clicked.connect(self.actualizar_estado)
        self.volver_atras.clicked.connect(self.volver_menu.emit)
        self.filtrar.clicked.connect(self.filtrar_tabla)
        self.borrar_filtro.clicked.connect(self.rellenar_tabla)

        # Rellenar la tabla al inicio
        self.rellenar_tabla()

        # Rellenar ComboBox con los estados de impresión
        estados = select_all_estado_impresion()
        self.filtro_estado.addItem("Selecciona un estado")
        for es in estados:
            self.filtro_estado.insertItem(es[0].id_estadoimpresiones, es[0].estado_impresion)

        hoja = select_type_sheet()
        self.filtro_tipo_papel.addItem("Selecciona un tipo de papel")
        for h in hoja:
            self.filtro_tipo_papel.addItem(h[0])

    def rellenar_tabla(self):
        self.tabla_impresiones.setRowCount(0)
        impresiones = select_impresion_all()
        self.filtro_estado.setCurrentIndex(0)
        self.filtro_tipo_papel.setCurrentIndex(0)
        self.tabla(impresiones)

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
        self.tabla_impresiones.setRowCount(0)
        estado_seleccionado = self.filtro_estado.currentIndex()
        papel = self.filtro_tipo_papel.currentText()
        if estado_seleccionado != 0 or papel != "Selecciona un tipo de papel":
            datos_tabla = select_impresiones_filtradas(estado_seleccionado, papel)
            self.tabla(datos_tabla)
        else:
            self.rellenar_tabla()

    def tabla(self, impresiones):
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
