import uuid
from cassandra.cqlengine  import columns
from app.users.models import User
from app.users.exceptions import InvalidUserIDException
from cassandra.cqlengine.models import Model
from app.config import get_settings
from app.shortcuts import templates

from .exceptions import(
    InvalidYouTubeVideoURLException,
    VideoAlreadyAddedException
)
from .extractors import extract_video_id

settings = get_settings()


class Video(Model):
    __keyspace__ = settings.keyspace
    host_id =  columns.Text(primary_key=True)  # youtube , vimeo 
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    host_service = columns.Text(default='youtube')
    title = columns.Text() 
    url = columns.Text()
    user_id = columns.UUID()
     # user_display_name
    
    def __str__(self):
        return self.__repr__()
    
    
    def __repr__(self):
        return f"Video(title={self.title}, host_id={self.host_id},host_service={self.host_service})"
    
    def render(self):
        basename = self.host_service #youtube, vimeo
        template_name = f"videos/renderers/{basename}.html"
        context = {"host_id": self.host_id}
        t = templates.get_template(template_name)
        return t.render(context)
    
    def as_data(self):
        return {f"{self.host_service}_id": self.host_id, "path": self.path}
    
    @property
    def path(self):
        return f"/videos/{self.host_id}"
     
    
    @staticmethod
    def add_video(url, user_id=None, **kwargs):
        # extract video_id from url
        # video_id = host_id
        # service API - Youtube/vimeo ...
        host_id = extract_video_id(url)
        if host_id is None:
            raise InvalidYouTubeVideoURLException("Invalid Youtube Video URL")
        user_exists  = User.check_exists(user_id)
        if user_exists is None:
            raise InvalidUserIDException("Invalid user_id")
        # user_obj = User.by_user_id(user_id)
        # user_obj.display_name
        q = Video.objects.allow_filtering().filter(host_id=host_id) #user_id=user_id)
        if q.count() != 0:
            raise VideoAlreadyAddedException("Video already added")
        return Video.create(host_id=host_id, user_id=user_id, url=url, **kwargs)
    
    
    
   # class PrivateVideo(Video):
   #     pass