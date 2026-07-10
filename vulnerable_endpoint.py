import os
import subprocess
from fastapi import FastAPI, Request

app = FastAPI()
BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "files"))

ALLOWED_COMMANDS = {
    "list": ["ls"],
    "pwd": ["pwd"],
}

@app.get("/run")
def run_command(cmd: str):
    # CWE-78: OS Command Injection - fixed by allowlisting and avoiding shell=True
    if cmd not in ALLOWED_COMMANDS:
        return {"error": "Unsupported command"}
    result = subprocess.call(ALLOWED_COMMANDS[cmd])
    return {"exit_code": result}

def _safe_resolve_path(user_path: str) -> str:
    base = os.path.realpath(BASE_DIR)
    if os.path.isabs(user_path):
        raise ValueError("Invalid path")
    resolved = os.path.realpath(os.path.join(base, user_path))
    if not (resolved == base or resolved.startswith(base + os.sep)):
        raise ValueError("Invalid path")
    return resolved

@app.get("/read")
def read_file(path: str):
    # CWE-22: Path Traversal - validate and constrain to BASE_DIR
    return 'Disabled'

SECRET_KEY = "super_secret_password_123"  # CWE-798: Hardcoded Credentials
