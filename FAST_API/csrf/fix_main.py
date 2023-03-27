from fastapi import FastAPI, status, Request, Form, Depends

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
from pydantic import BaseModel
from fastapi_csrf_protect import CsrfProtect
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
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

class CsrfSettings(BaseModel):
  secret_key:str = 'asecrettoeverybody'

@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()
 
#Initialise CSRF
csrf_protect = CsrfProtect(app)

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
async def read(request: Request, csrf_token = Depends(csrf_protect)):
    return templates.TemplateResponse("upload.html", {"request": request,'csrf_token': csrf_token})    
    

@app.post("/blog", status_code=status.HTTP_201_CREATED)
#Depends will check if csrf is valid
def create_todo(request: ToDoRequest, csrf_token: str =Depends(csrf_protect)):

    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()

    content= request.content
    project = [content]
    sql = ''' INSERT INTO blog( content)
              VALUES(?) '''
    cursor.execute(sql, project)
    conn.commit()

    return content





