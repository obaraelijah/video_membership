from fastapi import FastAPI

from . import config
settings = config.get_settings()

app = FastAPI()

@app.get("/")
def homepage():
    return {"hello": "world", "keyspace": settings.keyspace}

