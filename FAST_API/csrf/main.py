from fastapi import FastAPI, status, Request, Form

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
import os
import sqlite3
from pydantic import BaseModel


#pip install fastapi-csrf-protect


# Create ToDoRequest Base Model
class ToDoRequest(BaseModel):
    content: str
    

# Initialize app
app = FastAPI()

app.mount("/storage", StaticFiles(directory="./"), name="public")

#
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    drop = """DROP TABLE IF EXISTS todos"""
    cursor.execute(drop)

    table ="""CREATE TABLE IF NOT EXISTS blog(ID INTEGER PRIMARY KEY AUTOINCREMENT, CONTENT VARCHAR(255));"""
    cursor.execute(table)

    return "CSRF"


@app.get("/blog", response_class=HTMLResponse)
async def read(request: Request):
    
    return templates.TemplateResponse("upload.html", {"request": request})    



    

@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_todo(content: str = Form(...)):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    project = [content]
    sql = ''' INSERT INTO blog( content)
              VALUES(?) '''
    cursor.execute(sql, project)
    conn.commit()

    return content




