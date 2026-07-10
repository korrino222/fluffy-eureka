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

@app.get("/read")
def read_file(path: str):
    # CWE-22: Path Traversal (fixed by constraining to BASE_DIR)
    full_path = os.path.realpath(os.path.join(BASE_DIR, path))
    if os.path.commonpath([BASE_DIR, full_path]) != BASE_DIR:
        raise ValueError("Invalid path")
    with open(full_path, "r") as f:
        return {"content": f.read()}

SECRET_KEY = "super_secret_password_123"  # CWE-798: Hardcoded Credentials