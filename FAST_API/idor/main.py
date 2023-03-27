from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
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

    drop = """DROP TABLE IF EXISTS image"""
    cursor.execute(drop)

    table ="""CREATE TABLE IF NOT EXISTS image(ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME VARCHAR(255), USER INTEGER NOT NULL);"""
    cursor.execute(table)

    return "IDOR"




@app.post("/upload")
def upload(uploadfile: UploadFile = File(...)):
   

    try:
        contents = uploadfile.file.read()
    
        with open(uploadfile.filename, 'wb') as f:
            f.write(contents)

        ##save filename to db    
        conn = sqlite3.connect('tutorial.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO image( name, user) VALUES(?,?)", (uploadfile.filename, 1,))
        conn.commit()    
        
    
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        uploadfile.file.close()

    return {"message": f"Successfully uploaded {uploadfile.filename}"}

@app.get("/upload", response_class=HTMLResponse)
async def read(request: Request):
    
    return templates.TemplateResponse("upload.html", {"request": request})    

@app.get("/file/{id}")
def read_todo(id ):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    query = """SELECT * FROM image WHERE id = ?"""
    file = cursor.execute(query, id).fetchmany()

    return file
