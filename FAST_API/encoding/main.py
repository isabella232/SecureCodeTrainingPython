from fastapi import FastAPI, status, Request
from pydantic import BaseModel

import sqlite3


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

    cursor.execute('''INSERT INTO employee VALUES (1, 'test@test.com')''')

    
    conn.commit()
    conn.close()
    return "ENCODING"


@app.get("/email/{id}")
def read_todo(id ):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    raw_sql = "SELECT * FROM employee WHERE id = "+id


    todo = cursor.execute(raw_sql).fetchmany()

    return todo

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    project = [todo.email]
    sql = ''' INSERT INTO employee(email)
              VALUES(?) '''
    cursor.execute(sql, project)
    conn.commit()

    return todo



