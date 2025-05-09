from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView,
                             QPushButton, QLabel, QAbstractItemView,
                             QMessageBox, QHBoxLayout, QSizePolicy)
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
        vertical_layout = QVBoxLayout()

        self.voidLabel_1 = QLabel()
        self.voidLabel_2 = QLabel()

        vertical_layout.setContentsMargins(15, 15, 15, 15)
        vertical_layout.setSpacing(5)

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
        button_layout = QHBoxLayout()
        self.cambiar_estado.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.volver_atras.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button_layout.addWidget(self.cambiar_estado)
        button_layout.addWidget(self.volver_atras)
        vertical_layout.addLayout(button_layout)

        #Asignar el layout
        self.setLayout(vertical_layout)

        self.tabla_historial.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_historial.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla_historial.setMinimumHeight(300)
        self.tabla_historial.setMaximumHeight(500)

        #Funcionamiento Botones
        self.cambiar_estado.clicked.connect(self.cambiar_state)
        self.volver_atras.clicked.connect(self.volver_principal.emit)

        self.rellenar_tabla()

    #Funcion para rellenar la tabla
    def rellenar_tabla(self):
        self.tabla_historial.setRowCount(0)
        prestamos = select_prestamos_all()
        tablerow = 0
        column_count = self.tabla_historial.columnCount()

        extraviado = QColor("#ff6b6b")  # rojo suave
        devuelto = QColor("#b2f7b2")    # verde claro
        prestado = QColor("#ffe066")    # amarillo pastel
        if prestamos:
            for p in prestamos:
                row_position = self.tabla_historial.rowCount()
                self.tabla_historial.insertRow(row_position)
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
            msg.setWindowTitle("Seleccion invalida")
            msg.setText("Por favor, selecciona un préstamo para continuar.")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
            return
        
        fecha_item = self.tabla_historial.item(selected_rows[0].row(), 4).text()
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