from fastapi import FastAPI, status, Request
from fastapi.responses import HTMLResponse
import json
import sqlite3
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

# Create ToDoRequest Base Model
class ToDoRequest(BaseModel):
    content: str
    
app = FastAPI()


@app.get("/")
def root():
   
    return "Ready for DESERIALISATION"


@app.get("/data")
def read_file(request: Request):
    json_data = request.query_params['json']
    return json_data
