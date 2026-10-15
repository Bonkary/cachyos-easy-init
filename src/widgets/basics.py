from PySide6.QtWidgets import (
    QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QStackedLayout,
    QTextEdit, QDialog, QTextBrowser
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QSize, QUrl
import numpy as np
import constants as cnsts
from dataclasses import dataclass
from pathlib import Path
import markdown

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

class BasicStackedLayout(QStackedLayout):
    def __init__(self):
        super().__init__()
        
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
                 read_only: bool = False,
                 font: QFont | None = None):
        super().__init__(parent=None)
        
        if read_only:
            self.setReadOnly(True)
        if font:
            self.setFont(font)

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
        Yes = 3
        No = 4
    
    @dataclass
    class Cache:
        Input = None
    def __init__(self, parent,
                 text: str | None = None,
                 *, 
                 size: QSize | None = None,
                 is_input: bool = False,
                 hide_input: bool = False,
                 font: QFont | None = None,
                 is_confirm: bool = False):
        super().__init__(parent)
        
        self.setFixedSize(cnsts.Gui.Sizes.MessageBoxSize)
        
        self.label = BasicLabel(text, font=font)
        self.inputBox = BasicLineEdit(width=200)
        if hide_input:
            self.inputBox.setEchoMode(QLineEdit.EchoMode.Password)
        doneButton = BasicPushButton("Done", width=100)
        
        yesButton = BasicPushButton("Yes")
        noButton = BasicPushButton("No")
        yesNoLayout = BasicHBoxLayout()
        yesNoLayout.addStretch()
        yesNoLayout.addWidget(noButton)
        yesNoLayout.addSpacing(10)
        yesNoLayout.addWidget(yesButton)
        yesNoLayout.addStretch()
        
        mainLayout = BasicVBoxLayout()
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        if is_input:
            mainLayout.addSpacing(20)
            mainLayout.addWidget(self.inputBox, alignment=Qt.AlignmentFlag.AlignCenter)
            mainLayout.addSpacing(10)
            mainLayout.addWidget(doneButton, alignment=Qt.AlignmentFlag.AlignCenter)
        
        if is_confirm:
            mainLayout.addSpacing(20)
            mainLayout.addLayout(yesNoLayout)
        
        self.setLayout(mainLayout)
        
        doneButton.clicked.connect(self.getInput)
        yesButton.clicked.connect(lambda: self.done(self.ExitCodes.Yes))
        noButton.clicked.connect(lambda: self.done(self.ExitCodes.No))
    
    def getInput(self) -> str:
        BasicMessageBox.Cache.Input = self.inputBox.text()
        self.done(BasicMessageBox.ExitCodes.Success)
        
class BasicMarkdown(QTextBrowser):
    def __init__(self, parent=None,
                 *,
                 size: QSize | None = None,
                 file: Path | None = None,
                 ext_links: bool = True,
                 spacing: int | None = None):
        super().__init__(parent)
        
        self.setOpenExternalLinks(ext_links)
        self.setLineWrapMode(QTextBrowser.LineWrapMode.WidgetWidth)
        self.setFont(cnsts.Gui.Fonts.MessageBox)
        self.setFixedSize(size if size else cnsts.Gui.Sizes.AppSize)
        
        if size:
            self.resize(size)
        
        if file:
            html = markdown.markdown(file.read_text(encoding=('utf-8')),
                                     extensions=["extra", "sane_lists", "nl2br"])
            self.setHtml(html)
            
        
            
            
            
            
            
            