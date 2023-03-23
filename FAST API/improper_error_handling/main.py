from fastapi import FastAPI, status, Request
import traceback
import sys

app = FastAPI()

@app.get("/file")
def read_file(request: Request):

    file = request.query_params['name']
    try:
        f = open(file, "r")
        return f
        
    except Exception as e:
        
         print(traceback.print_exception(*sys.exc_info()))
        

   
   
