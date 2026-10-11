from dataclasses import dataclass
import subprocess
import os
import constants as cnsts

type Blake2BSum = str

def cmd_line(cmd: list[str]) -> subprocess.CompletedProcess:
    subprocess.run(cmd, capture_output=True, text=True)

@dataclass
class sbctl:
    @staticmethod
    def status() -> str:
        status = cmd_line(['sudo', 'sbctl', 'status'])
        # match status:
        #     case cnsts.sbctl.statuses.
        
    @staticmethod
    def install() -> bool:
        pass
    
    @staticmethod
    def create_keys() -> bool:
        pass
    
    @staticmethod
    def enroll_kets() -> bool:
        pass
    
    @staticmethod
    def hash() -> Blake2BSum:
        pass
    
    @staticmethod
    def hash_wallpaper() -> str:
        pass
    
    @staticmethod
    def get_progress() -> int:
        pass
    
    @staticmethod
    def is_installed() -> bool:
        cmd = ['pacman', '-Q', 'sbctl']
        if "error: package 'sbctl' was not found"
