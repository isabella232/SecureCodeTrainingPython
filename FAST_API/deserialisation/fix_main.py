import re
import json
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/data")
def read_file(request: Request):
    json_data = request.query_params['json']
    json_pattern = r'^(\s*|\{.*\}|\[.*\])$'
    if not re.match(json_pattern, json_data):
        return "Invalid Json Data"
    try:
        json.loads(json_data)
    except ValueError as e:
        return "Invalid Json Data"
    return "Valid Json Data"
