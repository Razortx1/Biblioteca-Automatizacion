from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView,
                             QPushButton, QLabel)
from PyQt5.QtCore import (pyqtSignal)

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
        self.tabla_historial.setColumnCount(6)
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
        item.setText("Fecha de pedido")
        self.tabla_historial.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        item.setText("Fecha Devolucion")
        self.tabla_historial.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        item.setText("Estado Prestamo")
        self.tabla_historial.setHorizontalHeaderItem(5, item)

        #Tamaño Columnas
        header = self.tabla_historial.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        #Creacion botones
        self.volver_atras = QPushButton("Volver Atras")

        #Agregar los Widgets al layout
        vertical_layout.addWidget(self.tabla_historial)
        vertical_layout.addWidget(self.volver_atras)
        vertical_layout.addLayout(void_layout_1)
        vertical_layout.addLayout(void_layout_2)

        #Asignar el layout
        self.setLayout(vertical_layout)

        #Funcionamiento Botones
        self.volver_atras.clicked.connect(self.volver_principal.emit)
