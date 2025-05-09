from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QDateEdit, QSpacerItem, QSizePolicy, QMessageBox
)
from datetime import date

from PyQt5.QtCore import pyqtSignal
from connection.session import selected_libro_by_cod
from connection.connection import insertar_libros

class AgregarLibros(QWidget):
    volver_principal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Definición de Layouts
        layout_principal = QVBoxLayout()
        horizontal_layot = QHBoxLayout()
        form_layout_c1 = QVBoxLayout()
        form_layout_c2 = QVBoxLayout()
        button_layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_principal.setSpacing(20)

        # Widgets de entrada
        self.agregar_nombre = QLineEdit()
        self.agregar_nombre.setPlaceholderText("Ingrese nombre del libro")
        
        self.agregar_autor = QLineEdit()
        self.agregar_autor.setPlaceholderText("Ingrese el Autor")

        self.agregar_editorial = QLineEdit()
        self.agregar_editorial.setPlaceholderText("Ingrese la editorial")

        self.sector_biblioteca = QLineEdit()
        self.sector_biblioteca.setPlaceholderText("Ingrese el sector de la biblioteca donde esta la estanteria del libro")

        self.sector_estanteria = QLineEdit()
        self.sector_estanteria.setPlaceholderText("Ingrese el sector de la estanteria donde estará el libro")

        self.stock_libro = QLineEdit()
        self.stock_libro.setPlaceholderText("Ingrese el Stock disponible")

        # Botones
        self.button_agregar = QPushButton("Agregar nuevo Libro")
        self.volver_atras = QPushButton("Volver Atras")
        
        # Etiquetas
        self.nombre = QLabel("Nombre del Libro")
        self.editorial = QLabel("Editorial del Libro")
        self.autor = QLabel("Autor del Libro")
        self.stock = QLabel("Stock del Libro")
        self.sector_b = QLabel("Sector Biblioteca")
        self.sector_es = QLabel("Sector de la Estanteria")

        # Añadir widgets al layout

        form_layout_c1.addWidget(self.nombre)
        form_layout_c1.addWidget(self.agregar_nombre)
        
        form_layout_c1.addWidget(self.autor)
        form_layout_c1.addWidget(self.agregar_autor)

        form_layout_c1.addWidget(self.editorial)
        form_layout_c1.addWidget(self.agregar_editorial)

        form_layout_c2.addWidget(self.sector_b)
        form_layout_c2.addWidget(self.sector_biblioteca)

        form_layout_c2.addWidget(self.sector_es)
        form_layout_c2.addWidget(self.sector_estanteria)

        form_layout_c2.addWidget(self.stock)
        form_layout_c2.addWidget(self.stock_libro)

        # Añadir botones
        button_layout.addWidget(self.button_agregar)
        button_layout.addWidget(self.volver_atras)

        # Añadir todo a layout principal
        horizontal_layot.addLayout(form_layout_c1)
        horizontal_layot.addLayout(form_layout_c2)
        layout_principal.addLayout(horizontal_layot)
        layout_principal.addLayout(button_layout)
        layout_principal.addItem(spacer)

        # Establecer el layout principal
        self.setLayout(layout_principal)

        # Funcionalidad de los botones
        self.button_agregar.clicked.connect(self.agregar_boton)
        self.volver_atras.clicked.connect(self.volver_principal.emit)

    def agregar_boton(self):
        nombre = self.agregar_nombre.text()
        autor = self.agregar_autor.text()
        editorial = self.agregar_editorial.text()
        sector_biblioteca = self.sector_biblioteca.text()
        sector_estanteria = self.sector_estanteria.text()
        fecha = date.today()
        stock = self.stock_libro.text()

        # Validación simple para asegurarse de que los campos no están vacíos
        if not nombre or not stock or not editorial or not sector_biblioteca or not sector_estanteria:
            return
        if not stock.isdigit():
            msg = QMessageBox()
            msg.setWindowTitle("Error de Entrada")
            msg.setText("Por favor, ingrese un valor numérico valido para el stock.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec()
            return
        if not autor:
            autor = "Desconocido"

        # Llamada a la función para insertar el libro
        insertar_libros(nombre, autor, editorial, fecha, sector_biblioteca, sector_estanteria, stock)

        # Limpiar los campos después de agregar
        self.agregar_nombre.clear()
        self.agregar_autor.clear()
        self.agregar_editorial.clear()
        self.sector_biblioteca.clear()
        self.sector_estanteria.clear()
        self.stock_libro.clear()
        msg = QMessageBox()
        msg.setWindowTitle("Libro Agregado")
        msg.setText("El libro se ha agregado correctamente.")
        msg.setIcon(QMessageBox.Information)
        msg.exec()
