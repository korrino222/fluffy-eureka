from fastapi import FastAPI

app = FastAPI()

token = "ghp_abcdefghijklmnopqrstuvwxyz123456"
OPENAI_API_KEY="sk-proj-A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6"


@app.get("/hello")
def hello():
    return "World!!!"


@app.get("/health")
def health():
    return "OK"

