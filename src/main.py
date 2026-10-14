import constants as cnsts
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QProcess
import PySide6.QtAsyncio as QtAsyncio
import sys
from widgets.easy_init import EasyInit
from widgets.basics import *
import linux_sbctl.pyside as sbctl
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.setFixedSize(cnsts.Gui.Sizes.AppSize)
        easyInit = EasyInit()
        
        self.setCentralWidget(easyInit)

if __name__ == "__main__":
    app = QApplication([])
    app.setFont(cnsts.Gui.Fonts.Default)

    window = MainWindow()
    window.setStyleSheet("background-color: #2b6868;")
    window.show()
    
    sys.exit(app.exec())
    
