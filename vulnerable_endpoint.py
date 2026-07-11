import shlex
import subprocess
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

ALLOWED_COMMANDS = {"ls", "whoami", "date"}

@app.get("/run")
def run_command(cmd: str):
    if cmd not in ALLOWED_COMMANDS:
        raise HTTPException(status_code=400, detail="Command not allowed")
    result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    return {"stdout": result.stdout}

SAFE_BASE = "/app/data"

@app.get("/read")
def read_file(path: str):
    full_path = os.path.realpath(os.path.join(SAFE_BASE, path))
    if not full_path.startswith(SAFE_BASE):
        raise HTTPException(status_code=400, detail="Invalid path")
    with open(full_path, "r") as f:
        return {"content": f.read()}

# Secret loaded from environment variable
SECRET_KEY = os.environ.get("SECRET_KEY", "")
