from PyQt5.QtWidgets import (QSizePolicy, QWidget, QStackedWidget,
                             QPushButton, QTableWidgetItem, QTableWidget,
                             QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QApplication, QHeaderView)
from PyQt5.QtCore import (QLocale, QSize, Qt, QRect, QMetaObject,
                          QCoreApplication, pyqtSignal)

from PyQt5.QtGui import QColor

from connection.session import select_libros_available
from .actualizar_ui.actualizar_libros import ActualizarLibros

class HistorialLibros(QWidget):
    volver_principal = pyqtSignal()
    def __init__(self):
        super().__init__()            
        
        #Definicion del layout
        void_layout_1 = QVBoxLayout()
        void_layout_2 = QVBoxLayout()
        vertical_layout = QVBoxLayout()

        self.w = None

        self.voidLabel_1 = QLabel()
        self.voidLabel_2 = QLabel()
        void_layout_1.addWidget(self.voidLabel_1)
        void_layout_2.addWidget(self.voidLabel_2)
        #Creacion de la tabla
        self.tabla_libros = QTableWidget()
        self.tabla_libros.setColumnCount(6)
        item = QTableWidgetItem()
        item.setText("Nombre Libro")
        self.tabla_libros.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Codigo de Barras")
        self.tabla_libros.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setText("Autor")
        self.tabla_libros.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setText("Fecha Publicacion")
        self.tabla_libros.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        item.setText("Stock de Libros")
        self.tabla_libros.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        item.setText("Estado del Libro")
        self.tabla_libros.setHorizontalHeaderItem(5, item)

        #Tamaño Columnas
        header = self.tabla_libros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        #Creacion botones
        self.cambiar_estado = QPushButton("Cambiar Estado Libro")
        self.volver_inicio = QPushButton("Volver a Inicio")

        #Agregar los Widget al layout principal
        vertical_layout.addWidget(self.tabla_libros)
        vertical_layout.addWidget(self.cambiar_estado)
        vertical_layout.addWidget(self.volver_inicio)
        vertical_layout.addLayout(void_layout_1)
        vertical_layout.addLayout(void_layout_2)
        
        #Vaciado de tabla
        self.tabla_libros.setRowCount(0)

        #Relleno de Tabla
        self.rellenar_tabla()

        #Agregar el layout a la respectiva lista
        self.setLayout(vertical_layout)

        #Funcionamiento Botones
        self.cambiar_estado.clicked.connect(self.actualizar_estado)
        self.volver_inicio.clicked.connect(self.volver_principal.emit)


    def rellenar_tabla(self):
        libros = select_libros_available()
        tablerow = 0
        self.tabla_libros.setRowCount(50)

        column_count = self.tabla_libros.columnCount()

        mal_estado = QColor(255, 205, 0)
        buen_estado = QColor(90,255,90)
        dado_baja = QColor(255,50,50)
        estado_regular = QColor(255,255,0)


        if libros:
            for l in libros:
                self.tabla_libros.setItem(tablerow, 0, QTableWidgetItem(l.nombre_libro))
                self.tabla_libros.setItem(tablerow, 1, QTableWidgetItem(l.cod_barras))
                self.tabla_libros.setItem(tablerow, 2, QTableWidgetItem(l.autor))
                self.tabla_libros.setItem(tablerow, 3, QTableWidgetItem(str(l.fecha_publicacion)))
                self.tabla_libros.setItem(tablerow, 4, QTableWidgetItem(str(l.stock)))
                self.tabla_libros.setItem(tablerow, 5, QTableWidgetItem(l.estado_libro))

                texto_tabla = self.tabla_libros.item(tablerow, column_count-1).text()

                if texto_tabla == "Buen Estado":
                    self.tabla_libros.item(tablerow, column_count-1).setBackground(buen_estado)
                elif texto_tabla == "Mal Estado":
                    self.tabla_libros.item(tablerow, column_count-1).setBackground(mal_estado)
                elif texto_tabla == "Estado Regular":
                    self.tabla_libros.item(tablerow, column_count-1).setBackground(estado_regular)
                elif texto_tabla == "Dado de Baja":
                    self.tabla_libros.item(tablerow, column_count-1).setBackground(dado_baja)

                tablerow+=1
        else:
            pass

    def actualizar_estado(self):
        if self.w is None:
            self.w = ActualizarLibros()
            self.w.actualizar_datos.connect(self.rellenar_tabla)
            self.w.show()
        else:
            self.w = None
