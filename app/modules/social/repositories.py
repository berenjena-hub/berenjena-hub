from app.modules.social.models import Social, Follow

from core.repositories.BaseRepository import BaseRepository


class SocialRepository(BaseRepository):
    def __init__(self):
        super().__init__(Social)


class FollowRepository(BaseRepository):
    def __init__(self):
        super().__init__(Follow)
        
    def create(self, follower_id, followed_id, followed_at):
        follow = Follow(follower_id=follower_id, followed_id=followed_id, followed_at=followed_at)
        self.session.add(follow)
        self.session.commit()
        return follow
    
    def delete(self, follower_id, followed_id):
        follow = self.session.query(Follow).filter_by(follower_id=follower_id, followed_id=followed_id).first()
        if follow:
            self.session.delete(follow)
            self.session.commit()
        return follow

    def get_user_following(self, user_id):
        return self.session.query(Follow).filter_by(follower_id=user_id).all()

    def get_user_followed(self, user_id):
        return self.session.query(Follow).filter_by(followed_id=user_id).all()
