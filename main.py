import sys, os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QSizePolicy, QWidget, QStackedWidget,
                             QPushButton, QTableWidgetItem, QTableWidget,
                             QLabel, QLineEdit, QVBoxLayout, QGridLayout,
                             QMainWindow, QApplication)
from PyQt5.QtCore import (QLocale, QSize, Qt, QRect, QMetaObject,
                          QCoreApplication)

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS # for --onefile
        # bundle_dir = path.dirname(path.abspath(sys.executable)) # for --onedir
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(bundle_dir, relative_path)

icon = resource_path("images.ico")

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pruebas")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())