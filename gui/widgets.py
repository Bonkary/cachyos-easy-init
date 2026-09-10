from PySide6.QtCore import Qt, Signal, QObject, QSize
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QCheckBox,
    QWidget, QMainWindow, QBoxLayout)
from PySide6.QtGui import QFont, QIcon
from typing import Literal
from .constants import fonts, styles

# NOTE: These are all carry overs from another project...

class BasicWidget(QWidget):
    '''This is just to get the background color set to a single line of code rather than 4 lol'''
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def setBackgroundColor(self, color: str):
        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), color)
        self.setPalette(bg)

class BasicMainWindow(QMainWindow):
    '''This is just to get the background color set to a single line of code rather than 4 lol'''
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def setBackgroundColor(self, color: str) -> None:
        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), color)
        self.setPalette(bg)


# General
class TitledDropdown(QFrame):
    '''
    General Combobox that has a label to 'ID' it, I guess?
    
    Arguments:
        title - Text above the dropdown
        titleFont - Font of the title
        titlePlacement - Where to place the title
    '''
    def __init__(self, *, title: str, title_placement: Literal['top', 'side'], font: QFont = QFont(fonts.DEFAULT), values: list[str] = []):
        super().__init__()
        self.signals = DropdownSignals()
        self._values = values
        self.alertActive = False
        
         # Widgets
        titleLabel = BasicLabel(text=title, font=QFont(font))
        self._dropdown = BasicComboBox(width=200, stylesheet=styles.DROPDOWN)
        if self._values:
            for value in self._values:
                self._dropdown.addItem(value)
            self.setCurrentIndex(-1)
        
        # Layouts
        match title_placement:
            case 'top':
                mainLayout = BasicVBoxLayout()
                mainLayout.setDirection(QBoxLayout.Direction.TopToBottom)
            case 'side':
                mainLayout = BasicHBoxLayout()
                mainLayout.setDirection(QBoxLayout.Direction.LeftToRight)
            case _: 
                raise ValueError(f"{title_placement} is not a valid value (must be 'top' or 'side')")
        
        #   Main Layout
        mainLayout.addWidget(titleLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        mainLayout.addSpacing(3)
        mainLayout.addWidget(self._dropdown)
        
        self.setLayout(mainLayout)
        
        # Connections
        self._dropdown.currentTextChanged.connect(self.signals.textChanged.emit)
        
    def addItem(self, item: str|int) -> None:
        '''
        Add item to the dropdown
        
        Arguments:
            item - Value to add to the dropdown
        '''
        self._dropdown.addItem(item)
        self._values.append(item)
        
    def setCurrentText(self, text: str|int) -> None:
        '''
        Set the current value on the dropdown.
        
        Arguments:
            text - Text to set the dropdown to.
        '''
        self._dropdown.setCurrentText(text)
        
    def setCurrentIndex(self, index: int) -> None:
        '''
        Set the index of the dropdown.
        
        Arguments:
            index - Index to the set dropdown to.
        '''
        self._dropdown.setCurrentIndex(index)
        
    def getCurrentText(self) -> str:
        ''' Get the current text of the dropdown.'''
        return self._dropdown.currentText().strip()
        
    def removeItem(self, item: str) -> None:
        '''
        Remove item from the dropdown.
        
        Arguments:
            item - Value to remove from the dropdown.
        '''
        print(item)
        print(self._values)
        self._values.remove(item)
        self._dropdown.clear()
        for value in self._values:
            self._dropdown.addItem(value)
    
    def alert(self) -> None:
        '''Change the stylesheet to display an error.'''
        self.alertActive = True
        self._dropdown.setStyleSheet(styles.DROPDOWN_ALERT)
    
    def clearAlert(self) -> None:
        '''Change the stylesheet to the default.'''
        self.alertActive = False
        self._dropdown.setStyleSheet(styles.DROPDOWN)

class TitledLineEdit(QFrame):
    '''
    LineEdit that has a title.
    
    Arguments:
        title - Title of the LineEdit
        title_placement - Where to place the title.
        title_font - QFont to use for the title label.
        title_alignment - The alignment of the title.
        width - Width of the LineEdit
        spacing - Spacing between the title and LineEdit
        center_stretch - Whether to add strect between the Title and LineEdit.
        padding - Padding on the ends.
        center_padding - Padding between the Title and LineEdit.
        placeholder - Placeholder text.
    '''
    def __init__(self, *, title: str, title_placement: Literal['top', 'side'],
                 font: QFont = fonts.DEFAULT,
                 title_alignment: Literal['left', 'right', 'center'] = 'left',
                 spacing: int = 10, width: int = 100, center_stretch: bool = False,
                 padding: tuple[int:int] = (0,0), center_spacing: int = 10, placeholder: str = '',
                 underline: bool = False, bold: bool = False):
        super().__init__()
        self.signals = WidgetSignals()
        self.alertActive = False
        
        font = QFont(font)
        if font.isCopyOf(fonts.DEFAULT):
            font.setUnderline(underline)
            font.setBold(bold)
        
        # Widgets
        titleLabel = BasicLabel(text=title, font=font)
        self._entry = BasicLineEdit(width=width, stylesheet=styles.LINE_EDIT, placeholder=placeholder)
        
        # Layouts
        match title_placement:
            case 'top':
                mainLayout = BasicVBoxLayout()
                alignment = Qt.AlignmentFlag.AlignCenter
            case 'side':
                mainLayout = BasicHBoxLayout()
                alignment = Qt.AlignmentFlag.AlignCenter
            case _: 
                raise ValueError(f"{title_placement} is not a valid value")
        
        match title_alignment:
            case 'left':
                title_alignment = Qt.AlignmentFlag.AlignLeft
            case 'right':
                title_alignment = Qt.AlignmentFlag.AlignRight
            case 'center':
                title_alignment = Qt.AlignmentFlag.AlignCenter
        
        #   Main Layout
        mainLayout.addSpacing(padding[0])
        mainLayout.addWidget(titleLabel, alignment=title_alignment)
        mainLayout.addSpacing(center_spacing)
        if title_placement == 'side' and center_stretch:
            mainLayout.addStretch()
        mainLayout.addWidget(self._entry, alignment=alignment)
        mainLayout.addSpacing(padding[1])
        
        self.setLayout(mainLayout)
        
        # Connections
        self.signals.textChanged.connect(lambda: self._entry.textChanged.emit(self.getText()))
        self._entry.textChanged.connect(self.clearAlert)
        
    def getText(self) -> str:
        '''Get the text from the LineEdit'''
        return self._entry.text().strip()
    
    def setText(self, text: str) -> None:
        '''
        Set the text in the LineEdit
        
        Arguments:
            text - The text to set.
        '''
        self._entry.setText(text)

    def clear(self) -> None:
        '''Clear the LineEdit'''
        self._entry.setText("")
        self.clearAlert()

    def alert(self) -> None:
        '''Highlight the border red'''
        self.alertActive = True
        self._entry.setStyleSheet(styles.LINE_EDIT_ALERT)
        
    def clearAlert(self) -> None:
        '''Remove the red border'''
        self.alertActive = False
        self._entry.setStyleSheet(styles.LINE_EDIT)

class TitledLabel(QFrame):
    '''
    Label that has a title.
    
    Arguments: 
        title - The title.
        text - The text of the Label.
        title_font - QFont to use for the Title.
        text_font - QFont to use for the Label.
        spacing - Spacing between the Title and Label.
        underline - Whether to have the Title underlined.
        bold - Whether to bold the Title.
    '''
    def __init__(self, title: str, text: str, title_font: QFont = QFont(fonts.DEFAULT), bold: bool = True,
                 text_font: QFont = QFont(fonts.DEFAULT), spacing: int = 3, underline: bool = True):
        super().__init__()
        
        title_font.setUnderline(underline)
        title_font.setBold(bold)
        
        # Widgets
        titleLabel = BasicLabel(text=title, underline=underline, font=title_font)
        textLabel = BasicLabel(text=text, font=text_font)
        
        # Layouts
        mainLayout = BasicVBoxLayout()
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #   Main Layout
        mainLayout.addWidget(titleLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(textLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(mainLayout)

class BasicLabel(QLabel):
    '''
    QLabel but you can create/config it with less lines of code.
    
    Arguments:
        text - The text of the label.
        font - QFont of the label.
        alignment - Alignment of the text of the label.
        underline - Whether to underline the text.
        bold - Whether to bold the text.
        stylesheet - The stylesheet to use.
        width - The value of the width.
    '''
    def __init__(self, text: str = None, *, font: QFont = fonts.DEFAULT,
                 alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter, underline: bool | None = None,
                 stylesheet: str = None, width: int = None, bold: bool | None = None):
        super().__init__(parent=None, text=text)
        
        font = QFont(font) # Create copy so any constants dont get changed lol
        if not bold == None:
            font.setBold(bold)
        if not underline == None:
            font.setUnderline(underline)
        self.setFont(font)
            
        self.setAlignment(alignment)
        if width:
            self.setFixedWidth(width)
        if stylesheet:
            self.setStyleSheet(stylesheet)

class BasicPushButton(QPushButton):
    '''
    QPushButton but you can create/config it with less lines of code.
    
    Arguments:
        text - Text of the button.
        font - QFont of the button.
        width - Value of the width.
        height - Value of the height.
        stylesheet - Stylesheet to use.
        icon - The QIcon to use.
        flat - Whether to make the button flat.
    '''
    def __init__(self, *, text: str | None = None, font: QFont = fonts.DEFAULT, width: int = 100, height: int = 25,
                 stylesheet: str | None = None, icon: QIcon | None = None, flat: bool = False, size: QSize | None = None, hide: bool = False):
        super().__init__(parent=None)
        self.setFlat(flat)
        self.setText(text)
        self.setFont(font)
        if stylesheet:
            self.setStyleSheet(stylesheet)
        if icon:
            self.setIcon(icon)
        if size:
            self.setFixedSize(size)
        else:
            self.setFixedSize(QSize(width, height))
        if hide:
            self.hide()
        
class BasicComboBox(QComboBox):
    '''
    QComboBox but you can create/config it with less lines of code.
    
    ArgumentsL
        font - QFont to use.
        width - Value of the width.
        stylesheet - Stylesheet to use.
    '''
    def __init__(self, *, font: QFont = QFont(fonts.DEFAULT), width: int = None, stylesheet: str = None):
        super().__init__(parent=None)
        self.setFont(font)
        if width:
            self.setFixedWidth(width)
        if stylesheet:
            self.setStyleSheet(stylesheet)
            
class BasicLineEdit(QLineEdit):
    '''
    QLineEdit but you can create/config it with less lines of code.
    
    Arguments:
        font - QFont to use.
        width - Value of the width.
        stylesheet - Stylesheet to use.
        placeholder - Placeholder text.
    '''
    def __init__(self, *, font: QFont = QFont(fonts.DEFAULT), width: int = None, stylesheet: str = None, placeholder: str = None):
        super().__init__(parent=None)
        self.setFont(font)
        if width:
            self.setFixedWidth(width)
        if stylesheet:
            self.setStyleSheet(stylesheet)
        if placeholder:
            self.setText(placeholder)
        
class BasicCheckbox(QCheckBox):
    '''
    QComboBox but you can create/config it with less lines of code.
    
    Arguments:
        text - The text of the Checkbox.
        font - QFont to use.
        checked - Whether to start the Checkbox as checked.
    '''
    def __init__(self, text: str, *, font: QFont = QFont(fonts.DEFAULT), checked: bool = False):
        super().__init__(parent=None, text=text)
        self.setFont(font)
        if checked:
            self.setCheckState(Qt.CheckState.Checked)


# Layouts
class BasicHBoxLayout(QHBoxLayout):
    '''QHBoxLayout that has no padding around it.'''
    def __init__(self, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter, **kwargs):
        super().__init__(**kwargs)
        
        self.setAlignment(alignment)
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
        
class BasicVBoxLayout(QVBoxLayout):
    '''QVBoxLayout that has no padding around it.'''
    def __init__(self, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter, **kwargs):
        super().__init__(**kwargs)
        
        self.setAlignment(alignment)
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

# Signals 
class InputSignals(QObject):
    addCommand = Signal(object)

class DropdownSignals(QObject):
    textChanged = Signal(str)
  
class WidgetSignals(QObject):
    textChanged = Signal()



