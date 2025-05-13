from PyQt5.QtWidgets import (QWidget, QPushButton, QTableWidgetItem, QTableWidget,
                             QAbstractItemView, QVBoxLayout, QHeaderView, QHBoxLayout,
                             QMessageBox, QComboBox, QLineEdit)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor

from connection.session import (select_libros_available, select_estado_libro_all)
from .actualizar_ui.actualizar_libros import ActualizarLibros

class HistorialLibros(QWidget):
    volver_principal = pyqtSignal()
    ir_prestamo_libro = pyqtSignal(str, str, str, str)
    pasar_datos = pyqtSignal(str, str, str, str)

    def __init__(self, parent = None):
        super().__init__(parent)

        self.w = None
        # Layout principal
        main_layout = QVBoxLayout()

        # Layout para filtrado
        filtro_layout = QHBoxLayout()

        # PushButtons para filtrado de tabla
        self.filtrar = QPushButton("Aplicar Filtro(s)")
        self.quitar_filtro = QPushButton("Quitar Filtro(s)")

        # Combobox para filtrado de tabla
        self.estado_filtro = QComboBox()

        # LineEdit para filtrado de tabla
        self.nombre_filtro = QLineEdit()
        self.nombre_filtro.setPlaceholderText("Nombre del libro")

        self.sector_biblioteca = QLineEdit()
        self.sector_biblioteca.setPlaceholderText("Sector Biblioteca")

        self.sector_estanteria = QLineEdit()
        self.sector_estanteria.setPlaceholderText("Sector Estanteria")

        self.editorial = QLineEdit()
        self.editorial.setPlaceholderText("Editoral")

        self.autor_libro = QLineEdit()
        self.autor_libro.setPlaceholderText("Autor")

        # Crear la tabla de libros
        self.tabla_libros = QTableWidget()
        self.tabla_libros.setColumnCount(8)
        headers = ["Nombre Libro", "Autor", "Editorial", "Fecha Entrada a Biblioteca","Area de Biblioteca", 
                   "Sector Estanteria" , "Stock de Libros", "Estado del Libro"]
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
        self.volver_inicio = QPushButton("Volver al Menu Principal")
        self.agregar_prestamo = QPushButton("Agregar prestamo del libro")

        # Agregar los widgets al layout principal
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addWidget(self.cambiar_estado)
        button_layout.addWidget(self.volver_inicio)

        filtro_layout.addWidget(self.nombre_filtro)
        filtro_layout.addWidget(self.autor_libro)
        filtro_layout.addWidget(self.editorial)
        filtro_layout.addWidget(self.sector_biblioteca)
        filtro_layout.addWidget(self.sector_estanteria)
        filtro_layout.addWidget(self.estado_filtro)
        filtro_layout.addWidget(self.filtrar)
        filtro_layout.addWidget(self.quitar_filtro)

        main_layout.addLayout(filtro_layout)
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
        self.filtrar.clicked.connect(self.aplicar_filtros)
        self.quitar_filtro.clicked.connect(self.vaciar_filtrado)

        # Rellenado del combobox
        self.estado_filtro.addItem("Selecciona un estado")
        estado = select_estado_libro_all()
        for es in estado:
            self.estado_filtro.addItem(es[0].estado_libro)

    def rellenar_tabla(self):
        self.tabla_libros.setRowCount(0)
        libros = select_libros_available()
        self.tabla(libros)

    def vaciar_filtrado(self):
        self.estado_filtro.setCurrentIndex(0)
        self.sector_biblioteca.clear()
        self.sector_estanteria.clear()
        self.editorial.clear()
        self.nombre_filtro.clear()
        self.autor_libro.clear()
        self.rellenar_tabla()

    def aplicar_filtros(self):
        self.tabla_libros.setRowCount(0)
        biblioteca = self.sector_biblioteca.text()
        estanteria = self.sector_estanteria.text()
        no_editorial = self.editorial.text()
        autor = self.autor_libro.text()
        nombre = self.nombre_filtro.text()
        estado = self.estado_filtro.currentText()
        if estado == "Selecciona un estado":
            estado = None
        else:
            self.rellenar_tabla()
            return
        libros = select_libros_available(nombre=nombre,autor= autor,Editorial=no_editorial, Estado_=estado,
                                         SectorBiblio=biblioteca, SectorEstanteria=estanteria)
        self.tabla(libros)
        
    def prestamo_ir(self):
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
        self.ir_prestamo_libro.emit(nombre, autor, editorial, fecha)

    def tabla(self, libros):
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

    def actualizar_estado(self):
        selected_row = self.tabla_libros.selectionModel().selectedRows()
        if not selected_row:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion Invalida")
            msg.setText("Por favor, selecciona un libro antes de continuar")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
            return
        
        for row in selected_row:
            nombre = self.tabla_libros.item(row.row(), 0).text()
            autor = self.tabla_libros.item(row.row(), 1).text()
            editorial = self.tabla_libros.item(row.row(), 2).text()
            fecha = self.tabla_libros.item(row.row(), 3).text()
        if self.w is None:
            self.w = ActualizarLibros()
            self.w.actualizar_datos.connect(self.rellenar_tabla)
            self.pasar_datos.connect(self.w.traer_datos)
            self.pasar_datos.emit(nombre, autor, editorial, fecha)
            self.w.show()
            self.w.cerrar_ventana.connect(self.cerrar_ventana)

    def cerrar_ventana(self):
        if self.w is not None:
            self.w = None
