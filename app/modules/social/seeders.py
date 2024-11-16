from core.seeders.BaseSeeder import BaseSeeder
from app.modules.social.models import Social, Follow
from datetime import datetime, timezone
from app.modules.auth.models import User


class SocialSeeder(BaseSeeder):

    def run(self):
        
        user1 = User.query.filter_by(email='user1@example.com').first()
        user2 = User.query.filter_by(email='user2@example.com').first()

        if not user1 or not user2:
            raise Exception("Users not found. Please seed users first.")

        social = [
            Social(
                text='Hola',
                comment=False,
                created_at=datetime.now(timezone.utc),
                follower=user1.id,
                followed=user2.id,
            ),
            Social(
                text='¿Cómo estás?',
                comment=False,
                created_at=datetime.now(timezone.utc),
                follower=user1.id,
                followed=user2.id,
            ),
            Social(
                text='Hola, estoy bien.',
                comment=False,
                created_at=datetime.now(timezone.utc),
                follower=user2.id,
                followed=user1.id,
            )
            
        ]

        self.seed(social)

        follow = [
            Follow(
                follower_id=user1.id,
                followed_id=user2.id,
            ),
            Follow(
                follower_id=user2.id,
                followed_id=user1.id,
            )
        ]

        self.seed(follow)
