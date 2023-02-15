from fastapi import FastAPI

from .users.models import User
from . import config, db
from cassandra.cqlengine.management import sync_table

app = FastAPI()
DB_SESSION = None
 # settings = config.get_settings()


@app.on_event("startup")
def on_startup():
    #triggered when fastapi starts
    print("hello world")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    
@app.get("/")
def homepage():
    return {"hello": "world"} # json data -> REST API
