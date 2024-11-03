
from app.modules.socialmodule.models import SocialModule
from core.repositories.BaseRepository import BaseRepository


class SocialModuleRepository(BaseRepository):
    def __init__(self):
        super().__init__(SocialModule)
