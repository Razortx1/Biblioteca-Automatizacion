from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QDateEdit, QSpacerItem, QSizePolicy
)

from PyQt5.QtCore import pyqtSignal
from connection.session import selected_libro_by_cod
from connection.connection import insertar_libros

class AgregarLibros(QWidget):
    volver_principal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Definición de Layouts
        layout_principal = QVBoxLayout()
        form_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_principal.setSpacing(20)

        # Widgets de entrada
        self.agregar_nombre = QLineEdit()
        self.agregar_nombre.setPlaceholderText("Ingrese nombre del libro")
        self.agregar_nombre.setDisabled(True)
        
        self.agregar_codigo = QLineEdit()
        self.agregar_codigo.setPlaceholderText("Ingrese el Código de Barras")
        
        self.agregar_autor = QLineEdit()
        self.agregar_autor.setPlaceholderText("Ingrese el Autor")
        self.agregar_autor.setDisabled(True)

        self.fecha_publicacion = QDateEdit()
        self.fecha_publicacion.setDisplayFormat("yyyy-MM-dd")
        self.fecha_publicacion.setCalendarPopup(True)
        self.fecha_publicacion.setDisabled(True)

        self.stock_libro = QLineEdit()
        self.stock_libro.setPlaceholderText("Ingrese el Stock disponible")

        # Botones
        self.button_agregar = QPushButton("Agregar nuevo Libro")
        self.volver_atras = QPushButton("Volver Atras")
        self.button_buscar = QPushButton("Buscar")
        
        # Etiquetas
        self.nombre = QLabel("Nombre del Libro")
        self.codigo_barras = QLabel("Código de Barras del Libro")
        self.autor = QLabel("Autor del Libro")
        self.publicacion = QLabel("Fecha de Publicación")
        self.stock = QLabel("Stock del Libro")

        # Añadir widgets al layout
        form_layout.addWidget(self.codigo_barras)
        form_layout.addWidget(self.agregar_codigo)
        form_layout.addWidget(self.button_buscar)

        form_layout.addWidget(self.nombre)
        form_layout.addWidget(self.agregar_nombre)
        
        form_layout.addWidget(self.autor)
        form_layout.addWidget(self.agregar_autor)

        form_layout.addWidget(self.publicacion)
        form_layout.addWidget(self.fecha_publicacion)

        form_layout.addWidget(self.stock)
        form_layout.addWidget(self.stock_libro)

        # Añadir botones
        button_layout.addWidget(self.button_agregar)
        button_layout.addWidget(self.volver_atras)

        # Añadir todo a layout principal
        layout_principal.addLayout(form_layout)
        layout_principal.addLayout(button_layout)
        layout_principal.addItem(spacer)

        # Establecer el layout principal
        self.setLayout(layout_principal)

        # Funcionalidad de los botones
        self.button_agregar.clicked.connect(self.agregar_boton)
        self.volver_atras.clicked.connect(self.volver_principal.emit)
        self.button_buscar.clicked.connect(self.boton_buscar)

    def boton_buscar(self):
        libro = selected_libro_by_cod(self.agregar_codigo.text())
        if libro:
            self.agregar_nombre.setText(libro[0][0].nombre_libro)
            self.agregar_autor.setText(libro[0][0].autor)
            self.fecha_publicacion.setDate(libro[0][0].fecha_publicacion)
            self.agregar_nombre.setDisabled(True)
            self.agregar_autor.setDisabled(True)
            self.fecha_publicacion.setDisabled(True)
        else:
            self.agregar_nombre.setDisabled(False)
            self.agregar_autor.setDisabled(False)
            self.fecha_publicacion.setDisabled(False)

    def agregar_boton(self):
        nombre = self.agregar_nombre.text()
        cod_barras = self.agregar_codigo.text()
        autor = self.agregar_autor.text()
        fecha = self.fecha_publicacion.dateTime().toPyDateTime().date()
        stock = self.stock_libro.text()

        # Validación simple para asegurarse de que los campos no están vacíos
        if not nombre or not cod_barras or not autor or not stock:
            return

        # Llamada a la función para insertar el libro
        insertar_libros(nombre, cod_barras, autor, fecha, stock)

        # Limpiar los campos después de agregar
        self.agregar_nombre.clear()
        self.agregar_codigo.clear()
        self.agregar_autor.clear()
        self.stock_libro.clear()
