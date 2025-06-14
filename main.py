"""
    **Modulo main.py**\n
    Es el encargado de inicializar todo el programa, desde la llamada a la base de datos, como
    todas las ventanas que vayan a utilizarse 

    **Imports del modulo**\n

    sys ---> Usado para obtener funciones de sistema
    os ----> Usado principalmente para obtener las url de los diversos iconos a usar\n
    PyQt5.QtWidgets ---> Usado para traer los diversos widgets que se necesitan para
                        crear la interfaz grafica
    PyQt5.QtCore ----> Usado principalmente para obtener otras configuraciones para los
                        widgets
    PyQt5.QtGui -----> Usado para obtener modulos con respecto a iconos e imagenes

    UI.pagina_principal ----> Usado como pagina para los widgets importados de PyQt5.QWidgets
                                StackWidgets
    UI.agregar_libros ----> Usado como pagina para los widgets importados de PyQt5.QWidgets
                                StackWidgets
    UI.historia_libros ----> Usado como pagina para los widgets importados de PyQt5.QWidgets
                                StackWidgets
    UI.prestamo_libros ----> Usado como pagina para los widgets importados de PyQt5.QWidgets
                                StackWidgets
    UI.menu_impresiones ----> Usado como pagina para los widgets importados de PyQt5.QWidgets
                                StackWidgets
    UI.historial_prestamos ----> Usado como pagina para los widgets importados de PyQt5.QWidgets
                                StackWidgets
    UI.historial_impresiones ----> Usado como pagina para los widgets importados de PyQt5.QWidgets
                                StackWidgets
    UI.agregar_prestamos ----> Usado como pagina para los widgets importados de PyQt5.QWidgets
                                StackWidgets
"""
import sys
import os
from PyQt5.QtWidgets import (QWidget, QStackedWidget,
                             QVBoxLayout, QHBoxLayout,
                             QMainWindow, QApplication, QLabel, QMenuBar, QAction,
                             QFileDialog, QMessageBox)
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
from connection.backup import backups_database_rotation, backups_restoration

def resource_path(relative_path):
    """
    **Funcion resource_path**\n
    Permite obtener la url completa de los archivos del sistema, con el fin de
    poder utilizarlos sin tener problemas con la implementacion de estos en otros
    entornos que no sean el pc del programador.\n 
    Estos archivos pueden ser imagenes, iconos o archivos de estilo como los .css\n

    **Parametros**\n
    - relative_path: str

    **Retorna**\n
    url: str

    **Ejemplo:**\n
    imagen = "image.png"\n
    img = resource_path(imagen)\n
    print(img) ------> c:/user/downloads/
    """
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS  # for --onefile
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(bundle_dir, relative_path)

icon = resource_path("images/biblioteca.ico")

class Window(QMainWindow):
    """
    **Clase Window**\n
    Es la clase principal del sistema. Es la encargada de llevar todos los procesos de carga de
    las demas ventanas, ademas de otorgarle los css correspondientes.\n

    Hereda de QMainWindow
    """
    def __init__(self):
        """
        **Funcion __ init __**\n
        Permite cargar todos los componentes que se van a utilizar durante el ciclo de vida de la
        aplicacion, como lo pueden ser los widgets, las señales, o la misma apertura de la aplicacion
        """
        super().__init__()

        # Definición de las páginas a usar
        self.pages = {
            "pagina_principal": PaginaPrincipal(),
            "agregar_libros": AgregarLibros(),
            "historia_libros": HistorialLibros(),
            "prestamo_libros": PrestamoLibros(),
            "menu_impresiones" : MenuImpresiones(),
            "ficha_prestamos": HistorialPrestamos(),
            "historial_impresiones" : HistorialImpresiones(),
            "agregar_impresiones": AgregarImpresiones()
        }
        # Implementacion de elementos para backup
        backups_database_rotation()
        menubar = QMenuBar()
        self.setMenuBar(menubar)
        restaurar = QAction("Copia de Seguridad", self)
        restaurar.triggered.connect(self.restauracion_backups)
        menubar.addAction(restaurar)

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
        self.pages["pagina_principal"].ir_a_menu_impresiones.connect(lambda: self.cambiar_pagina("menu_impresiones"))
        self.pages["pagina_principal"].ir_a_historial_prestamo.connect(lambda: self.cambiar_pagina("ficha_prestamos"))

        # Establecer el funcionamiento para cambiar de páginas entre el menú de impresiones a sus "hijas"
        self.pages["menu_impresiones"].ir_a_historial_impresiones.connect(lambda: self.cambiar_pagina("historial_impresiones"))
        self.pages["menu_impresiones"].ir_a_agregar_impresiones.connect(lambda: self.cambiar_pagina("agregar_impresiones"))

        #Establecer el funcionamiento para cammbiar de paginas entre el historial de libros y el prestamo de libros
        self.pages["historia_libros"].ir_prestamo_libro.connect(lambda: self.cambiar_pagina("prestamo_libros"))
        self.pages["historia_libros"].ir_prestamo_libro.connect(self.pages["prestamo_libros"].traer_objeto)


        # Establecer el funcionamiento para volver a las anteriores ventanas
        self.pages["agregar_libros"].volver_principal.connect(lambda: self.cambiar_pagina("pagina_principal"))
        self.pages["historia_libros"].volver_principal.connect(lambda: self.cambiar_pagina("pagina_principal"))
        self.pages["menu_impresiones"].volver_principal.connect(lambda: self.cambiar_pagina("pagina_principal"))
        self.pages["ficha_prestamos"].volver_principal.connect(lambda: self.cambiar_pagina("pagina_principal"))
        self.pages["prestamo_libros"].volver_principal.connect(lambda: self.cambiar_pagina("historia_libros"))

        # Establecer el funcionamiento para volver al menú de impresiones
        self.pages["agregar_impresiones"].volver_menu.connect(lambda: self.cambiar_pagina("menu_impresiones"))
        self.pages["historial_impresiones"].volver_menu.connect(lambda: self.cambiar_pagina("menu_impresiones"))

        # Asignar el widget principal a la ventana
        self.setCentralWidget(main_widget)
    
    def restauracion_backups(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de backup",
            resource_path("backups"),
            "Base de datos (*.db)"
        )
        if not path:
            # Usuario presionó cancelar en el diálogo de archivo
            msg_cancel = QMessageBox()
            msg_cancel.setWindowTitle("Acción cancelada")
            msg_cancel.setText("No se seleccionó ningún archivo.")
            msg_cancel.setIcon(QMessageBox.Information)
            msg_cancel.exec()
            return

        # Mostrar confirmación solo si se seleccionó un archivo
        msg = QMessageBox()
        msg.setWindowTitle("Confirmación")
        msg.setText(
            "¿Está seguro de que desea restaurar esta copia de seguridad?\n"
            "Se perderán los cambios hechos desde que se abrió el programa."
        )
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        respuesta = msg.exec()

        if respuesta == QMessageBox.Yes:
            nombre_backup = os.path.basename(path)
            if backups_restoration(nombre_backup):
                    msg = QMessageBox()
                    msg.setWindowTitle("Restauracion Exitosa")
                    msg.setText("Se restauró la base de datos correctamente.")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec()
            else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Error ocurrido")
                    msg.setText("No se pudo restaurar los datos a partir de la copia de seguridad")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec()
        else:
            msg_cancel = QMessageBox()
            msg_cancel.setWindowTitle("Acción cancelada")
            msg_cancel.setText("Se canceló la restauración.")
            msg_cancel.setIcon(QMessageBox.Information)
            msg_cancel.exec()

    # Función para cambiar entre páginas
    def cambiar_pagina(self, nombre_pagina):
        """
        **Funcion cambiar_pagina**\n
        Le permite, al stackwidget, ir cambiando entre las diversas paginas que este posee, ademas de
        poder actualizar las tablas y los combobox, en caso que esta las posea.\n

        **Parametros**\n
        self: Window\n
        nombre_pagina: str
        """
        if nombre_pagina in self.page_indice:
            self.stack.setCurrentIndex(self.page_indice[nombre_pagina])
            nombre = nombre_pagina.replace("_", " ")
            nombre = nombre.upper()
            self.setWindowTitle(f"Sistema Biblioteca | {nombre}")
            if nombre_pagina == "historial_impresiones":
                self.pages[nombre_pagina].rellenar_tabla()
                self.pages[nombre_pagina].rellenar_combobox()
            elif nombre_pagina == "historia_libros":
                self.pages[nombre_pagina].rellenar_tabla()
                self.pages[nombre_pagina].rellenar_combobox()
            elif nombre_pagina == "ficha_prestamos":
                self.pages[nombre_pagina].rellenar_tabla()
                self.pages[nombre_pagina].rellenar_combobox()
        else:
            print(f"Pagina {nombre_pagina} no encontrada")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
