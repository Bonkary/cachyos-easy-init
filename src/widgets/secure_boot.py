from PySide6.QtWidgets import QWidget, QApplication, QTextBrowser
from PySide6.QtCore import QThreadPool, QTimer, QUrl, QThreadPool, QRunnable
import constants as cnsts
from widgets.basics import *
from linux_sbctl import sbctl
import os
import subprocess
import sys
from pathlib import Path
from exceptions import *
import time


@dataclass
class Stages:
    Start = 'start'
    Install = 'install'
    WindowsBoot = 'windowsboot'
    SetupMode = 'setupmode'
    Completed = 'completed'

type Stage = str

class Stage():
    Start = 'start'
    Install = 'install'
    WindowsBoot = 'windowsboot'
    SetupMode = 'setupmode'
    Completed = 'completed'
    def __init__(self):
        if not os.path.exists(cnsts.Files.Tmp.SecureBoot):
            with open(cnsts.Files.Tmp.SecureBoot, 'w') as tmp:
                tmp.write(Stage.Start)
        self.file = Path(cnsts.Files.Tmp.SecureBoot).resolve()
        self.current = self.file.read_text()
    
    # def current(self) -> str:
    #     return self.file.read_text()
    
    def update(self, stage: Stage) -> None:
        print(f"Current stage: {self.current}")
        print(f"New Stage: {stage}\n")
        self.file.write_text(stage)
        self.current = stage

class Rebooter(QRunnable):
    def __init__(self):
        pass

class SecureBoot(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        
        self.stage = Stage()
        buttonWidth = 200
        
        self.markdownBox = BasicMarkdown(file=cnsts.Files.Markdown.SecureBoot.Start,
                                         size=QSize(cnsts.Gui.Sizes.SecureBootSize))
        
        self.nextButton = BasicPushButton("Next")
        
        self.rebootButton = BasicPushButton("Reboot")
        self.rebootLaterButton = BasicPushButton("Reboot Later")
        
        self.asusSelect = BasicPushButton("ASUS")
        self.msiSelect = BasicPushButton("MSI")
        self.neitherSelect = BasicPushButton("Neither")
        
        buttonSpacing = 20
        self.rebootWidget = QWidget(self)
        rebootLayout = BasicHBoxLayout()
        rebootLayout.addStretch()
        rebootLayout.addWidget(self.rebootButton)
        rebootLayout.addSpacing(buttonSpacing)
        rebootLayout.addWidget(self.rebootLaterButton)
        rebootLayout.addStretch()
        self.rebootWidget.setLayout(rebootLayout)
        
        self.selectMoboWidget = QWidget(self)
        selectMoboLayout = BasicHBoxLayout()
        selectMoboLayout.addStretch()
        selectMoboLayout.addWidget(self.asusSelect)
        selectMoboLayout.addSpacing(buttonSpacing)
        selectMoboLayout.addWidget(self.msiSelect)
        selectMoboLayout.addSpacing(buttonSpacing)
        selectMoboLayout.addWidget(self.neitherSelect)
        selectMoboLayout.addStretch()
        self.selectMoboWidget.setLayout(selectMoboLayout)
        
        
        
        mainLayout = BasicVBoxLayout()
        mainLayout.addSpacing(20)
        mainLayout.addWidget(self.markdownBox, alignment=Qt.AlignmentFlag.AlignCenter)
        mainLayout.addSpacing(50)
        mainLayout.addWidget(self.nextButton, alignment=Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.selectMoboWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(self.rebootWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.rebootWidget.hide()
        self.selectMoboWidget.hide()
        
        self.setLayout(mainLayout)
        
        self.nextButton.clicked.connect(self.set_stage)
        self.asusSelect.clicked.connect(lambda: self.select_mobo('asus'))
        self.msiSelect.clicked.connect(lambda: self.select_mobo('msi'))
        self.neitherSelect.clicked.connect(lambda: self.select_mobo('standard'))
        
    def install_sbctl(self) -> bool:
        if not sbctl.is_installed():
            pswd = self.request_pswd(to_install="sbctl")
            
            if sbctl.install(sudo_pswd=pswd):
                self.stage.update(Stages.WindowsBoot)
            else:
                raise FailedPackageInstall("sbctl")
            
        else:
            self.set_stage()
        
    def request_pswd(self) -> str:
        pswdPopup = BasicMessageBox(
            self,
            f"Sudo password to install sbctl",
            font=cnsts.Gui.Fonts.MessageBox,
            is_input=True,
            hide_input=True
        )
        exitCode = pswdPopup.exec()
        if exitCode == BasicMessageBox.ExitCodes.Success:
            return BasicMessageBox.Cache.Input
    
    def get_stage(self) -> Stage:
        try:
            if not os.path.exists(cnsts.Files.Tmp.SecureBoot):
                stage = Stages.Start
                with open(cnsts.Files.Tmp.SecureBoot, 'w') as log:
                    log.write('0')
            else:
                with open(cnsts.Files.Tmp.SecureBoot, 'r') as log:
                    stage = log.read()
                    if not stage:
                        stage = Stages.Start
                                    
            return stage
        
        except Exception as err:
            raise GetStageError(err)
    
    def set_stage(self, stage: Stage | None = None) -> None:
        match self.stage.current:
            case Stage.Start:
                # signGrub = sbctl.sign_grub() if self.user_uses_grub() else None
                
                self.stage.update(
                    Stages.WindowsBoot if self.needs_windows_boot()
                    else Stages.SetupMode
                )
                self.set_stage(Stage.WindowsBoot)
                    
            case Stage.WindowsBoot:
                self.markdownBox.set(cnsts.Files.Markdown.SecureBoot.Windows)
                self.rebootWidget.show()
                self.nextButton.hide()
            
            case Stage.SetupMode:
                self.markdownBox.set(cnsts.Files.Markdown.SecureBoot.SetupMode)
                self.selectMoboWidget.show()
                
                self.nextButton.hide()
                
            case _:
                self.set_stage(Stage.Start)

        return self.stage
    
    def needs_windows_boot(self) -> bool:
        popup = BasicMessageBox(
            self,
            "Do you have Windows 10/11 installed?",
            font=cnsts.Gui.Fonts.MessageBox,
            is_confirm=True
        )
        exitCode = popup.exec()
        if exitCode == BasicMessageBox.ExitCodes.Yes:
            popup = BasicMessageBox(
                self,
                "Have you booted into Windows yet?",
                font=cnsts.Gui.Fonts.MessageBox,
                is_confirm=True
            )
            exitCode = popup.exec()
            if exitCode == BasicMessageBox.ExitCodes.No:
                self.stage.update(Stage.WindowsBoot)
            else:
                self.stage.update(Stage.SetupMode)
            self.set_stage()
            
        else:
            return False
        
    def user_uses_grub(self) -> bool:
        popup = BasicMessageBox(
            self,
            "Are you using Grub as your boot manager?",
            font=cnsts.Gui.Fonts.MessageBox,
            is_confirm=True
        )
        exitCode = popup.exec()
        if exitCode == BasicMessageBox.ExitCodes.Yes:
            sbctl.sign_grub()

    def select_mobo(self, mobo: str) -> None:
        match mobo:
            case 'asus':
                self.markdownBox.set(cnsts.Files.Markdown.SecureBoot.AsusSetup)
            case 'msi':
                self.markdownBox.set(cnsts.Files.Markdown.SecureBoot.MsiSetup)
            case 'standard':
                self.markdownBox.set(cnsts.Files.Markdown.SecureBoot.StandardSetup)
        self.rebootWidget.show()
