from dataclasses import dataclass
import subprocess
import os
import constants as cnsts

type Blake2BSum = str

def cmd_line(cmd: list[str] | str, capture: bool = True, input: str | None = None, terminal: bool = False) -> subprocess.CompletedProcess:
    if type(cmd) == str:
        cmd = cmd.split(" ")

    result = subprocess.run(cmd, capture_output=capture, text=True, input=input, timeout=60)

    if result:
        return result.stdout
    else:
        return None

