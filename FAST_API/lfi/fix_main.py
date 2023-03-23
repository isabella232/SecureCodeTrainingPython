from fastapi import FastAPI, status, Request

app = FastAPI()

allow_files = ["home","contact"]

@app.get("/file")
def read_file(request: Request):
   file = request.query_params['name']
   if file in allow_files:
      
        f = open(file, "r")
        return f.read()
   else:
       return "File not found"
   
