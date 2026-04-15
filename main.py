from fastapi import FastAPI

OPENAI_API_KEY="sk-proj-abcdefghijklmnopqrstuvwxyz123456789"

app = FastAPI()


@app.get("/hello")
def hello():
    return "World!!!"


@app.get("/health")
def health():
    return "OK"

