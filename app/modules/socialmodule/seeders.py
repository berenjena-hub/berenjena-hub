from app.modules.socialmodule.models import SocialModule
from datetime import datetime, timezone
from app.modules.auth.models import User
from core.seeders.BaseSeeder import BaseSeeder


class SocialModuleSeeder(BaseSeeder):

    def run(self):
        
        user1 = User.query.filter_by(email='user1@example.com').first()
        user2 = User.query.filter_by(email='user2@example.com').first()

        if not user1 or not user2:
            raise Exception("Users not found. Please seed users first.")

        SocialModules = [
            # Create any Model object you want to make seed
            SocialModule(
                text='',
                comment=False,
                created_at=datetime.now(timezone.utc),
                follower=user1.id,
                followed=user2.id,
                ),
        ]

        self.seed(SocialModules)
