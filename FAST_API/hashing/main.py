from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import sqlite3




# assign templates
templates = Jinja2Templates(directory="templates")

# Create FAST API app
app = FastAPI()

# Create SQLITE db
conn = sqlite3.connect("database.db", check_same_thread=False)

# Create tables and default credentials
c = conn.cursor()
c.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0
    )
    """
)
c.execute("""INSERT OR IGNORE INTO users(username, password, is_admin) VALUES ("user","user",0)""")
c.execute("""INSERT OR IGNORE INTO users(username, password, is_admin) VALUES ("admin","admin",1)""")
conn.commit()
c.close()


#Defice middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Define a function to verify user credentials
def verify_user(username: str, password: str):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username,password,))
    user = c.fetchone()
    c.close()
    if user:
        return user

# Define a dependency to get the current user from the session
def get_current_user(request: Request):
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    c.close()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# Define a decorator to check if a user is an admin
def is_admin(username):
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    c.close()
    if result and result[0] == 1:
        return True
    else:
        return False

# Serve static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define a route to display the login page
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define a route to handle form submission
@app.post("/login")
async def login(request: Request,  username: str = Form(...), password: str = Form(...)):
    user = verify_user(username, password)
    if user:
        request.session["username"] = user[1]
        request.session["admin"]=user[3]
        return templates.TemplateResponse("home.html", {"request":request, "id": user[1], "admin": user[3]})
    else:
        return templates.TemplateResponse("failure.html", {"request": request, "error": "Invalid username or password"})

@app.get("/register", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register",response_class=HTMLResponse)
async def create_user(request: Request, username: str = Form(...), password: str = Form(...), is_admin: str = Form(...)):
    # Insert the new user into the database
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, password, is_admin))
    conn.commit()
    c.close()

    # Redirect the user back to the user administration page
    return templates.TemplateResponse("register_success.html", {"request": request})

@app.get("/logout", response_class= HTMLResponse)
async def logout(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/resetpassword", response_class=HTMLResponse)
async def resetpage(request: Request):
    return templates.TemplateResponse("resetpassword.html",{"request":request})

@app.get("/home", response_class=HTMLResponse)
async def resetpage(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})

@app.post("/resetpassword", response_class=HTMLResponse)
async def resetpassword(request: Request, username: str = Form(...), oldpassword: str = Form(...), newpassword: str = Form(...)):
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE id = ? ",(newpassword, username))
    conn.commit()
    c. close()
    return templates.TemplateResponse("reset_success.html", {"request": request})


# Define a route to display the user administration page
@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, user=Depends(get_current_user)):
    # Check if the user is an admin
    if not is_admin(user[1]):
        raise HTTPException(status_code=403, detail="Forbidden")
    # Retrieve all users from the database
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    c.close()
    # Render the user administration page
    return templates.TemplateResponse("admin.html",{"request": request, "users": users} )

# Define a route to handle user creation
@app.post("/admin/create",response_class=HTMLResponse)
async def create_user(request: Request, username: str = Form(...), password: str = Form(...), is_admin: str = Form(...)):
    # Insert the new user into the database
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, password, is_admin))
    conn.commit()
    c.execute("SELECT id from users WHERE username=?", (username,))
    id= c.fetchone()
    c.close()
    # Redirect the user back to the user administration page
    return templates.TemplateResponse("create_user.html", {"request": request, "id": id, "username": username})

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
