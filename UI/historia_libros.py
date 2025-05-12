from PyQt5.QtWidgets import (QWidget, QPushButton, QTableWidgetItem, QTableWidget,
                             QAbstractItemView, QVBoxLayout, QHeaderView, QHBoxLayout,
                             QMessageBox)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor

from connection.session import select_libros_available
from .actualizar_ui.actualizar_libros import ActualizarLibros

class HistorialLibros(QWidget):
    volver_principal = pyqtSignal()
    ir_prestamo_libro = pyqtSignal(str, str, str, str)

    def __init__(self):
        super().__init__()

        self.w = None
        # Layout principal
        main_layout = QVBoxLayout()

        # Crear la tabla de libros
        self.tabla_libros = QTableWidget()
        self.tabla_libros.setColumnCount(8)
        headers = ["Nombre Libro", "Autor", "Editorial", "Fecha Entrada a Biblioteca","Area de Biblioteca", "Sector Estanteria" , "Stock de Libros", "Estado del Libro"]
        self.tabla_libros.setMinimumHeight(300)
        self.tabla_libros.setMaximumHeight(700)
        
        # Asignar encabezados de las columnas
        for i, header in enumerate(headers):
            item = QTableWidgetItem(header)
            self.tabla_libros.setHorizontalHeaderItem(i, item)

        # Hacer que las columnas se ajusten al tamaño de la ventana
        header = self.tabla_libros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Crear los botones
        self.cambiar_estado = QPushButton("Cambiar Estado Libro")
        self.volver_inicio = QPushButton("Volver a Inicio")
        self.agregar_prestamo = QPushButton("Agregar prestamo del libro")

        # Agregar los widgets al layout principal
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addWidget(self.cambiar_estado)
        button_layout.addWidget(self.volver_inicio)
        main_layout.addWidget(self.tabla_libros)
        main_layout.addWidget(self.agregar_prestamo)
        main_layout.addLayout(button_layout)

        self.tabla_libros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_libros.setSelectionMode(QAbstractItemView.SingleSelection)

        # Agregar espaciadores si es necesario (opcional)
        main_layout.addStretch(1)

        # Establecer el layout principal
        self.setLayout(main_layout)

        # Inicializar la tabla
        self.tabla_libros.setRowCount(0)
        self.rellenar_tabla()

        # Conectar los botones con las funciones
        self.cambiar_estado.clicked.connect(self.actualizar_estado)
        self.volver_inicio.clicked.connect(self.volver_principal.emit)
        self.agregar_prestamo.clicked.connect(self.prestamo_ir)

    def rellenar_tabla(self):
        self.tabla_libros.setRowCount(0)
        libros = select_libros_available()
        mal_estado = QColor("#ffd62e")  # Mal estado
        buen_estado = QColor("#b2f7b2")  # Buen estado
        dado_baja = QColor("#ff6b6b")  # Dado de baja
        estado_regular = QColor("#ffe066")  # Estado regular

        if libros:
            for l in libros:
                row_position = self.tabla_libros.rowCount()
                self.tabla_libros.insertRow(row_position)

                # Insertar los datos del libro
                self.tabla_libros.setItem(row_position, 0, QTableWidgetItem(l.nombre_libro))
                self.tabla_libros.setItem(row_position, 1, QTableWidgetItem(l.autor))
                self.tabla_libros.setItem(row_position, 2, QTableWidgetItem(l.editorial))
                self.tabla_libros.setItem(row_position, 3, QTableWidgetItem(str(l.fecha_entrada)))
                self.tabla_libros.setItem(row_position, 4, QTableWidgetItem(l.sector_biblioteca))
                self.tabla_libros.setItem(row_position, 5, QTableWidgetItem(l.sector_estanteria))
                self.tabla_libros.setItem(row_position, 6, QTableWidgetItem(str(l.stock)))
                self.tabla_libros.setItem(row_position, 7, QTableWidgetItem(l.estado_libro))

                # Asignar colores dependiendo del estado
                estado_libro = self.tabla_libros.item(row_position, 7).text()

                if estado_libro == "Buen Estado":
                    self.tabla_libros.item(row_position, 7).setBackground(buen_estado)
                elif estado_libro == "Mal Estado":
                    self.tabla_libros.item(row_position, 7).setBackground(mal_estado)
                elif estado_libro == "Estado Regular":
                    self.tabla_libros.item(row_position, 7).setBackground(estado_regular)
                elif estado_libro == "Dado de Baja":
                    self.tabla_libros.item(row_position, 7).setBackground(dado_baja)
        else:
            return
        
    def prestamo_ir(self):
        from UI.prestamo_libros import PrestamoLibros
        selected_rows = self.tabla_libros.selectionModel().selectedRows()
        if not selected_rows:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion Invalida")
            msg.setText("Por favor, selecciona un libro antes de continuar")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
            return
        for row in selected_rows:
            nombre = self.tabla_libros.item(row.row(), 0).text()
            autor = self.tabla_libros.item(row.row(), 1).text()
            editorial = self.tabla_libros.item(row.row(), 2).text()
            fecha = self.tabla_libros.item(row.row(), 3).text()
        self.prestamos = PrestamoLibros()
        self.ir_prestamo_libro.connect(self.prestamos.traer_objeto)
        self.ir_prestamo_libro.emit(nombre, autor, editorial, fecha)

    def actualizar_estado(self):
        if self.w is None:
            self.w = ActualizarLibros()
            self.w.actualizar_datos.connect(self.rellenar_tabla)
            self.w.show()
            self.w.cerrar_ventana.connect(self.cerrar_ventana)

    def cerrar_ventana(self):
        if self.w is not None:
            self.w = None
