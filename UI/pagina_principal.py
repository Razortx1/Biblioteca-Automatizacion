"""
    **Modulo pagina_principal.py**\n
    Corresponde a la primera ventana que se mostrará al usuario. Esta esta compuesta
    por 4 botones que estan dirigidos hacia las diversas ventanas que estan presentes
    en el sistema\n

    **Importaciones del modulo**\n
    PyQt5.QtWidgets ---->  Usado para obtener los diversos widgets necesarios para una
                            pagina principal\n
    PyQt5.QtCore -----> Usado para obtener configuraciones adicionales, ademas de las señales
                        se que usarán durante el ciclo de vida del sistema
"""

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QSpacerItem,
    QSizePolicy, QFrame, QHBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal


class PaginaPrincipal(QWidget):
    """
    **Clase PaginaPrincipal**\n
    Es la primera vista que logra observar el usuario. Esta contiene 4 botones que redirigen
    a las distintas vistas\n
    """
    # Señales
    ir_a_agregar_libros = pyqtSignal()
    ir_a_historia_libros = pyqtSignal()
    ir_a_menu_impresiones = pyqtSignal()
    ir_a_historial_prestamo = pyqtSignal()

    def __init__(self):
        """
        **Funcion**\n
        Es la funcion que realiza la carga a los widgets a la interfaz grafica
        """
        super().__init__()

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Título
        titulo = QLabel("Bienvenido")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        main_layout.addWidget(titulo)

        # Contenedor central con marco
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Botones con espaciado
        botones = [
            ("Registro de Libros", self.ir_a_agregar_libros),
            ("Inventario de Libros", self.ir_a_historia_libros),
            ("Ficha de Préstamos", self.ir_a_historial_prestamo),
            ("Menú de Impresiones", self.ir_a_menu_impresiones)
        ]

        grid_layout = QHBoxLayout()

        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        # Distribuye los botones en dos columnas
        for i, (texto, señal) in enumerate(botones):
            btn = QPushButton(texto)
            btn.setMinimumWidth(200)
            btn.setMinimumHeight(40)
            btn.clicked.connect(señal.emit)

            if i % 2 == 0:
                col1.addWidget(btn)
                col1.addSpacing(10)
            else:
                col2.addWidget(btn)
                col2.addSpacing(10)

        grid_layout.addLayout(col1)
        grid_layout.addSpacing(40)  # separación entre columnas
        grid_layout.addLayout(col2)

        frame.setLayout(grid_layout)
        main_layout.addWidget(frame)

        # Espaciador final
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)
