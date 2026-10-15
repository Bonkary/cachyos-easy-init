import subprocess
import os
import sys
import git
from getpass import getpass
import stat
import tempfile

HERMES_HOME_DIR = os.path.join('/home', os.environ["USER"], '.hermes')
HERMES_DIR = os.path.join(HERMES_HOME_DIR, 'Hermes')
HERMES_URL = 'https://github.com/MrOz59/Hermes.git'

HERMES_KMS_DIR = os.path.join(HERMES_HOME_DIR, 'Hermes-KMS')
HERMES_KMS_URL = 'https://github.com/MrOz59/Hermes-KMS.git'

class ProgressPrinter(git.RemoteProgress):

    def update(self, op_code, cur_count, max_count=None, message=""):
        lines = (
            f"OP Code: {op_code}",
            f"Current: {cur_count}",
            f"Total: {max_count}",
            f"Message: {message}",
        )
        if getattr(self, "_started", False):
            sys.stdout.write(f"\033[{len(lines)}A")
        for line in lines:
            sys.stdout.write(f"\r\033[K{line}\n")
        sys.stdout.flush()
        self._started = True

def cmd_line(cmd: list[str] | str,
             capture: bool = True,
             input: str | None = None,
             cwd: str | None = None,
             env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    if type(cmd) == str:
        cmd = cmd.split(" ")
    
    result = subprocess.run(
        cmd,
        capture_output=capture,
        text=True,
        input=input,
        timeout=60,
        shell=True,
        cwd=cwd,
        env=env
    )
    
    return result

def download() -> bool:
    downloaded = False
    try:
        if not os.path.exists(HERMES_HOME_DIR):
            os.makedirs(HERMES_HOME_DIR, exist_ok=True)
        
        if not os.path.exists(HERMES_DIR):
            print("Downloading Hermes...")
            hermesRepo = git.Repo.clone_from(HERMES_URL, HERMES_DIR,
                                             progress=ProgressPrinter())
            print()
            if not os.path.exists(HERMES_DIR):
                print("Failed to clone Hermes dir")
        else:
            print("Hermes already downloaded.")
        
        if not os.path.exists(HERMES_KMS_DIR):
            print("Downloading Hermes-KMS")
            hermesKmsRepo = git.Repo.clone_from(HERMES_KMS_URL, HERMES_KMS_DIR,
                                                progress=ProgressPrinter())
            print()
            if not os.path.exists(HERMES_KMS_DIR):
                print("Failed to clone Hermes-KMS dir")
        else:
            print("Hermes-KMS already downloaded.")
        
        if os.path.exists(HERMES_DIR) and os.path.exists(HERMES_KMS_DIR):
            downloaded = True
        
        return downloaded
    
    except Exception as err:
        print(err)

def install_kms(password: str) -> None:
    if not is_installed():
        if not os.path.exists(HERMES_HOME_DIR):
            os.makedirs(HERMES_HOME_DIR, exist_ok=True)
        
        makeClean = subprocess.run(
            "make clean",
            capture_output=True,
            text=True,
            timeout=60,
            shell=True,
            cwd=HERMES_KMS_DIR,
        )
        if makeClean.stderr:
            print(f"Failed to make clean: {makeClean.stderr}")
        
        make = subprocess.run(
            "make",
            capture_output=True,
            text=True,
            timeout=60,
            shell=True,
            cwd=HERMES_KMS_DIR,
        )
        if make.stderr:
            print(f"Failed to make: {make.stderr}")
        
        with tempfile.TemporaryDirectory() as helper_dir:
            askpass = os.path.join(helper_dir, "askpass")
            sudo_wrapper = os.path.join(helper_dir, "sudo")
            with open(askpass, "w") as helper:
                helper.write('#!/bin/sh\nprintf "%s\\n" "$HERMES_SUDO_PASSWORD"\n')
            with open(sudo_wrapper, "w") as helper:
                helper.write('#!/bin/sh\nexec /usr/bin/sudo -A "$@"\n')
            os.chmod(askpass, stat.S_IRWXU)
            os.chmod(sudo_wrapper, stat.S_IRWXU)

            env = os.environ.copy()
            env["HERMES_SUDO_PASSWORD"] = password
            env["SUDO_ASKPASS"] = askpass
            env["PATH"] = helper_dir + os.pathsep + env.get("PATH", "")
            makepkg = subprocess.run(
                "makepkg -si -f --noconfirm",
                shell=True,
                cwd=HERMES_KMS_DIR,
                env=env,
            )
        if makepkg.returncode == 0:
            print("Time to reboot!")
            return True
        else:
            print(f"Failed to makepkg (exit code {makepkg.returncode}).")
            return False
    else:
        print("Hermes-KMS already installed.")
        return True
    
def is_installed() -> bool:
    installed = False
    lsmodOutput = cmd_line("lsmod | grep hermes_kms", capture=True)
    if not lsmodOutput.stdout:
        print("Failed to install KMS")
    
    lsOutput = cmd_line("ls /dev/dri/by-path/ | grep hermes")
    if not lsOutput.stdout:
        print("Failed to install KMS")
    
    return installed