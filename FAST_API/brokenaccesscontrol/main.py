from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

#assign templates
templates = Jinja2Templates(directory="templates")

#Create FAST API app
app = FastAPI()

#Create SQLITE db 
conn = sqlite3.connect("database.db", check_same_thread=False)

#Create tables
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0
    )
""")
conn.commit()
c.close()

# Serve static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define a route to display the login page
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define a route to handle form submission
@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Check if the username and password match a user in the database
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    c.close()

    # If a matching user is found, redirect to the home page
    if user:
        return templates.TemplateResponse("home.html", {"request": request, "username": username})
    # If a matching user is not found, display an error message
    else:
        return templates.TemplateResponse("failure.html", {"request": request, "error": "Invalid username or password"})

@app.get("/home", response_class=HTMLResponse)
async def resetpage(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})

# Define a route to display the user administration page
@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    # Retrieve all users from the database
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    c.close()

    # Render the user administration page
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "users": users}
    )

# Define a route to handle user creation
@app.post("/admin/create",response_class=HTMLResponse)
async def create_user(request: Request, username: str = Form(...), password: str = Form(...), is_admin: int = Form(...)):
    # Insert the new user into the database
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, password, is_admin))
    conn.commit()
    c.close()

    # Redirect the user back to the user administration page
    return templates.TemplateResponse("create_user.html", {"request": request})

# Define a route to handle user deletion
@app.post("/admin/delete",response_class=HTMLResponse)
async def delete_user(request: Request, id: int= Form(...)):
    # Delete the user from the database
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    c.close()

    # Redirect the user back to the user administration page
    return templates.TemplateResponse("delete_user.html", {"request": request, "id": id})