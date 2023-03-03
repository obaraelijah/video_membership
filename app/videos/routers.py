from typing import Optional
import uuid

from starlette.exceptions import HTTPException

from fastapi import APIRouter, Request,Form , Depends
from fastapi.responses import HTMLResponse

from app.users.decorators import login_required
from app.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    is_htmx
    )
from app import utils

from app.watch_events.models import WatchEvent
from .schemas import (
    VideoCreateSchema,
    VideoEditSchema
)

from .models import Video

router = APIRouter(
    prefix='/videos'
)




@router.get("/create", response_class=HTMLResponse)
@login_required
def video_create_view(
    request: Request,
    is_htmx=Depends(is_htmx),
    playlist_id: Optional[uuid.UUID] = None
    ):
    print(playlist_id)
    if is_htmx:
        return render(request, "videos/htmx/create.html", {})
    return render(request, "videos/create.html", {})

@router.post("/create", response_class=HTMLResponse)
@login_required
def video_create_post_view(request: Request, is_htmx=Depends(is_htmx), title: str=Form(...), url: str = Form(...)
):  
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, VideoCreateSchema)
    redirect_path = data.get('path') or "/videos/create"
    
    context = {
        "data": data,
        "errors": errors,
        "title":title,
        "url": url,
    }
    
    if is_htmx:
        """
            Handles all htmx requests
        """
        if len(errors) > 0:
            return render(request, "videos/htmx/create.html", context)
    
        context = {"path": redirect_path, "title": data.get('title')}
        return render(request, "videos/htmx/link.html", context)
    """
    Handles default HTML requests
    """
    
    if len(errors) > 0:
        return render(request, "videos/create.html", context, status_code=400)
    
    return redirect(redirect_path)

@router.get("/", response_class=HTMLResponse)
def video_list_view(request: Request):
    q = Video.objects.all().limit(100)
    context = {
        "object_list": q
    }
    return render(request, "videos/list.html", context)

# host_id ='video-1'
# f"{host_id} is cool"

@router.get("/{host_id}", response_class=HTMLResponse)
def video_detail_view(request: Request, host_id: str):
    obj = get_object_or_404(Video, host_id=host_id)
    start_time = 0
    if request.user.is_authenticated:
        user_id = request.user.username 
        start_time = WatchEvent.get_resume_time(host_id, user_id)
    context = {
        "host_id": host_id,
        "start_time": start_time,
        "object": obj
    }
    return render(request, "videos/detail.html", context)


@router.get("/{host_id}/edit", response_class=HTMLResponse)
@login_required
def video_edit_view(request: Request, host_id: str):
    obj = get_object_or_404(Video, host_id=host_id)
    context = {
        "object": obj
    }
    return render(request, "videos/edit.html", context)



@router.post("/{host_id}/edit", response_class=HTMLResponse)
@login_required
def video_edit_post_view(
    request: Request,
    host_id: str,
    is_htmx=Depends(is_htmx),
    title: str=Form(...),
    url: str = Form(...)
):  
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }
    obj = get_object_or_404(Video, host_id=host_id)
    context = {
        "object": obj
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, VideoEditSchema)
    if len(errors) > 0:
        return render(request, "videos/edit.html", context, status_code=400)
    obj.title = data.get('title') or obj.title 
    obj.update_video_url(url, save=True)
    return render(request, "videos/edit.html", context, status_code=400)


@router.get("/{host_id}/hx-edit", response_class=HTMLResponse)
@login_required
def video_hx_edit_view(
    request: Request, 
    host_id: str, 
    is_htmx=Depends(is_htmx)):
    if not is_htmx:
        raise HTTPException(status_code=400)
    obj = None
    not_found = False
    try:
        obj = get_object_or_404(Video, host_id=host_id)
    except:
        not_found = True
    if not_found:
        return HTMLResponse("Not found, please try again.")
    context = {
        "object": obj
    }
    return render(request, "videos/htmx/edit.html", context) 





@router.post("/{host_id}/hx-edit", response_class=HTMLResponse)
@login_required
def video_hx_edit_post_view(
        request: Request,
        host_id: str, 
        is_htmx=Depends(is_htmx), 
        title: str=Form(...), 
        url: str = Form(...),
        delete: Optional[bool] = Form(default=False)):
    if not is_htmx:
        raise HTTPException(status_code=400)
    obj = None
    not_found = False
    try:
        obj = get_object_or_404(Video, host_id=host_id)
    except:
        not_found = True
    if not_found:
        return HTMLResponse("Not found, please try again.")
    if delete:
        obj.delete()
        return HTMLResponse('Item Deleted')
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, VideoEditSchema)
    if len(errors) > 0:
        return render(request, "videos/htmx/edit.html", context, status_code=400)
    obj.title = data.get('title') or obj.title
    obj.update_video_url(url, save=True)
    context = {
        "object": obj
    }
    return render(request, "videos/htmx/list-inline.html", context)