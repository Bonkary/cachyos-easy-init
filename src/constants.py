from dataclasses import dataclass
from PySide6.QtCore import QSize
from PySide6.QtGui import QFont
from pathlib import Path
import os

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
    class Sizes:
        AppSize = QSize(1300,800)
        MessageBoxSize = QSize(600,200)
        SecureBootSize = QSize(1200, 600)
        Button = QSize(200,40)
        
    @dataclass
    class Fonts:
        Default = _create_font()
        MessageBox = _create_font(point_size=14)
        Terminal = _create_font(point_size=11)
        
@dataclass
class Files:
    @dataclass
    class Tmp:
        SecureBoot = Path(os.path.join('/tmp', 'init-secure-boot'))
    
    @dataclass
    class Markdown:
        @dataclass
        class SecureBoot:
            _Root = Path(os.path.join(Path(__file__).parent, "dialog", 'secureboot'))
            Start = Path(os.path.join(_Root, 'start.md'))
            Windows = Path(os.path.join(_Root, 'windows.md'))
            SetupMode = Path(os.path.join(_Root, 'setupmode.md'))
            AsusSetup = Path(os.path.join(_Root, 'asus_setupmode.md'))
            MsiSetup = Path(os.path.join(_Root, 'msi_setupmode.md'))
            StandardSetup = Path(os.path.join(_Root, 'standard_setupmode.md'))