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

class EasyInit(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        
        self.label = BasicLabel("Select")
        self.terminal = InternalTerminal()
        
        buttonWidth = 200
        self.secureBoot = BasicPushButton("Setup Secure Boot", width=buttonWidth)
        self.hermesStreaming = BasicPushButton("Hermes Streaming", width=buttonWidth)

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
        # mainLayout.addStretch()
        mainLayout.addWidget(self.terminal)

        self.setLayout(mainLayout)

        self.secureBoot.clicked.connect(lambda: asyncio.ensure_future(self.terminal.secure_boot()))
    
            
