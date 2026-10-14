from PySide6.QtWidgets import QWidget, QApplication, QTextBrowser
from PySide6.QtCore import QThreadPool, QTimer, QUrl
import constants as cnsts
from widgets.basics import *
from linux_sbctl import sbctl
import os
import subprocess
import sys
from pathlib import Path

class SecureBoot(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        
        self.stage = self.get_stage()
        buttonWidth = 200
        
        self.markdownBox = BasicMarkdown(file=cnsts.Files.Markdown.SecureBoot.Start,
                                         size=QSize(cnsts.Gui.Sizes.AppSize))
        print(Path(__file__).parent)
        
        # self.installButton = BasicPushButton("Install sbctl", width=buttonWidth)
        self.nextButton = BasicPushButton("Next", width=buttonWidth)
        
        mainLayout = BasicVBoxLayout()
        mainLayout.addSpacing(20)
        mainLayout.addWidget(self.markdownBox, alignment=Qt.AlignmentFlag.AlignCenter)
        mainLayout.addSpacing(50)
        # mainLayout.addWidget(self.installButton, alignment=Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.nextButton, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.nextButton.hide()
        self.setLayout(mainLayout)
        
        # self.installButton.clicked.connect(self.install)
        self.nextButton.clicked.connect(self.next_stage)
        
        self.next_stage()
            
    def install(self) -> None:
        self.ask_grub()
        self.installButton.hide()
        
        if not sbctl.is_installed():
            pswd = self.request_pswd(to_install="sbctl")
            QApplication.processEvents()
            if not sbctl.install(sudo_pswd=pswd):
                pass
            else:
                self.next_stage()
        else:
            self.next_stage()
        self.nextButton.show()
        
    def request_pswd(self) -> bool:
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
    
    def get_stage(self) -> int:
        if not os.path.exists(cnsts.Files.Tmp.SecureBoot):
            stage = 0
            with open(cnsts.Files.Tmp.SecureBoot, 'w') as log:
                log.write('0')
        else:
            with open(cnsts.Files.Tmp.SecureBoot, 'r') as log:
                stage = log.read()
                if not stage:
                    stage = 0
                elif stage.isdigit():
                    stage = int(stage)
        return stage
    
    def next_stage(self) -> None:
        self.stage += 1
        with open(cnsts.Files.Tmp.SecureBoot, 'w') as log:
            log.write(str(self.stage))
        
        self.nextButton.hide()
        match self.stage:
            case 0:
                sbctl.install()
            case 1:
                # self.label.setText("Take a look at the terminal you booted me from. Maybe resize if need be.\n\nTake a picture probably or something.")
                QApplication.processEvents()
                QTimer.singleShot(5000, lambda: sys.exit(0))
                # subprocess.run(['./secure_boot_msg.sh'])
            case 2:
                pass
            case 3:
                pass
    
    def ask_grub(self) -> bool:
        popup = BasicMessageBox(
            self,
            "Are you using Grub as your boot manager?",
            font=cnsts.Gui.Fonts.MessageBox,
            is_confirm=True
        )
        exitCode = popup.exec()
        if exitCode == BasicMessageBox.ExitCodes.Yes:
            sbctl.grub()