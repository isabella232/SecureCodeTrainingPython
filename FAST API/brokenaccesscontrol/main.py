from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Serve static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the HTML login page
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Handle login requests
@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "user" and password == "password":
        return templates.TemplateResponse("success.html", {"request": request})
    else:
        return templates.TemplateResponse("failure.html", {"request": request})
