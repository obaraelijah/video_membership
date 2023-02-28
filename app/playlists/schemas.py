import uuid
from pydantic import (
    BaseModel
)

from app.users.exceptions import InvalidUserIDException


from .models import Playlist

class PlaylistCreateSchema(BaseModel):
    title: str  
    user_id:  uuid.UUID # request.  session user_id
    
    
   