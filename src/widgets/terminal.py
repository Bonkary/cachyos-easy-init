from PySide6.QtCore import QProcess, QThreadPool
from PySide6.QtWidgets import QWidget, QInputDialog
from .basics import *
import linux_sbctl.sbctl as sbctl
import sys

class InternalTerminal(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        
        self.outputView = BasicTextEdit(read_only=True, font=cnsts.Gui.Fonts.Terminal)
        self.setFont(cnsts.Gui.Fonts.Terminal)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.outputView)
        
        self.setLayout(mainLayout)
    
    def secure_boot(self) -> bool:
        self.print("Checking for sbctl installation...")
        sbctlVer = sbctl.is_installed()
        if sbctlVer:
            self.outputView.append(f"Found {sbctlVer}")
        else:
            if self.confirm("'sbctl' need to be installed. Is that cool?"):
                pswd = self.pswd_for_install(install='sbctl')
                # sbctl.install(sudo_pswd=pswd)
    
    def print(self, data: str) -> None:
        self.outputView.append(">  "+data)
    
    def handle_stdout(self, data: str) -> None:
        self.outputView.append(data)
    
    def handle_stderr(self, data: str) -> None:
        self.outputView.append(data)
        
    def confirm(self, question: str) -> bool:
        popup = BasicMessageBox(
            self,
            question,
            font=cnsts.Gui.Fonts.MessageBox,
            is_confirm=True
        )
        exitCode = popup.exec()
        popup.deleteLater()
        if exitCode == BasicMessageBox.ExitCodes.Yes:
            return True
        else:
            return False
        
    def pswd_for_install(self, install: str | list[str]) -> bool:
        pswdPopup = BasicMessageBox(
            self,
            f"Sudo password to install {install}",
            font=cnsts.Gui.Fonts.MessageBox,
            is_input=True,
            hide_input=True
        )
        exitCode = pswdPopup.exec()
        if exitCode == BasicMessageBox.ExitCodes.UserClosed:
            self.outputView.append(">  User closed password request.")
        elif exitCode:
            pswd = pswdPopup.getInput().strip()
        
        return pswd
    