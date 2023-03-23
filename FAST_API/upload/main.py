from fastapi import FastAPI, status, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
import os


# Initialize app
app = FastAPI()

app.mount("/storage", StaticFiles(directory="./"), name="public")


templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return "Upload Vulnerability"



@app.post("/upload")
def upload(file: UploadFile = File(...)):
   

    try:
        
        contents = file.file.read()
    
        with open(file.filename, 'wb') as f:
            f.write(contents)
        
    
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

@app.get("/upload", response_class=HTMLResponse)
async def read(request: Request):
    
    return templates.TemplateResponse("upload.html", {"request": request})    


