from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView,
                             QPushButton, QLabel)
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtGui import QColor

from connection.session import select_prestamos_all

class HistorialPrestamos(QWidget):
    volver_principal = pyqtSignal()
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
        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(7)

        item = QTableWidgetItem()
        item.setText("Nombre Alumno/Profesor")
        self.tabla_historial.setHorizontalHeaderItem(0, item)

        item = QTableWidgetItem()
        item.setText("Curso/Departamento")
        self.tabla_historial.setHorizontalHeaderItem(1, item)

        item = QTableWidgetItem()
        item.setText("Rut")
        self.tabla_historial.setHorizontalHeaderItem(2, item)

        item = QTableWidgetItem()
        item.setText("Nombre Libro")
        self.tabla_historial.setHorizontalHeaderItem(3, item)

        item = QTableWidgetItem()
        item.setText("Fecha de pedido")
        self.tabla_historial.setHorizontalHeaderItem(4, item)

        item = QTableWidgetItem()
        item.setText("Fecha Devolucion")
        self.tabla_historial.setHorizontalHeaderItem(5, item)

        item = QTableWidgetItem()
        item.setText("Estado Prestamo")
        self.tabla_historial.setHorizontalHeaderItem(6, item)

        #Tamaño Columnas
        header = self.tabla_historial.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_historial.setRowCount(0)

        #Creacion botones
        self.cambiar_estado = QPushButton("Cambiar Estado")
        self.volver_atras = QPushButton("Volver Atras")

        #Agregar los Widgets al layout
        vertical_layout.addWidget(self.tabla_historial)
        vertical_layout.addWidget(self.cambiar_estado)
        vertical_layout.addWidget(self.volver_atras)
        vertical_layout.addLayout(void_layout_1)
        vertical_layout.addLayout(void_layout_2)

        #Asignar el layout
        self.setLayout(vertical_layout)

        #Funcionamiento Botones
        self.volver_atras.clicked.connect(self.volver_principal.emit)

        self.rellenar_tabla()

    #Funcion para rellenar la tabla
    def rellenar_tabla(self):
        prestamos = select_prestamos_all()
        tablerow = 0
        self.tabla_historial.setRowCount(50)

        column_count = self.tabla_historial.columnCount()

        extraviado = QColor(255, 90, 90)
        devuelto = QColor(90,255,90)
        prestado = QColor(255,215,0)
        if prestamos:
            for p in prestamos:
                self.tabla_historial.setItem(tablerow, 0, QTableWidgetItem(p.nombre))
                self.tabla_historial.setItem(tablerow, 1, QTableWidgetItem(p.curso))
                self.tabla_historial.setItem(tablerow, 2, QTableWidgetItem(p.rut))
                self.tabla_historial.setItem(tablerow, 3, QTableWidgetItem(p.nombre_libro))
                self.tabla_historial.setItem(tablerow, 4, QTableWidgetItem(str(p.fecha_inicio)))
                self.tabla_historial.setItem(tablerow, 5, QTableWidgetItem(str(p.fecha_termino)))
                self.tabla_historial.setItem(tablerow, 6, QTableWidgetItem(p.estado_prestamo))

                texto_tabla = self.tabla_historial.item(tablerow, column_count-1).text()

                if texto_tabla == "Prestado":
                    self.tabla_historial.item(tablerow, column_count-1).setBackground(prestado)
                elif texto_tabla == "Devuelto":
                    self.tabla_historial.item(tablerow, column_count-1).setBackground(devuelto)
                elif texto_tabla == "Extraviado":
                    self.tabla_historial.item(tablerow, column_count-1).setBackground(extraviado)

                tablerow+=1
        else:
            pass

