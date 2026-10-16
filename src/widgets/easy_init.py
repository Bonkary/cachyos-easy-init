from widgets import basics
from PySide6.QtCore import (
    Signal, Slot, QObject
)
from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QWidget
from widgets.basics import *
from widgets.selections import Selections
from widgets.secure_boot import SecureBoot
import linux_sbctl.pyside as sbctl
import os
import subprocess

class EasyInit(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        
        self.selections = Selections()
        self.secureBoot = SecureBoot()
        
        mainStack = BasicStackedLayout()
        mainStack.addWidget(self.selections)
        mainStack.addWidget(self.secureBoot)

        self.setLayout(mainStack)

        self.selections.secureBoot.clicked.connect(lambda: mainStack.setCurrentWidget(self.secureBoot))
    
        
            
