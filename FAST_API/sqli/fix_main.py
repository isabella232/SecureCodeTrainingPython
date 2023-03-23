from fastapi import FastAPI, status, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text,select
import sqlite3


# Create ToDoRequest Base Model
class ToDoRequest(BaseModel):
    task: str
    user_id: int

# Initialize app
app = FastAPI()


@app.get("/")
def root():
    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    drop = """DROP TABLE IF EXISTS todos"""
    cursor.execute(drop)

    table ="""CREATE TABLE IF NOT EXISTS todos(ID INTEGER PRIMARY KEY AUTOINCREMENT,USER_ID INTEGER(12), TASK VARCHAR(255));"""
    cursor.execute(table)

    cursor.execute('''INSERT INTO todos VALUES (1,1, 'test1')''')
    cursor.execute('''INSERT INTO todos VALUES (2,1, 'test2')''')
    
    conn.commit()
    conn.close()
    return "Ready for SQL Injection?"

@app.get("/todo/{id}/{user_id}")
def read_todo(id : int, user_id : int):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    raw_sql = "SELECT * FROM todos WHERE user_id = "+user_id+" AND id = "+id


    todo = cursor.execute(raw_sql).fetchmany()

    return todo

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    project = [todo.user_id, todo.task]
    sql = ''' INSERT INTO todos(user_id, task)
              VALUES(?,?) '''
    cursor.execute(sql, project)
    conn.commit()

    return todo



