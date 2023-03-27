from fastapi import FastAPI, status, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
import uuid
import sqlite3

# Initialize app
app = FastAPI()

app.mount("/storage", StaticFiles(directory="./"), name="public")


templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()
    cursor.execute("""ALTER TABLE image 
    ADD COLUMN uuid [VARCHAR];""")

    return "Upload Vulnerability"



@app.post("/upload")
def upload(uploadfile: UploadFile = File(...)):
    try:
        contents = uploadfile.file.read()
        fileguid = str(uuid.uuid4())
        with open(uploadfile.filename, 'wb') as f:
            f.write(contents)

        conn = sqlite3.connect('tutorial.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO image( uuid, name, user) VALUES(?,?,?)", (fileguid,uploadfile.filename, 1,))
        conn.commit()
    
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        uploadfile.file.close()

    return {"message": f"Successfully uploaded {uploadfile.filename} with uuid {fileguid}"}

@app.get("/upload", response_class=HTMLResponse)
async def read(request: Request):
    
    return templates.TemplateResponse("upload.html", {"request": request})  

@app.get("/file/{user_id}/{id}")
def read_todo(user_id: int, id: str):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    query = """SELECT * FROM image WHERE user = ? AND  uuid = ?"""
    tuple1 = (user_id, id)
    file = cursor.execute(query, tuple1).fetchmany()

    return f"image:{file}"  


