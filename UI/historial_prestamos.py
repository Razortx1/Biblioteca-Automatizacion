from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView,
                             QPushButton, QLabel, QAbstractItemView,
                             QMessageBox)
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtGui import QColor

from connection.session import select_prestamos_all
from .actualizar_ui.actualizar_prestamos import ActualizarPrestamos

class HistorialPrestamos(QWidget):
    volver_principal = pyqtSignal()
    pasar_fecha = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        self.w = None

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
        self.tabla_historial.setColumnCount(8)

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
        item.setText("Cantidad Libros Prestada")
        self.tabla_historial.setHorizontalHeaderItem(6, item)

        item = QTableWidgetItem()
        item.setText("Estado Prestamo")
        self.tabla_historial.setHorizontalHeaderItem(7, item)

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

        self.tabla_historial.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_historial.setSelectionMode(QAbstractItemView.SingleSelection)

        #Funcionamiento Botones
        self.cambiar_estado.clicked.connect(self.cambiar_state)
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
                self.tabla_historial.setItem(tablerow, 6, QTableWidgetItem(str(p.stock)))
                self.tabla_historial.setItem(tablerow, 7, QTableWidgetItem(p.estado_prestamo))

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


    def cambiar_state(self):
        selected_rows = self.tabla_historial.selectionModel().selectedRows()
        if not selected_rows:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion erronea")
            msg.setText("No se ha seleccionado un prestamo")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
        else:
            for row in selected_rows:
                fecha_item = self.tabla_historial.item(row.row(), 4).text()
            if self.w is None:
                self.w = ActualizarPrestamos()
                self.w.actualizar_datos.connect(self.rellenar_tabla)
                self.pasar_fecha.connect(self.w.traer_fecha)
                self.pasar_fecha.emit(fecha_item)
                self.w.show()
                self.w.cerrar_ventana.connect(self.cerrar_ventana)
    
    def cerrar_ventana(self):
        if self.w is not None:
            self.w = None