from datetime import datetime, timezone
from app.modules.social.repositories import SocialRepository, FollowRepository
from core.services.BaseService import BaseService


class SocialService(BaseService):
    def __init__(self):
        super().__init__(SocialRepository())


class FollowService(BaseService):
    def __init__(self):
        super().__init__(FollowRepository())

    def follow_user(self, follower_id, followed_id):
        existing_follow = self.repository.get_user_following(follower_id)
        if followed_id in existing_follow:
            return False, "Ya sigues a este usuario."

        followed_at = datetime.now(timezone.utc)
        self.repository.create(follower_id, followed_id, followed_at)
        return True, None

    def unfollow_user(self, follower_id, followed_id):
        self.repository.delete(follower_id, followed_id)
        return True, None
