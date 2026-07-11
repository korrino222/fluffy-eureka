import subprocess
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/run")
def run_command(cmd: str):
    # CWE-78: OS Command Injection
    result = subprocess.call(cmd, shell=True)
    return {"exit_code": result}

@app.get("/read")
def read_file(path: str):
    # CWE-22: Path Traversal
    with open(path, "r") as f:
        return {"content": f.read()}

SECRET_KEY = "super_secret_password_123"  # CWE-798: Hardcoded Credentials
