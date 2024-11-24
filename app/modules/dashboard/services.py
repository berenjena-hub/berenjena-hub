from app.modules.dashboard.repositories import DashboardRepository
from core.services.BaseService import BaseService


class DashboardService(BaseService):
    def __init__(self):
        super().__init__(DashboardRepository())
