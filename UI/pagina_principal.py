from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QSpacerItem,
    QSizePolicy, QFrame, QHBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal


class PaginaPrincipal(QWidget):
    # Señales
    ir_a_agregar_libros = pyqtSignal()
    ir_a_historia_libros = pyqtSignal()
    ir_a_menu_impresiones = pyqtSignal()
    ir_a_historial_prestamo = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Título
        titulo = QLabel("Sistema de Biblioteca")
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
            ("Menú de Impresiones", self.ir_a_menu_impresiones),
            ("Historial de Préstamos", self.ir_a_historial_prestamo)
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
