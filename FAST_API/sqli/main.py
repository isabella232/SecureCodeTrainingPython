from fastapi import FastAPI, status, Request
from pydantic import BaseModel

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

    conn.commit()
    conn.close()
    return "Ready for SQL Injection?"


@app.get("/todo/{id}/{user_id}")
def read_todo(id, user_id ):

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
