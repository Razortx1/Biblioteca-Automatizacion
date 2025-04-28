from PyQt5.QtWidgets import (QWidget, QPushButton, QTableWidget,
                             QTableWidgetItem, QLabel, QVBoxLayout,
                             QHeaderView)
from PyQt5.QtCore import pyqtSignal
from connection.session import select_impresion_all
from PyQt5.QtGui import QColor

class HistorialImpresiones(QWidget):
    volver_menu = pyqtSignal()
    def __init__(self):
        super().__init__()

                #Definicion del layout
        void_layout_1 = QVBoxLayout()
        void_layout_2 = QVBoxLayout()
        vertical_layout = QVBoxLayout()

        self.voidLabel_1 = QLabel()
        self.voidLabel_2 = QLabel()
        void_layout_1.addWidget(self.voidLabel_1)
        void_layout_2.addWidget(self.voidLabel_2)

        #Creacion de la tabla
        self.tabla_impresiones = QTableWidget()
        self.tabla_impresiones.setColumnCount(8)

        item = QTableWidgetItem()
        item.setText("Nombre Alumno/Profesor")
        self.tabla_impresiones.setHorizontalHeaderItem(0, item)

        item = QTableWidgetItem()
        item.setText("Curso/Departamento")
        self.tabla_impresiones.setHorizontalHeaderItem(1, item)

        item = QTableWidgetItem()
        item.setText("Cantidad de Paginas")
        self.tabla_impresiones.setHorizontalHeaderItem(2, item)

        item = QTableWidgetItem()
        item.setText("Cantidad de Copias")
        self.tabla_impresiones.setHorizontalHeaderItem(3, item)

        item = QTableWidgetItem()
        item.setText("Fecha de Impresion")
        self.tabla_impresiones.setHorizontalHeaderItem(4, item)

        item = QTableWidgetItem()
        item.setText("Hojas usadas en total")
        self.tabla_impresiones.setHorizontalHeaderItem(5, item)

        item = QTableWidgetItem()
        item.setText("Descripción")
        self.tabla_impresiones.setHorizontalHeaderItem(6, item)

        item = QTableWidgetItem()
        item.setText("Estado Impresion")
        self.tabla_impresiones.setHorizontalHeaderItem(7, item)

        #Tamaño Columnas
        header = self.tabla_impresiones.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_impresiones.setRowCount(50)

        #Creacion botones
        self.volver_atras = QPushButton("Volver Atras")

        #Agregar los Widgets al layout
        vertical_layout.addWidget(self.tabla_impresiones)
        vertical_layout.addWidget(self.volver_atras)
        vertical_layout.addLayout(void_layout_1)
        vertical_layout.addLayout(void_layout_2)

        #Asignar el layout
        self.setLayout(vertical_layout)

        #Funcionamiento Botones
        self.volver_atras.clicked.connect(self.volver_menu.emit)

        #Relleno de tabla
        self.rellenar_tabla()

    def rellenar_tabla(self):
        impresiones = select_impresion_all()
        tablerow = 0

        column_count = self.tabla_impresiones.columnCount()

        no_impreso = QColor(255, 90, 90)
        ya_impreso = QColor(90,255,90)


        for i in impresiones:

            suma = int(i.Impresiones.cantidad_copias * i.Impresiones.cantidad_paginas)

            self.tabla_impresiones.setItem(tablerow, 0, QTableWidgetItem(i.Usuario.nombre))
            self.tabla_impresiones.setItem(tablerow, 1, QTableWidgetItem(i.Usuario.curso))
            self.tabla_impresiones.setItem(tablerow, 2, QTableWidgetItem(i.Impresiones.cantidad_paginas))
            self.tabla_impresiones.setItem(tablerow, 3, QTableWidgetItem(i.Impresiones.cantidad_copias))
            self.tabla_impresiones.setItem(tablerow, 4, QTableWidgetItem(str(suma)))
            self.tabla_impresiones.setItem(tablerow, 5, QTableWidgetItem(str(i.Impresiones.fecha_impresion)))
            self.tabla_impresiones.setItem(tablerow, 6, QTableWidgetItem(i.Impresiones.descripcion))
            self.tabla_impresiones.setItem(tablerow, 7, QTableWidgetItem(i.Estado_Impresion.estado_impresion))

            texto_tabla = self.tabla_impresiones.item(tablerow, column_count-1).text()

            if texto_tabla == "Aun no Impreso":
                self.tabla_impresiones.item(tablerow, column_count-1).setBackground(no_impreso)
            elif texto_tabla == "Ya Impreso":
                self.tabla_impresiones.item(tablerow, column_count-1).setBackground(ya_impreso)

            tablerow+=1

