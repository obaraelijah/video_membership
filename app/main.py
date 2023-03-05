import json
import pathlib
from typing import Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires

from .indexing.client import (
    update_index,
    search_index
)
from .playlist.routers import router as playlist_router

from .users.models import User
from . import config, db, utils
from .users.schemas import (
    UserLoginSchema,
    UserSignupSchema
)
from .shortcuts import redirect, render
from .users.backends import JWTCookieBackend
from cassandra.cqlengine.management import sync_table
from pydantic.error_wrappers import ValidationError
from .users.decorators import login_required
from .videos.models import Video
from .videos.routers import router as video_router
from .watch_events.models import WatchEvent
from .watch_events.routers import router as watch_event_router


BASE_DIR = pathlib.Path(__file__).resolve().parent #app/

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
app.include_router(playlist_router)
app.include_router(video_router)
app.include_router(watch_event_router)

from .handlers import * # noqa

@app.on_event("startup")
def on_startup():
    #triggered when fastapi starts
    print("hello world")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    sync_table(Video)
    sync_table(WatchEvent)
    
@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {}, 
        status_code=200)
    return render(request,"home.html", {})

@app.get("/account", response_class=HTMLResponse)
@login_required
def account_view(request: Request): 
    """
    Hello world
    """
    context = {}
    return render(request,"account.html", context)
@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    return render(request, "auth/login.html", {})

@app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request, 
    email: str=Form(...), 
    password: str = Form(...),
    next: Optional[str] = "/"
    ):

    raw_data  = {
        "email": email,
        "password": password,
       
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
    context = {
                "data": data,
                "errors": errors,
            }
    if len(errors) > 0:
        return render(request, "auth/login.html", context, status_code=400)
    if "http://127.0.0.1" not in next:
        next = '/'
    return redirect(next, cookies=data)
 
@app.get("/logout", response_class=HTMLResponse)
def logout_get_view(request: Request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, "auth/logout.html", {})

@app.post("/logout", response_class=HTMLResponse)
def logout_post_view(request: Request):
    return redirect("/login", remove_session=True)  


@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):

    return render(request,"auth/signup.html")



@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request,
    email: str=Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...)
    ):
    raw_data = {
      "email": email,
       "password": password,
       "password_confirm": password_confirm
    }
    data , errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    context = {
        "data": data,
        "errors": errors
    }
    if len(errors) > 0:
        return render(request, "auth/signup.html", context, status_code=400)
    return redirect("/login")
    
@app.post('/update-index', response_class=HTMLResponse)
def htmx_update_index_view(request:Request):
    count = update_index()
    return HTMLResponse(f"({count}) Refreshed")

@app.get("/search", response_class=HTMLResponse)
def search_detail_view(request:Request, q:Optional[str] = None):
    query = None
    context = {}
    if q is not None:
        query = q
        results = search_index(query)
        hits = results.get('hits') or []
        num_hits = results.get('nbHits')
        context = {
            "query": query,
            "hits": hits,
            "num_hits": num_hits
        }
    return render(request, "search/detail.html", context)
