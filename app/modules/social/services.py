from app.modules.social.repositories import SocialRepository, FollowRepository
from app import db
from app.modules.auth.models import User
from core.services.BaseService import BaseService


class SocialService(BaseService):
    def __init__(self):
        super().__init__(SocialRepository())

    def send_message(self, follower_id, followed_id, text):
        self.repository.save_message(follower_id, followed_id, text)
        return True, None

    def fetch_messages(self, follower_id, followed_id):
        messages = self.repository.get_messages_between(follower_id, followed_id)
        current = db.session.query(User).filter(User.id == follower_id).first()
        other = db.session.query(User).filter(User.id == followed_id).first()
        name_current = current.profile.name
        surname_current = current.profile.surname
        name_other = other.profile.name
        surname_other = other.profile.surname
        return [
            {
                "text": msg.text,
                "sender": name_current+" "+surname_current if int(msg.follower) == int(follower_id) 
                else name_other+" "+surname_other,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]


class FollowService(BaseService):
    def __init__(self):
        super().__init__(FollowRepository())

    def follow_user(self, follower_id, followed_id):
        existing_follow = self.repository.get_user_following(follower_id)
        if followed_id in existing_follow:
            return False, "Ya sigues a este usuario."

        self.repository.create(follower_id, followed_id)
        return True, None

    def unfollow_user(self, follower_id, followed_id):
        self.repository.delete(follower_id, followed_id)
        return True, None

    def get_following_user(self, follower_id):
        following_list = self.repository.get_user_following(follower_id)
        return following_list, "Lista de usuarios a los que seigues"

    def get_followers_user(self, user_id):
        followers_list = self.repository.get_user_followed(user_id)
        return followers_list, "Lista de usuarios que te siguen"

    def get_follow_between(self, follower_id):
        following_list = [follow.followed_id for follow in self.repository.get_user_following(follower_id)]
        followers_list = [follow.follower_id for follow in self.repository.get_user_followed(follower_id)]

        # Encuentra la intersección
        mutual_follows = list(set(following_list) & set(followers_list))

        return mutual_follows, "Lista de usuarios que sigues y también te siguen"
