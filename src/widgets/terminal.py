from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QWidget, QInputDialog
from .basics import *
import linux_sbctl.pyside as sbctl
import sys

class InternalTerminal(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        
        self.outputView = BasicTextEdit(read_only=True)
        self.process = QProcess(self)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.outputView)
        
        self.setLayout(mainLayout)
        
        sbctl.link_terminal(stdout=self.handle_stdout, stderr=self.handle_stderr)
    
    async def secure_boot(self) -> bool:
        if not await sbctl.is_installed():
            pswdPopup = BasicMessageBox(
                self,
                "Sudo password to install sbctl",
                font=cnsts.Gui.Fonts.MessageBox,
                is_input=True,
                hide_input=True
            )
            exitCode = pswdPopup.exec()
            if exitCode == BasicMessageBox.ExitCodes.UserClosed:
                self.outputView.append("User closed password request.")
            elif exitCode:
                pswd = pswdPopup.getInput().strip()
                await sbctl.install(sudo=pswd)
            
    def handle_stdout(self) -> None:
        data = self.process.readAllStandardOutput().data().decode().strip()
        self.outputView.append(data)
    
    def handle_stderr(self) -> None:
        data = self.process.readAllStandardError().data().decode().strip()
        self.outputView.append(data)
        
        
        