from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton)
from PyQt5.QtCore import (pyqtSignal)

class MenuImpresiones(QWidget):
    volver_principal = pyqtSignal()
    ir_a_historial_impresiones = pyqtSignal()
    ir_a_agregar_impresiones = pyqtSignal()

    def __init__(self):
        super().__init__()

        #Definicion de Layout
        horizontal_layout = QHBoxLayout()

        #Creacion de los Botones
        self.historial_impresion = QPushButton("Historial de Impresion")
        self.agregar_impresion = QPushButton("Agregar Impresion")
        self.volver = QPushButton("Volver Atras")

        #Agregarndo los botones al layout
        horizontal_layout.addWidget(self.historial_impresion)
        horizontal_layout.addWidget(self.agregar_impresion)
        horizontal_layout.addWidget(self.volver)

        self.setLayout(horizontal_layout)

        #Funcionalidad del boton
        self.volver.clicked.connect(self.volver_principal.emit)



