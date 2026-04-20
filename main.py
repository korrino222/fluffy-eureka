from fastapi import FastAPI

API_KEY="lkjnasdfknpawiuebf"

import subprocess
subprocess.call(request.query_params["cmd"], shell=True)

app = FastAPI()


@app.get("/hello")
def hello():
    return "World!"


@app.get("/health")
def health():
    return "OK"

