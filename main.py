import sys, os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QSizePolicy, QWidget, QStackedWidget,
                             QPushButton, QTableWidgetItem, QTableWidget,
                             QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QApplication)
from PyQt5.QtCore import (QLocale, QSize, Qt, QRect, QMetaObject,
                          QCoreApplication)
from PyQt5.QtGui import QIcon, QPixmap

from UI.pagina_principal import PaginaPrincipal
from UI.agregar_libros import AgregarLibros
from UI.historia_libros import HistorialLibros

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS # for --onefile
        # bundle_dir = path.dirname(path.abspath(sys.executable)) # for --onedir
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(bundle_dir, relative_path)

icon = resource_path("images/biblioteca.ico")

class Window(QMainWindow):
    def __init__(self):
        #Definicion de los parametros para la Ventana
        super().__init__()
        self.setWindowTitle("Sistema Biblioteca")
        self.setLocale(QLocale(QLocale.Spanish, QLocale.Chile))
        self.showMaximized()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowIcon(QIcon(icon))
        self.setStyleSheet(open(resource_path("css/style.css")).read())
        #Definicion para agregar el logo
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        #Definicion imagen
        image_layout = QHBoxLayout()
        self.imagen_colegio = QLabel()
        pixmap = QPixmap(resource_path("images/logo_transparente.ico"))
        pixmap = pixmap.scaled(500, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imagen_colegio.setPixmap(pixmap)
        self.imagen_colegio.setAlignment(Qt.AlignCenter)


        image_layout.addWidget(self.imagen_colegio)

        main_layout.addLayout(image_layout)

        #Creacion del StackWidget
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        main_widget.setLayout(main_layout)
        
        #Definicion para el layout entre otros
        self.setCentralWidget(main_widget)
        self.page_1 = PaginaPrincipal()
        self.page_2 = AgregarLibros()
        self.page_3 = HistorialLibros()
        #Definicion de las ventanas "hijas"
        self.stack.addWidget(self.page_1)
        self.stack.addWidget(self.page_2)
        self.stack.addWidget(self.page_3)
        self.stack.setCurrentIndex(1)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())