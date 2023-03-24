from fastapi import FastAPI, status, Request
import json


app = FastAPI()

@app.get("/data")
def read_file(request: Request):
    json_data = request.query_params['json']
    try:
        json.loads(json_data)
    except ValueError as e:
        return "Invalid Json Data"
    return "Valid Json Data"

