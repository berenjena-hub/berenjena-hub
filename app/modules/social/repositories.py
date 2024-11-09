from app.modules.social.models import Social
from core.repositories.BaseRepository import BaseRepository


class SocialRepository(BaseRepository):
    def __init__(self):
        super().__init__(Social)
