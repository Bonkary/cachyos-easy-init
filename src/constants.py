from dataclasses import dataclass
from PySide6.QtCore import QSize
from PySide6.QtGui import QFont

def _create_font(family: str = 'Arial', point_size: int = 16,
                 bold: bool = False, underline: bool = False):
    font = QFont()
    font.setPointSize(point_size)
    font.setFamily(family)
    font.setBold(bold)
    font.setUnderline(underline)
    
    return font

@dataclass
class Gui:    
    @dataclass
    class sizes:
        AppSize = QSize(800,600)
        MessageBoxSize = QSize(400,200)
        
    @dataclass
    class Fonts:
        default = _create_font()
        MessageBox = _create_font(point_size=14)
        