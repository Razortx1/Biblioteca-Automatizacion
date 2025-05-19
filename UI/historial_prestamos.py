from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView,
                             QPushButton, QComboBox, QAbstractItemView,
                             QMessageBox, QHBoxLayout,
                             QLineEdit, QLabel)
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from connection.session import (select_prestamos_all, select_all_estado_prestamos, 
                                select_cursos_user)
from .actualizar_ui.actualizar_prestamos import ActualizarPrestamos

class HistorialPrestamos(QWidget):
    volver_principal = pyqtSignal()
    pasar_fecha = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        self.w = None

        # Definicion del layout
        vertical_layout = QVBoxLayout()

        filtro_layout = QHBoxLayout()

        paginacion_layout = QHBoxLayout()

        # Definicion de combobox para filtrado
        self.estado_prestamo = QComboBox()
        self.combo_curso = QComboBox()

        # Definicion de lineedit para filtrado
        self.rut_prestatario = QLineEdit()
        self.rut_prestatario.setInputMask("00.000.000-n;_")

        self.nombre_libro = QLineEdit()
        self.nombre_libro.setPlaceholderText("Nombre Libro")

        self.nombre_user = QLineEdit()
        self.nombre_user.setPlaceholderText("Nombre Alumno/Profesor")

        # Definicion botones para filtrado
        self.filtrar = QPushButton("Aplicar Filtro")
        self.quitar_filtro = QPushButton("Quitar Filtro")

        # Label para paginaciones
        self.pagina = QLabel("Pagina 1")
        self.pagina.setAlignment(Qt.AlignCenter)

        # Creacion de la tabla
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

        # Tamaño Columnas
        header = self.tabla_historial.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_historial.setMinimumHeight(300)
        self.tabla_historial.setMaximumHeight(300)

        self.page_size = 7
        self.current_page = 0

        # Creacion botones
        self.cambiar_estado = QPushButton("Cambiar Estado")
        self.volver_atras = QPushButton("Volver al Menu Principal")

        # Definicion PushButton para Paginaciones
        self.anterior = QPushButton("Pagina Anterior")
        self.anterior.setDisabled(True)
        self.siguiente = QPushButton("Pagina Siguiente")

        # Agregar los Widgets al layout
        filtro_layout.addWidget(self.nombre_user)
        filtro_layout.addWidget(self.combo_curso)
        filtro_layout.addWidget(self.rut_prestatario)
        filtro_layout.addWidget(self.nombre_libro)
        filtro_layout.addWidget(self.estado_prestamo)
        filtro_layout.addWidget(self.filtrar)
        filtro_layout.addWidget(self.quitar_filtro)

        vertical_layout.addLayout(filtro_layout)
        vertical_layout.addWidget(self.tabla_historial)

        paginacion_layout.addWidget(self.anterior)
        paginacion_layout.addWidget(self.pagina)
        paginacion_layout.addWidget(self.siguiente)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cambiar_estado)
        button_layout.addWidget(self.volver_atras)

        vertical_layout.addLayout(paginacion_layout)
        vertical_layout.addLayout(button_layout)

        # Asignar el layout
        self.setLayout(vertical_layout)

        self.tabla_historial.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_historial.setSelectionMode(QAbstractItemView.SingleSelection)

        # Funcionamiento Botones
        self.cambiar_estado.clicked.connect(self.cambiar_state)
        self.volver_atras.clicked.connect(self.volver_principal.emit)
        self.quitar_filtro.clicked.connect(self.quitar_filtros)
        self.filtrar.clicked.connect(self.filtrado_datos)

        self.anterior.clicked.connect(self.anterior_funcion)
        self.siguiente.clicked.connect(self.siguiente_funcion)

    def rellenar_combobox(self):
        self.estado_prestamo.clear()
        self.combo_curso.clear()
        self.estado_prestamo.addItem("Selecciona un estado")
        estado = select_all_estado_prestamos()
        for es in estado:
            self.estado_prestamo.insertItem(es[0].id_estadoprestamo, es[0].estado_prestamo)
        
        self.combo_curso.addItem("Selecciona un curso")
        curso = select_cursos_user()
        for cur in curso:
            self.combo_curso.addItem(cur[0])

    def anterior_funcion(self):
        if self.current_page > 0:
            self.current_page -=1
            self.pagina.setText(f"Pagina {self.current_page +1}")
            self.filtrado_datos()

    def siguiente_funcion(self):
        self.current_page+=1
        self.pagina.setText(f"Pagina {self.current_page +1}")
        self.anterior.setDisabled(False)
        self.filtrado_datos()

    # Funcion para rellenar la tabla
    def rellenar_tabla(self, estado=None, rut_prest=None,
                       libro_nombre=None, user_nombre=None,curso=None):
        offset = self.current_page * self.page_size
        prestamos = list(select_prestamos_all(estado= estado, rut= rut_prest, 
                                            nombre_libro= libro_nombre,
                                            nombre_user= user_nombre,
                                            curso= curso, offset= offset, 
                                            limit= self.page_size+1))
        self.siguiente.setDisabled(False)
        self.anterior.setDisabled(False)
        if len(prestamos) > self.page_size:
            self.siguiente.setDisabled(False)
            self.anterior.setDisabled(True)
            prestamos = prestamos[:self.page_size]
        else:
            self.siguiente.setDisabled(True)
        self.tabla(prestamos)

    def tabla(self, prestamos):
        self.tabla_historial.setRowCount(0)
        tablerow = 0
        columna = 0
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
                columna+=1
        else:
            pass

    def filtrado_datos(self):
        #self.current_page = 0
        #self.pagina.setText(f"Pagina {self.current_page+1}")
        estado = ""
        rut_prest = ""
        libro_nombre = self.nombre_libro.text()
        user_nombre = self.nombre_user.text()
        curso = ""

        if self.estado_prestamo.currentText() != "Selecciona un estado":
            estado = self.estado_prestamo.currentIndex()
        elif estado == "Selecciona un estado":
            estado = ""
        if self.rut_prestatario.text() != "..-":
            rut_prest = self.rut_prestatario.text()
        if self.combo_curso.currentText() != "Selecciona un curso":
            curso = self.combo_curso.currentText()
        elif curso == "Selecciona un estado":
            curso = ""
        self.rellenar_tabla(estado=estado, rut_prest=rut_prest, 
                                        libro_nombre=libro_nombre,
                                        user_nombre=user_nombre,
                                        curso=curso)

    def quitar_filtros(self):
        self.estado_prestamo.setCurrentIndex(0)
        self.combo_curso.setCurrentIndex(0)
        self.rut_prestatario.clear()
        self.nombre_libro.clear()
        self.nombre_user.clear()
        self.rellenar_tabla()


    def cambiar_state(self):
        selected_rows = self.tabla_historial.selectionModel().selectedRows()
        if not selected_rows:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion Invalida")
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