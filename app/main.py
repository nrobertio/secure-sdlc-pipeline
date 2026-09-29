# Small FastAPI service used as the scan target for the DevSecOps pipeline.
from fastapi import FastAPI

app = FastAPI(title="secure-sdlc-sample", version="0.1.0")


@app.get("/")
def root():
    return {"service": "secure-sdlc-sample", "status": "ok"}


@app.get("/healthz")
def healthz():
    return {"status": "healthy"}


@app.get("/greet/{name}")
def greet(name: str):
    # Return value is JSON-encoded by FastAPI, which avoids injection in the response.
    return {"message": "hello " + name}
