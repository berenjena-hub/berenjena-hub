from app.modules.hubfile.services import HubfileService
from core.services.BaseService import BaseService
from app.modules.socialmodule.repositories import SocialModuleRepository


class FeatureModelService(BaseService):
    def __init__(self):
        super().__init__(SocialModuleRepository())
        self.hubfile_service = HubfileService()

    def total_social_module_views(self) -> int:
        return self.hubfile_service.total_hubfile_views()

    def total_social_module_downloads(self) -> int:
        return self.hubfile_service.total_hubfile_downloads()

    def count_social_module(self):
        return self.repository.count_social_module()