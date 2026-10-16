from widgets import basics
from PySide6.QtCore import (
    Signal, Slot, QObject
)
from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QWidget
from widgets.basics import *
from widgets.terminal import InternalTerminal
import linux_sbctl.pyside as sbctl
import asyncio

class Selections(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        
        self.label = BasicLabel("Select")

        self.secureBoot = BasicPushButton("Setup Secure Boot", size=cnsts.Gui.Sizes.Button)
        self.hermesStreaming = BasicPushButton("Hermes Streaming", size=cnsts.Gui.Sizes.Button)
        
        buttonSpacing = 20
        buttonsLayout = BasicVBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(self.secureBoot)
        buttonsLayout.addSpacing(buttonSpacing)
        buttonsLayout.addWidget(self.hermesStreaming)
        buttonsLayout.addStretch()
        
        mainLayout = BasicVBoxLayout()
        mainLayout.addSpacing(40)
        mainLayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(buttonsLayout)
        
        self.setLayout(mainLayout)
        