import sys
import os
from PyQt5.QtWidgets import (QSizePolicy, QWidget, QStackedWidget,
                             QPushButton, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QApplication, QLabel)
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtGui import QIcon, QPixmap

from UI.pagina_principal import PaginaPrincipal
from UI.agregar_libros import AgregarLibros
from UI.historia_libros import HistorialLibros
from UI.prestamo_libros import PrestamoLibros
from UI.menu_impresiones import MenuImpresiones
from UI.historial_prestamos import HistorialPrestamos
from UI.historial_impresiones import HistorialImpresiones
from UI.agregar_impresiones import AgregarImpresiones

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS  # for --onefile
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(bundle_dir, relative_path)

icon = resource_path("images/biblioteca.ico")

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Definición de las páginas a usar
        self.pages = {
            "pagina_principal": PaginaPrincipal(),
            "agregar_libros": AgregarLibros(),
            "historia_libros": HistorialLibros(),
            "prestamo_libros": PrestamoLibros(),
            "menu_impresiones" : MenuImpresiones(),
            "historial_prestamos": HistorialPrestamos(),
            "historial_impresiones" : HistorialImpresiones(),
            "agregar_impresiones": AgregarImpresiones()
        }

        # Definición de los parámetros para la Ventana
        self.setWindowTitle("Sistema Biblioteca | PAGINA PRINCIPAL")
        self.setLocale(QLocale(QLocale.Spanish, QLocale.Chile))
        self.showMaximized()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowIcon(QIcon(icon))
        self.setStyleSheet(open(resource_path("css/style.css")).read())

        # Definición para agregar el logo
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Definición imagen
        image_layout = QHBoxLayout()
        self.imagen_colegio = QLabel()
        pixmap = QPixmap(resource_path("images/logo_transparente.ico"))
        pixmap = pixmap.scaled(500, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imagen_colegio.setPixmap(pixmap)
        self.imagen_colegio.setAlignment(Qt.AlignCenter)

        image_layout.addWidget(self.imagen_colegio)

        main_layout.addLayout(image_layout)

        # Creación del StackWidget
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Definimos el layout central para centrar los widgets
        main_layout.setAlignment(Qt.AlignCenter)  # Centra los widgets en el layout

        main_widget.setLayout(main_layout)

        # Definición de las ventanas "hijas"
        self.page_indice = {}
        for i, (nombre, widget) in enumerate(self.pages.items()):
            self.stack.addWidget(widget)
            self.page_indice[nombre] = i
        # Definir primera pagina a mostrar
        self.stack.setCurrentIndex(0)

        # Establecer el funcionamiento para cambiar de páginas entre página principal a las demás
        self.pages["pagina_principal"].ir_a_agregar_libros.connect(lambda: self.cambiar_pagina("agregar_libros"))
        self.pages["pagina_principal"].ir_a_historia_libros.connect(lambda: self.cambiar_pagina("historia_libros"))
        self.pages["pagina_principal"].ir_prestamo_libro.connect(lambda: self.cambiar_pagina("prestamo_libros"))
        self.pages["pagina_principal"].ir_a_menu_impresiones.connect(lambda: self.cambiar_pagina("menu_impresiones"))
        self.pages["pagina_principal"].ir_a_historial_prestamo.connect(lambda: self.cambiar_pagina("historial_prestamos"))

        # Establecer el funcionamiento para cambiar de páginas entre el menú de impresiones a sus "hijas"
        self.pages["menu_impresiones"].ir_a_historial_impresiones.connect(lambda: self.cambiar_pagina("historial_impresiones"))
        self.pages["menu_impresiones"].ir_a_agregar_impresiones.connect(lambda: self.cambiar_pagina("agregar_impresiones"))

        # Establecer el funcionamiento para volver a las anteriores ventanas
        self.pages["agregar_libros"].volver_principal.connect(lambda: self.cambiar_pagina("pagina_principal"))
        self.pages["historia_libros"].volver_principal.connect(lambda: self.cambiar_pagina("pagina_principal"))
        self.pages["menu_impresiones"].volver_principal.connect(lambda: self.cambiar_pagina("pagina_principal"))
        self.pages["historial_prestamos"].volver_principal.connect(lambda: self.cambiar_pagina("pagina_principal"))
        self.pages["prestamo_libros"].volver_principal.connect(lambda: self.cambiar_pagina("pagina_principal"))

        # Establecer el funcionamiento para volver al menú de impresiones
        self.pages["agregar_impresiones"].volver_menu.connect(lambda: self.cambiar_pagina("menu_impresiones"))
        self.pages["historial_impresiones"].volver_menu.connect(lambda: self.cambiar_pagina("menu_impresiones"))

        # Asignar el widget principal a la ventana
        self.setCentralWidget(main_widget)

    # Función para cambiar entre páginas
    def cambiar_pagina(self, nombre_pagina):
        if nombre_pagina in self.page_indice:
            self.stack.setCurrentIndex(self.page_indice[nombre_pagina])
            nombre = nombre_pagina.replace("_", " ")
            nombre = nombre.upper()
            self.setWindowTitle(f"Sistema Biblioteca | {nombre}")
            if nombre_pagina == "historial_impresiones":
                self.pages[nombre_pagina].rellenar_tabla()
            elif nombre_pagina == "historia_libros":
                self.pages[nombre_pagina].rellenar_tabla()
            elif nombre_pagina == "historial_prestamos":
                self.pages[nombre_pagina].rellenar_tabla()
        else:
            print(f"Pagina {nombre_pagina} no encontrada")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
