from fastapi import APIRouter, Request,Form 
from fastapi.responses import HTMLResponse

from app.users.decorators import login_required
from app.shortcuts import render, redirect, get_object_or_404
from app import utils

from app.watch_events.models import WatchEvent
from .schemas import PlaylistCreateSchema

from .models import Playlist

router = APIRouter(
    prefix='/playlists'
)


@router.get("/create", response_class=HTMLResponse)
@login_required
def vlaylist_create_view(request: Request):
    return render(request, "playlists/create.html", {})

@router.post("/create", response_class=HTMLResponse)
@login_required
def vlaylist_create_post_view(request: Request,title: str=Form(...), url: str = Form(...)
):  
    raw_data = {
        "title": title,
        "user_id": request.user.username
    }
    print()
    data, errors = utils.valid_schema_data_or_error(raw_data, PlaylistCreateSchema)
    context = {
        "data": data,
        "errors": errors, 
        "url": url,
    }
    if len(errors) > 0:
        return render(request, "playlists/create.html", context, status_code=400)
    obj = Playlist.objects.create(**data)
    redirect_path = data.get('path') or "/playlists/create"
    return redirect(redirect_path)

@router.get("/", response_class=HTMLResponse)
def vlaylist_list_view(request: Request):
    q = Playlist.objects.all().limit(100)
    context = {
        "object_list": q
    }
    return render(request, "playlists/list.html", context)

# host_id ='vlaylist-1'
# f"{host_id} is cool"

@router.get("/{db_id}", response_class=HTMLResponse)
def vlaylist_detail_view(request: Request, db_id: str):
    obj = get_object_or_404(Playlist, db_id=db_id)
    if request.user.is_authenticated:
        user_id = request.user.username 

    context = {
        "object": obj,
        "videos": obj.get_videos(),
    }
    return render(request, "playlists/detail.html", context)
 