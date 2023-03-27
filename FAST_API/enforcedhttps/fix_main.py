from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import ssl

app = FastAPI()

# Add HTTPS redirection middleware
app.add_middleware(HTTPSRedirectMiddleware)

# Configure SSL/TLS
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile="./cert.pem", keyfile="./key.pem")

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
        ssl_keyfile="./key.pem",
        ssl_certfile="./cert.pem",
        ssl_version=ssl.PROTOCOL_TLS,
    )
