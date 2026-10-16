import shlex
import subprocess


def run_command(command: list[str] | str,
                sudo_password: str | None = None,
                **kwargs) -> subprocess.CompletedProcess:
    
    runArgs = shlex.split(command) if isinstance(command, str) else command
    runInput = kwargs.pop("input", None)
    if sudo_password is not None:
        runArgs = ["sudo", "-S", "--", *runArgs]
        runInput = f"{sudo_password}\n{runInput or ''}"

    kwargs.setdefault("capture_output", True)
    kwargs.setdefault("text", True)
    if runInput is not None or sudo_password is not None:
        kwargs["input"] = runInput

    return subprocess.run(runArgs, **kwargs)