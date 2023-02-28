import uuid
from pydantic import (
    BaseModel,

)

from app.videos.models import Video

from .models import Playlist

class PlaylistCreateSchema(BaseModel):
    title: str # user generated
    user_id: uuid.UUID # request.session user_id