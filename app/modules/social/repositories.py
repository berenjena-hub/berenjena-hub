from app.modules.social.models import Social, Follow
from datetime import datetime, timezone
from core.repositories.BaseRepository import BaseRepository


class SocialRepository(BaseRepository):
    def __init__(self):
        super().__init__(Social)

    def save_message(self, follower_id, followed_id, text):
        message = Social(follower=follower_id, followed=followed_id, text=text, comment=False,
                         created_at=datetime.now(timezone.utc))
        self.session.add(message)
        self.session.commit()
        return message

    def get_messages_between(self, follower_id, followed_id):
        sent_messages = self.model.query.filter_by(
            follower=follower_id,
            followed=followed_id
        ).all()
        received_messages = self.model.query.filter_by(
            follower=followed_id,
            followed=follower_id
        ).all()

        conversation = sent_messages + received_messages

        conversation.sort(key=lambda message: message.created_at)

        return conversation

    def save_comments(self, follower_id, followed_id, dataset_id, text):
        message = Social(follower=follower_id, followed=followed_id, text=text, comment=True,
                         data_set=dataset_id, created_at=datetime.now(timezone.utc))
        self.session.add(message)
        self.session.commit()
        return message

    def get_comments(self, dataset_id):
        sent_messages = self.model.query.filter_by(
            data_set=dataset_id,
            comment=True
        ).all()

        sent_messages.sort(key=lambda message: message.created_at)

        return sent_messages


class FollowRepository(BaseRepository):
    def __init__(self):
        super().__init__(Follow)

    def create(self, follower_id, followed_id):
        follow = Follow(follower_id=follower_id, followed_id=followed_id)
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
    
