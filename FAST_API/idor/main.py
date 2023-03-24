from fastapi import FastAPI, status, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
import os
import sqlite3

# Initialize app
app = FastAPI()

app.mount("/storage", StaticFiles(directory="./"), name="public")


templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    drop = """DROP TABLE IF EXISTS todos"""
    cursor.execute(drop)

    table ="""CREATE TABLE IF NOT EXISTS image(ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME VARCHAR(255));"""
    cursor.execute(table)

    return "IDOR"




@app.post("/upload")
def upload(file: UploadFile = File(...)):
   

    try:
        contents = file.file.read()
    
        with open(file.filename, 'wb') as f:
            f.write(contents)

        ##save filename to db    
        conn = sqlite3.connect('tutorial.db')
        cursor = conn.cursor()

        project = [file.filename]
        sql = ''' INSERT INTO image( name)
                VALUES(?) '''
        cursor.execute(sql, project)
        conn.commit()    
        
    
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

@app.get("/upload", response_class=HTMLResponse)
async def read(request: Request):
    
    return templates.TemplateResponse("upload.html", {"request": request})    

@app.get("/file/{id}")
def read_todo(id ):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    #raw_sql = "SELECT * FROM todos WHERE user_id = "+user_id+" AND id = "+id

    query = """SELECT * FROM image WHERE id = ?"""
    tuple1 = (id)
    todo = cursor.execute(query, tuple1).fetchmany()

    #todo = cursor.execute(raw_sql).fetchmany()

    return todo
