from fastapi import FastAPI

app = FastAPI()

# Define a simple route that returns "Hello, world!"
@app.get("/")
async def root():
    return {"message": "Hello, world!"}
