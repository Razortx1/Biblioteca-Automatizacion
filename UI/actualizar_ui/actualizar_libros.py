"""
    **Modulo actualizar_libros**\n
    Es el modulo que se encarga de la parte visual con la cual el usuario
    podra hacer la actualizaciones con respecto a los estados de los libros\n

    **Importaciones del modulo**\n
    PyQt5.QtWidgets ----> Usado principalmente para obtener los widgets que serán
                            usados durante la creacion del libro\n
    PyQt5.QtCore ----> Usado para obtener, ya sean las señales, o algunas
                        configuraciones adicionales para los widgets\n
    PyQt.QtGui -----> Usado para cambiar los colores de la ultima columna de la tabla

    modulo connection ----> Usado para traer la funcion update_estado_libro, esto con el fin
                            de poder actualizar el estado del libro a la base de datos, tomando los datos
                            encontrados en los widgets\n
    modulo session -----> Usado para poder obtener todos los estados del libro y todos los libros que
                            pertenecen a dicho estado

"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QPushButton, QTableWidget,
                             QComboBox, QHBoxLayout, QMessageBox, QTableWidgetItem,
                             QAbstractItemView, QCheckBox, QHeaderView)

from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal

from connection.session import (select_estado_libro_all,
                                select_prestamo_libro)
from connection.connection import update_estado_libro

style_sheet = """
QWidget#ActualizarLibros {
    background-color: #6ec1e4;
}

QPushButton {
    background-color: #61ce70;
    color: #000000;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 14px;
    border: 1px solid #009c88;
    outline: none;
    height: 25px;
}

QPushButton:hover {
    background-color: #79db8a;
}

QPushButton:pressed {
    background-color: #4fa75e
}

QLineEdit,
QComboBox {
    background-color: #ffffff;
    border: 1px solid #bbb;
    border-radius: 8px;
    padding: 10px;
}
QTableWidget {
    background-color: #fdf9e3;
    border: 1px solid #ccc;
    font-size: 14px;
}

QHeaderView::section {
    background-color: #f7bc09;
    font-weight: bold;
    padding: 6px;
    border: none;
    color: #54595F
}"""

class ActualizarLibros(QWidget):
    """
    **Clase ActualizarLibros**\n
    Permite el poder actualizar los estados de los libros a traves de una interfaz parecida a un formularios.
    Este formulario cuenta con los siguientes campos: \n

    - Datos pertenecientes a la tabla\n
    - Estado de libro a partir de ComboBox
    """
    actualizar_datos = pyqtSignal()
    cerrar_ventana = pyqtSignal()
    def __init__(self):
        """
        **Funcion __ init __**\n
        Se encarga de cargar tanto los widgets como los datos a los widgets tanto al comobox
        como a la tabla, detectandose a penas el usuario presiona el boton de actualizar estado
        """
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
        """
        **Funcion seleccion_datos**\n
        Es la encargada de comprobar el estado actual del checkbox, esto con el fin de poder
        cerrar o no cerrar la ventana si es que el usuario no lo desea
        """
        is_true = self.check.isChecked()
        if is_true is not True:
            self.act_datos()
        else:
            self.act_datos()
            self.actualizar_datos.emit()
            self.cerrar_ventana.emit()
            self.close()

    def color_por_estado(self, estado: str) -> QColor:
        """
        **Funcion color_por_estado**\n
        Se encarga de obtener algunos colores para poder otorgarselas a la tabla, los cuales son los siguientes:\n

        - Buen estado: Verde pastel clarito
        - Mal Estado: Amarrillo pastel algo intenso
        - Estado Regular: Amarillo pastel algo menos inteso
        - Dado de Baja: Rojo pastel

        **Retorna**\n
        colores: Dict[str, QColor]
        """
        colores = {
            "Buen Estado": QColor("#b2f7b2"),
            "Mal Estado": QColor("#ffd62e"),
            "Estado Regular": QColor("#ffe066"),
            "Dado de Baja": QColor("#ff6b6b")
        }
        return colores.get(estado, QColor(255, 255, 255))

    def rellenar_tabla(self):
        """
        **Funcion rellenar_tabla**\n
        Se encarga de obtener todos los libros para luego cargarlos a la tabla

        **Excepcion**\n
        Se implementa traceback para errores fantasmas ademas de imprimir el error por consola
        """
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
        """
        **Funcion traer_objeto**\n
        Se encarga de traer los datos de los libros a traves de la señal propuesta por historial_libro

        **Parametros**\n
        - nombre: str\n
        - autor: str\n
        - editorial: str\n

        **Retorna**\n
        nombre_libro: str\n
        autor_libro: str\n
        editorial_libro: str\n
        """
        self.nombre = nombre_
        self.autor = autor_
        self.editorial = editorial_
        self.rellenar_tabla()
        return self.nombre, self.autor, self.editorial

    def act_datos(self):
        """
        **Funcion act_datos**\n
        Permite la actualizacion de los libros con respecto a su estado,
        con diversos validadores para poder comprobar si fue seleccionado un libro o no, o
        si en caso que el usuario no desee actualizar ahora el libro
        """
        selected_rows = self.tabla_cambiarlibros.selectionModel().selectedRows()
        if not selected_rows:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion erronea")
            msg.setText("Debe seleccionar al menos un libro")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
            return
            
        estado_id = self.estado.currentIndex() + 1

        for row in selected_rows:
            id_item = self.tabla_cambiarlibros.item(row.row(), 5)
            if id_item:
                copia_id = int(id_item.text())
                update_estado_libro(copia_id, estado_id)
        msg_ok = QMessageBox()
        msg_ok.setWindowTitle("Operacion Exitosa")
        msg_ok.setText("Se ha actualizado correctamente el estado del libro")
        msg_ok.setIcon(QMessageBox.Information)
        msg_ok.exec()     
        self.rellenar_tabla()
        
    def closeEvent(self, a0):
        """
        **Funcion closeEvent**\n
        Detecta si la ventana se cierra ya sea a traves de un boton o si se cierra
        por el boton de la X. Esto permite que se pueda volver a abrir sin necesidad
        de cerrar la aplicacion
        """
        self.cerrar_ventana.emit()
        a0.accept()
