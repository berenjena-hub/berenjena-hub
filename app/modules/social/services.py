from app.modules.social.repositories import SocialRepository
from core.services.BaseService import BaseService


class SocialService(BaseService):
    def __init__(self):
        super().__init__(SocialRepository())
