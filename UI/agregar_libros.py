from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QDateEdit, QSpacerItem, QSizePolicy, QMessageBox, QCompleter
)

from PyQt5.QtCore import pyqtSignal, Qt
from datetime import date

from connection.connection import insertar_libros
from connection.session import (select_distinct_nombre_libro, select_distinct_autor_libro, select_distinct_editorial_libro,
                                select_distinct_estanteria_libro, select_distinct_biblioteca_libro)

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

        # RellenarAutocompletadores
        nombre_libros = [nombre for nombre_ in select_distinct_nombre_libro() for nombre in nombre_]
        autor_libro = [autor for autor_ in select_distinct_autor_libro() for autor in autor_]
        editorial_libro = [editorial for editorial_ in select_distinct_editorial_libro() for editorial in editorial_]
        estanteria_libro = [estanteria for estanteria_ in select_distinct_estanteria_libro() for estanteria in estanteria_]
        biblioteca_libro = [biblioteca for biblioteca_ in select_distinct_biblioteca_libro() for biblioteca in biblioteca_]

        # Widgets de entrada
        self.agregar_nombre = QLineEdit()
        self.agregar_nombre.setPlaceholderText("Ingrese nombre del libro")
        self.nombre_completado = QCompleter(nombre_libros)
        self.nombre_completado.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.agregar_nombre.setCompleter(self.nombre_completado)
        
        self.agregar_autor = QLineEdit()
        self.agregar_autor.setPlaceholderText("Ingrese el Autor")
        self.autor_completado = QCompleter(autor_libro)
        self.autor_completado.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.agregar_autor.setCompleter(self.autor_completado)

        self.agregar_editorial = QLineEdit()
        self.agregar_editorial.setPlaceholderText("Ingrese la editorial")
        self.editorial_completado = QCompleter(editorial_libro)
        self.editorial_completado.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.agregar_editorial.setCompleter(self.editorial_completado)

        self.sector_biblioteca = QLineEdit()
        self.sector_biblioteca.setPlaceholderText("Ingrese el sector de la biblioteca donde esta la estanteria del libro")
        self.biblioteca_completado = QCompleter(biblioteca_libro)
        self.biblioteca_completado.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.sector_biblioteca.setCompleter(self.biblioteca_completado)

        self.sector_estanteria = QLineEdit()
        self.sector_estanteria.setPlaceholderText("Ingrese el sector de la estanteria donde estará el libro")
        self.estanteria_completado = QCompleter(estanteria_libro)
        self.estanteria_completado.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.sector_estanteria.setCompleter(self.estanteria_completado)

        self.stock_libro = QLineEdit()
        self.stock_libro.setPlaceholderText("Ingrese el Stock disponible")

        # Botones
        self.button_agregar = QPushButton("Agregar nuevo Libro")
        self.volver_atras = QPushButton("Volver al Menu Principal")
        
        # Etiquetas
        self.nombre = QLabel("Nombre del Libro *")
        self.editorial = QLabel("Editorial del Libro")
        self.autor = QLabel("Autor del Libro")
        self.stock = QLabel("Stock del Libro *")
        self.sector_b = QLabel("Sector Biblioteca *")
        self.sector_es = QLabel("Sector de la Estanteria *")

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

    def actualizar_autocompletados(self):
        nombre_libros = [nombre for nombre_ in select_distinct_nombre_libro() for nombre in nombre_]
        autor_libro = [autor for autor_ in select_distinct_autor_libro() for autor in autor_]
        editorial_libro = [editorial for editorial_ in select_distinct_editorial_libro() for editorial in editorial_]
        estanteria_libro = [estanteria for estanteria_ in select_distinct_estanteria_libro() for estanteria in estanteria_]
        biblioteca_libro = [biblioteca for biblioteca_ in select_distinct_biblioteca_libro() for biblioteca in biblioteca_]

        self.nombre_completado.model().setStringList(nombre_libros)
        self.autor_completado.model().setStringList(autor_libro)
        self.editorial_completado.model().setStringList(editorial_libro)
        self.biblioteca_completado.model().setStringList(estanteria_libro)
        self.estanteria_completado.model().setStringList(biblioteca_libro)

    def agregar_boton(self):
        nombre = self.agregar_nombre.text()
        autor = self.agregar_autor.text()
        editorial = self.agregar_editorial.text()
        sector_biblioteca = self.sector_biblioteca.text()
        sector_estanteria = self.sector_estanteria.text()
        fecha = date.today()
        stock = self.stock_libro.text()

        # Validación simple para asegurarse de que los campos no están vacíos
        if not nombre or not stock or not sector_biblioteca or not sector_estanteria:
            msg = QMessageBox()
            msg.setWindowTitle("Error de Entrada")
            msg.setText("Favor de ingresar los datos correspondientes del libro segun muestra el formulario \n"
            "A excepcion de autor o editorial si se desconoce")
            msg.setIcon(QMessageBox.Warning)
            msg.exec()
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
        if not editorial:
            editorial = "Desconocido"

        # Llamada a la función para insertar el libro
        insertar_libros(nombre, autor, editorial, fecha, sector_biblioteca, sector_estanteria, stock)

        # Limpiar los campos después de agregar
        self.agregar_nombre.clear()
        self.agregar_autor.clear()
        self.agregar_editorial.clear()
        self.sector_biblioteca.clear()
        self.sector_estanteria.clear()
        self.stock_libro.clear()

        # Actualizar los autocompletados luego de agregar
        self.actualizar_autocompletados()
