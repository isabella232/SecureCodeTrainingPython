from fastapi import FastAPI, status, Request

app = FastAPI()

@app.get("/file")
def read_file(request: Request):
   file = request.query_params['name']
   f = open(file, "r")
   return f.read()
