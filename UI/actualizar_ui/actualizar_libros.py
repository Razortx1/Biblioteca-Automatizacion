from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QPushButton, QTableWidget, QLineEdit, QLabel,
                             QComboBox, QHBoxLayout, QMessageBox, QTableWidgetItem,
                             QAbstractItemView, QCheckBox, QHeaderView)

from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal

from connection.session import (select_estado_libro_all,
                                select_copia_libros_by_id, select_prestamo_libro)
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

        #Creacion de Boton
        self.cambiar_estado = QPushButton("Cambiar estado del libro(s)")

        #Creacion de combobox
        self.estado = QComboBox()
        self.estado.setStyleSheet("background-color: #FFFFFF;")

        #Creacion del Checkbox
        self.check = QCheckBox("Cerrar ventana luego de cambios")

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

        self.tabla_cambiarlibros.setColumnHidden(5, True)

        #Asignar tablas
        header = self.tabla_cambiarlibros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_cambiarlibros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_cambiarlibros.setSelectionMode(QAbstractItemView.MultiSelection)

        #Asignar los widgets/layout a los principales layout

        horizontal_layout.addWidget(self.cambiar_estado)
        horizontal_layout.addWidget(self.estado)
        horizontal_layout.addWidget(self.check)

        vertical_layout.addLayout(horizontal_layout_1)
        vertical_layout.addWidget(self.tabla_cambiarlibros)
        vertical_layout.addLayout(horizontal_layout)
        

        self.setLayout(vertical_layout)

        #Establecer funciones del boton
        self.cambiar_estado.clicked.connect(self.seleccion_datos)

        #Rellenar Combobox
        estado_libro = select_estado_libro_all()
        for es in estado_libro:
            self.estado.insertItem(es[0].id_estadolibro, es[0].estado_libro)
        
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
            "Buen Estado": QColor("#b2f7b2"),
            "Mal Estado": QColor("#ffd62e"),
            "Estado Regular": QColor("#ffe066"),
            "Dado de Baja": QColor("#ff6b6b")
        }
        return colores.get(estado, QColor(255, 255, 255))

    def rellenar_tabla(self):
        try:
            self.tabla_cambiarlibros.setRowCount(0)
            copias = select_prestamo_libro(self.nombre, self.autor, self.editorial)
            tablerow = 0
            column_count = self.tabla_cambiarlibros.columnCount()-2

            if copias:
                for co in copias:
                    row_position = self.tabla_cambiarlibros.rowCount()
                    self.tabla_cambiarlibros.insertRow(row_position)
                    self.tabla_cambiarlibros.setItem(tablerow, 0, QTableWidgetItem(co.nombre_libro))
                    self.tabla_cambiarlibros.setItem(tablerow, 1, QTableWidgetItem(co.autor))
                    self.tabla_cambiarlibros.setItem(tablerow, 2, QTableWidgetItem(co.editorial))
                    self.tabla_cambiarlibros.setItem(tablerow, 3, QTableWidgetItem(str(co.fecha_entrada)))
                    self.tabla_cambiarlibros.setItem(tablerow, 4, QTableWidgetItem(co.estado_libro))
                    self.tabla_cambiarlibros.setItem(tablerow, 5, QTableWidgetItem(str(co.id_copia)))


                    estado = self.tabla_cambiarlibros.item(tablerow, column_count).text()
                    self.tabla_cambiarlibros.item(tablerow, column_count).setBackground(self.color_por_estado(estado))

                    tablerow+=1

            else:
                pass
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error {e}")

    def traer_datos(self, nombre_, autor_, editorial_):
        self.nombre = nombre_
        self.autor = autor_
        self.editorial = editorial_
        self.rellenar_tabla()
        return self.nombre, self.autor, self.editorial

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
        self.rellenar_tabla()
        
    def closeEvent(self, a0):
        self.cerrar_ventana.emit()
        a0.accept()
