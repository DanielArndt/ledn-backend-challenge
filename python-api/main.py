from fastapi import FastAPI
import motor.motor_asyncio
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
