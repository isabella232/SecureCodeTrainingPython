from fastapi import FastAPI, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
import os
import re
import sqlite3

from pydantic import BaseModel

# Create ToDoRequest Base Model
class ToDoRequest(BaseModel):
    task: str
    user_id: int

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    drop = """DROP TABLE IF EXISTS todos"""
    cursor.execute(drop)

    table ="""CREATE TABLE IF NOT EXISTS todos(ID INTEGER PRIMARY KEY AUTOINCREMENT,USER_ID INTEGER(12), TASK VARCHAR(255));"""
    cursor.execute(table)

    task = "<script>alert(1)</script>"
    
    project = [2,1,]

    sql = ''' INSERT INTO todos(id,user_id,task)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()

    conn.close()
    return "Ready for XSS"
    
@app.get("/todo/{id}", response_class=HTMLResponse)
def read_todo(request: Request,id  ):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    #raw_sql = "SELECT * FROM todos WHERE user_id = "+user_id+" AND id = "+id

    query = """SELECT * FROM todos WHERE id = ?"""
    tuple1 = (id)
    todo = cursor.execute(query, tuple1).fetchmany()

    #todo = cursor.execute(raw_sql).fetchmany()

    return f"task: {todo}"

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    project = [todo.user_id, todo.task.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')]
    sql = ''' INSERT INTO todos(user_id, task)
              VALUES(?,?) '''
    cursor.execute(sql, project)
    conn.commit()

    return todo




