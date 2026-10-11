from PySide6.QtWidgets import (
    QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QStackedLayout,
    QTextEdit, QDialog
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QSize
import numpy as np
import constants as cnsts
from dataclasses import dataclass

class BasicVBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
        
class BasicHBoxLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

class BasicLabel(QLabel):
    def __init__(self, text: str, *,
                 font: QFont | None = None):
        super().__init__(parent=None)
        
        if text:
            self.setText(text)
            
class BasicPushButton(QPushButton):
    def __init__(self,
                 text: str | None = None, *,
                 image: bytes | QPixmap | np.ndarray | None = None,
                 size: QSize | None = None,
                 width: int | None = None,
                 height: int | None = None):
        super().__init__(parent=None)
        
        if text:
            self.setText(text)
        if image:
            pass
        
        if size:
            self.setFixedSize(size)
        elif width or height:
            if width:
                self.setFixedWidth(width)
            if height:
                self.setFixedHeight(height)
        
class BasicTextEdit(QTextEdit):
    def __init__(self, *,
                 read_only: bool = False):
        super().__init__(parent=None)
        
        if read_only:
            self.setReadOnly(True)

class BasicLineEdit(QLineEdit):
    def __init__(self, *,
                 font: QFont | None = None,
                 width: int | None = None,):
        super().__init__(parent=None)
        if font:
            self.setFont(font)
        if width:
            self.setFixedWidth(width)
        
        
class BasicMessageBox(QDialog):
    @dataclass
    class ExitCodes:
        UserClosed = 0
        Success = 1
        Failed = 2
        
    def __init__(self, parent,
                 text: str | None = None,
                 *, 
                 size: QSize | None = None,
                 is_input: bool = False,
                 hide_input: bool = False,
                 font: QFont | None = None,
                 confirm: bool = False):
        super().__init__(parent)
        
        self.setFixedSize(cnsts.Gui.sizes.MessageBoxSize)
        
        self.label = BasicLabel(text, font=font)
        self.inputBox = BasicLineEdit(width=200)
        if hide_input:
            self.inputBox.setEchoMode(QLineEdit.EchoMode.Password)
        doneButton = BasicPushButton("Done", width=100)
        
        mainLayout = BasicVBoxLayout()
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        if is_input:
            mainLayout.addSpacing(20)
            mainLayout.addWidget(self.inputBox, alignment=Qt.AlignmentFlag.AlignCenter)
            mainLayout.addSpacing(10)
            mainLayout.addWidget(doneButton, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(mainLayout)
        
        doneButton.clicked.connect(lambda: self.done(self.ExitCodes.Success))
        
    def getInput(self) -> str:
        return self.inputBox.text()
        
        