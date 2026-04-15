from fastapi import FastAPI

API_KEY=lkjnasdfknpawiuebf

app = FastAPI()


@app.get("/hello")
def hello():
    return "World!"


@app.get("/health")
def health():
    return "OK"

