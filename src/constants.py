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
        MessageBoxSize = QSize(600,200)
        
    @dataclass
    class Fonts:
        Default = _create_font()
        MessageBox = _create_font(point_size=14)
        Terminal = _create_font(point_size=11)
        
    @dataclass
    class Dialog:
        @dataclass
        class SecureBoot:
            Start = "\n".join([
                "Welcome. Let's get Secure Boot going.\n\n\n",
                "First, let's check if 'sbctl' is installed.\n",
                "This package is what's going to manage the keys.\n"
            ])
            
            Install = "Please dont touch me or my son. He's terminal."
            
            RebootForSetupMode = "\n\n".join([
                "Okay, I'd take a picture of this or something if you're nervous.\n\n",
                "Take a look at the terminal underneath me. (Or wherever it is)"
            ])

@dataclass
class Files:
    SecureBootTmp = '/tmp/easy-init-secure-boot'