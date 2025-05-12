from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                             QFrame, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import (pyqtSignal, Qt)

class MenuImpresiones(QWidget):
    volver_principal = pyqtSignal()
    ir_a_historial_impresiones = pyqtSignal()
    ir_a_agregar_impresiones = pyqtSignal()

    def __init__(self):
        super().__init__()

        #Definicion de Layout
        main_layout = QVBoxLayout()
        horizontal_layout = QVBoxLayout()

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)

        horizontal_layout.setAlignment(Qt.AlignTop | Qt.AlignVCenter)

        #Creacion de los Botones
        self.historial_impresion = QPushButton("Historial de Impresion")
        self.agregar_impresion = QPushButton("Agregar Impresion")
        self.volver = QPushButton("Volver al Menu Principal")

        #Agregarndo los botones al layout
        horizontal_layout.addWidget(self.agregar_impresion)
        horizontal_layout.addSpacing(10)
        horizontal_layout.addWidget(self.historial_impresion)
        horizontal_layout.addSpacing(10)
        horizontal_layout.addWidget(self.volver)

        frame.setLayout(horizontal_layout)
        main_layout.addWidget(frame)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)

        #Funcionalidad del boton
        self.historial_impresion.clicked.connect(self.ir_a_historial_impresiones.emit)
        self.agregar_impresion.clicked.connect(self.ir_a_agregar_impresiones.emit)
        self.volver.clicked.connect(self.volver_principal.emit)



