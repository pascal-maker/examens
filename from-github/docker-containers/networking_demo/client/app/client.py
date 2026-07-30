from fastapi import FastAPI
from typing import List
import requests


app = FastAPI(title="Client demonstration")

@app.get("/")
def root():
    return {"message":"Hello World from the Client."}

@app.get("/api")
def doAPIRequest(path: str):
    print(path)
    response = requests.get(path)
    return response.json()