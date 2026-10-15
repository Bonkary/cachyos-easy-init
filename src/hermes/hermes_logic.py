import subprocess
import os
import sys
import git

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
             cwd: str | None = None) -> subprocess.CompletedProcess:
    if type(cmd) == str:
        cmd = cmd.split(" ")

    print(cmd)
    result = subprocess.run(args=cmd,
                            capture_output=capture,
                            text=True,
                            input=input,
                            timeout=60,
                            shell=True,
                            cwd=cwd)
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
    
def install_kms() -> bool:
    if not is_installed():
        cleanResult = cmd_line("make clean", cwd=HERMES_KMS_DIR)
        if cleanResult.stderr:
            print(f"Failed to make clean: {cleanResult.stderr}")
            
        makeResult = cmd_line("make", cwd=HERMES_KMS_DIR)
        if makeResult.stderr:
            print(f"Failed to make: {cleanResult.stderr}")
        
        pswd = input("Password: ")
        
        makepkgResult = cmd_line(f'makepkg -si --noconfirm', cwd=HERMES_KMS_DIR, input=pswd)
        if not makepkgResult:
            pass
    else:
        print("Hermes-KMS already installed.")
    
def is_installed() -> bool:
    installed = False
    lsmodOutput = cmd_line("lsmod | grep hermes_kms", capture=True)
    if not lsmodOutput.stdout:
        print("Failed to install KMS")
    
    lsOutput = cmd_line("ls /dev/dri/by-path/ | grep hermes")
    if not lsOutput.stdout:
        print("Failed to install KMS")
    
    return installed