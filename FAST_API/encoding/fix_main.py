from fastapi import FastAPI, status, Request
from pydantic import BaseModel

import sqlite3
import base64
import re

# Create ToDoRequest Base Model
class ToDoRequest(BaseModel):
    email: str

# Initialize app
app = FastAPI()


@app.get("/")
def root():
    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    drop = """DROP TABLE IF EXISTS employee"""
    cursor.execute(drop)

    table ="""CREATE TABLE IF NOT EXISTS employee(ID INTEGER PRIMARY KEY AUTOINCREMENT,EMAIL VARCHAR(255));"""
    cursor.execute(table)

   

    return "ENCODING"


@app.get("/email")
def read_todo(request: Request ):

    encoded = request.query_params['encode']
    
    decode = encoded
   
    #return base_enc
    if re.match('^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$',decode):
        return base64.b64decode(decode).decode('utf-8')
    else:
        return "not valid"
    #return base64.b64decode(todo[0]).decode('utf-8')
    


@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()
    
    project = [base64.b64encode(todo.email.encode('utf-8'))]
    sql = ''' INSERT INTO employee(email)
              VALUES(?) '''
    cursor.execute(sql, project)
    conn.commit()

    return base64.b64encode(todo.email.encode('utf-8'))




