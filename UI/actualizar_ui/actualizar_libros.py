from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QPushButton, QTableWidget, QLineEdit, QLabel,
                             QComboBox, QHBoxLayout, QMessageBox, QTableWidgetItem,
                             QAbstractItemView, QCheckBox, QHeaderView)

from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal

from connection.session import (select_estado_libro_all,
                                select_copia_libros_by_id)
from connection.connection import update_estado_libro

style_sheet = """
QWidget#ActualizarLibros {
    background-color: #B4E7FF;
}

QPushButton {
    background-color: #C7FF9C;
    color: #222;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 14px;
    border: 1px solid #a6d97b;
}

QPushButton:pressed {
    background-color: #b2f27c;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #bbb;
    border-radius: 8px;
    padding: 10px;
}

QTableWidget {
    background-color: #FFF9DB;
    border: 1px solid #ccc;
    font-size: 14px;
}

QHeaderView::section {
    background-color: #FFF3B0;
    font-weight: bold;
    padding: 6px;
    border: none;
}

QComboBox {
    font-size: 14px;
    padding: 5px;
}
"""

class ActualizarLibros(QWidget):
    actualizar_datos = pyqtSignal()
    cerrar_ventana = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Biblioteca | ACTUALIZACION ESTADO DE LIBROS")
        self.setObjectName("ActualizarLibros")
        self.setStyleSheet(style_sheet)
        self.setGeometry(200,200,700,700)

        #Layout
        horizontal_layout_1 = QHBoxLayout()
        vertical_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        #Creacion de los QLineEdits
        self.buscar_codbarras = QLineEdit()

        #Creacion de Boton
        self.buscar_libros = QPushButton("Buscar")
        self.cambiar_estado = QPushButton("Cambiar estado")

        #Creacion de combobox
        self.estado = QComboBox()
        self.estado.setStyleSheet("background-color: #FFFFFF;")

        #Creacion del Checkbox
        self.check = QCheckBox("Cerrar ventana luego de cambios")

        #creacion de labels
        self.cod = QLabel("Ingresa codigo de barras")

        #Creacion de la tabla
        self.tabla_cambiarlibros = QTableWidget()
        self.tabla_cambiarlibros.setColumnCount(6)
        item = QTableWidgetItem()
        item.setText("Nombre Libro")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Autor")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setText("Editorial")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setText("Fecha Ingreso Biblioteca")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        item.setText("Estado del Libro")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        item.setText("Id Interno")
        self.tabla_cambiarlibros.setHorizontalHeaderItem(5, item)

        #Asignar tablas
        header = self.tabla_cambiarlibros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_cambiarlibros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_cambiarlibros.setSelectionMode(QAbstractItemView.MultiSelection)

        #Asignar los widgets/layout a los principales layout
        horizontal_layout_1.addWidget(self.buscar_codbarras)
        horizontal_layout_1.addWidget(self.buscar_libros)

        horizontal_layout.addWidget(self.cambiar_estado)
        horizontal_layout.addWidget(self.estado)
        horizontal_layout.addWidget(self.check)

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

    def verificar_codi(self):
        msg = QMessageBox()
        msg.setWindowTitle("Libro no encontrado")
        msg.setText("No se ha encontrado el libro espeficicado")
        msg.setIcon(QMessageBox.Information)
        
    def seleccion_datos(self):
        is_true = self.check.isChecked()
        if is_true is not True:
            self.act_datos()
        else:
            self.act_datos()
            self.actualizar_datos.emit()
            self.cerrar_ventana.emit()
            self.close()

    def color_por_estado(self, estado: str) -> QColor:
        colores = {
            "Buen Estado": QColor(90,255,90),
            "Mal Estado": QColor(255, 205, 0),
            "Estado Regular": QColor(255,255,0),
            "Dado de Baja": QColor(255,50,50)
        }
        return colores.get(estado, QColor(255, 255, 255))

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

            if copias:
                for l in copias:
                    self.tabla_cambiarlibros.setItem(tablerow, 0, QTableWidgetItem(l.nombre_libro))
                    self.tabla_cambiarlibros.setItem(tablerow, 1, QTableWidgetItem(l.cod_barras))
                    self.tabla_cambiarlibros.setItem(tablerow, 2, QTableWidgetItem(l.autor))
                    self.tabla_cambiarlibros.setItem(tablerow, 3, QTableWidgetItem(str(l.fecha_publicacion)))
                    self.tabla_cambiarlibros.setItem(tablerow, 4, QTableWidgetItem(l.estado_libro))
                    self.tabla_cambiarlibros.setItem(tablerow, 5, QTableWidgetItem(str(l.id_copia)))


                    estado = self.tabla_cambiarlibros.item(tablerow, column_count).text()
                    self.tabla_cambiarlibros.item(tablerow, column_count).setBackground(self.color_por_estado(estado))

                    tablerow+=1

            else:
                pass
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error {e}")

    def act_datos(self):
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
        
    def closeEvent(self, a0):
        self.cerrar_ventana.emit()
        a0.accept()
