from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QPushButton, QTableWidget, QLineEdit, QLabel,
                             QComboBox, QHBoxLayout, QMessageBox, QTableWidgetItem,
                             QAbstractItemView)

from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal

from connection.session import (select_estado_libro_all, selected_libro_by_cod,
                                select_copia_libros_by_id)
from connection.connection import update_estado_libro

style_sheet = "QWidget{background-color: #B4E7FF;}" "QPushButton{\
        background-color: #C7FF9C;\
        border-radius:5px;\
        border: 1px solid black;\
        }\
        \
        QPushButton:pressed{\
            background-color: greenyellow;\
            color: white\
        }" "QLineEdit{\
        background-color: white;\
        border-radius: 10;\
        border: 1px solid black;\
    }" "QTableWidget{\
        background-color: rgb(255, 241, 184);\
    }"

class ActualizarLibros(QWidget):
    actualizar_datos = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Biblioteca | ACTUALIZACION ESTADO DE LIBROS")
        self.setStyleSheet(style_sheet)
        self.setGeometry(200,200,700,700)

        #Layout
        horizontal_layout_1 = QHBoxLayout()
        vertical_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        #Creacion de los QLineEdits
        self.buscar_codbarras = QLineEdit()
        self.buscar_codbarras.setStyleSheet(style_sheet)

        #Creacion de Boton
        self.buscar_libros = QPushButton("Buscar")
        self.buscar_libros.setStyleSheet(style_sheet)
        self.cambiar_estado = QPushButton("Cambiar estado")
        self.cambiar_estado.setStyleSheet(style_sheet)

        #Creacion de combobox
        self.estado = QComboBox()
        self.estado.setStyleSheet("background-color: #FFFFFF;")

        #creacion de labels
        self.cod = QLabel("Ingresa codigo de barras")

        #Creacion de la tabla
        self.tabla_cambiarlibros = QTableWidget()
        self.setStyleSheet(style_sheet)
        self.tabla_cambiarlibros.setColumnCount(6)
        item = QTableWidgetItem()
        item.setText("Nombre Libro")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Codigo de Barras")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setText("Autor")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setText("Fecha Publicacion")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        item.setText("Estado del Libro")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        item.setText("Id Interno")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(5, item)

        #Asignar tablas
        self.tabla_cambiarlibros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_cambiarlibros.setSelectionMode(QAbstractItemView.MultiSelection)

        #Asignar los widgets/layout a los principales layout
        horizontal_layout_1.addWidget(self.buscar_codbarras)
        horizontal_layout_1.addWidget(self.buscar_libros)

        horizontal_layout.addWidget(self.cambiar_estado)
        horizontal_layout.addWidget(self.estado)

        vertical_layout.addWidget(self.cod)
        vertical_layout.addLayout(horizontal_layout_1)
        vertical_layout.addWidget(self.tabla_cambiarlibros)
        vertical_layout.addLayout(horizontal_layout)
        

        self.setLayout(vertical_layout)

        #Establecer funciones del boton
        self.buscar_libros.clicked.connect(self.rellenar_tabla)
        self.cambiar_estado.clicked.connect(self.seleccion_datos)

        #Rellenar Combobox
        estado_libro = select_estado_libro_all()
        for es in estado_libro:
            self.estado.insertItem(es[0].id_estadolibro, es[0].estado_libro)

    def verificar_codi(self, codigo):
        msg = QMessageBox()
        msg.setWindowTitle("Libro no encontrado")
        msg.setText("No se ha encontrado el libro espeficicado")
        msg.setIcon(QMessageBox.Information)
        libros = selected_libro_by_cod(codigo)
        if libros:
            return libros
        else:
            msg.exec()
            return None
        
    def seleccion_datos(self):
        from UI.historia_libros import HistorialLibros
        selected_rows = self.tabla_cambiarlibros.selectionModel().selectedRows()
        if not selected_rows:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion erronea")
            msg.setText("No se ha seleccionado un libro")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
            
        estado_id = self.estado.currentIndex() + 1

        for row in selected_rows:
            id_item = self.tabla_cambiarlibros.item(row.row(), 5)
            if id_item:
                copia_id = int(id_item.text())
                update_estado_libro(copia_id, estado_id)

        self.actualizar_datos.emit()
        self.destroy(True)

    def rellenar_tabla(self):
        try:
            self.tabla_cambiarlibros.setRowCount(0)
            codigo = self.buscar_codbarras.text()
            libro = self.verificar_codi(codigo)
            id = libro[0][0].id_libro
            copias = select_copia_libros_by_id(id)

            tablerow = 0
            self.tabla_cambiarlibros.setRowCount(50)

            column_count = self.tabla_cambiarlibros.columnCount()-2

            mal_estado = QColor(255, 205, 0)
            buen_estado = QColor(90,255,90)
            dado_baja = QColor(255,50,50)
            estado_regular = QColor(255,255,0)
            if copias:
                for l in copias:
                    self.tabla_cambiarlibros.setItem(tablerow, 0, QTableWidgetItem(l.nombre_libro))
                    self.tabla_cambiarlibros.setItem(tablerow, 1, QTableWidgetItem(l.cod_barras))
                    self.tabla_cambiarlibros.setItem(tablerow, 2, QTableWidgetItem(l.autor))
                    self.tabla_cambiarlibros.setItem(tablerow, 3, QTableWidgetItem(str(l.fecha_publicacion)))
                    self.tabla_cambiarlibros.setItem(tablerow, 4, QTableWidgetItem(l.estado_libro))
                    self.tabla_cambiarlibros.setItem(tablerow, 5, QTableWidgetItem(str(l.id_copia)))

                    texto_tabla = self.tabla_cambiarlibros.item(tablerow, column_count).text()

                    if texto_tabla == "Buen Estado":
                        self.tabla_cambiarlibros.item(tablerow, column_count).setBackground(buen_estado)
                    elif texto_tabla == "Mal Estado":
                        self.tabla_cambiarlibros.item(tablerow, column_count).setBackground(mal_estado)
                    elif texto_tabla == "Estado Regular":
                        self.tabla_cambiarlibros.item(tablerow, column_count).setBackground(estado_regular)
                    elif texto_tabla == "Dado de Baja":
                        self.tabla_cambiarlibros.item(tablerow, column_count).setBackground(dado_baja)

                    tablerow+=1

            else:
                pass
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error {e}")
        
