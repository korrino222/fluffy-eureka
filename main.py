from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello():
    return "World!!!"


@app.get("/health")
def health():
    return "OK"

