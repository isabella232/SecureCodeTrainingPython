from fastapi import FastAPI, status, Request
import subprocess
import os


app = FastAPI()

@app.get("/ping")
def read_file(request: Request):
    ipaddress = request.query_params['name']
    proc = subprocess.Popen("ping -c 3 "+ipaddress, stdout=subprocess.PIPE, shell=True)

    stdout, stderr = proc.communicate()
    if proc.returncode == 0:
        print('{} is UP'.format(ipaddress))
        print('ping output:')
        return stdout.decode('ASCII')

