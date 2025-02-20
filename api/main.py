from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def connect():
    return {"msg": "connection successful"}
