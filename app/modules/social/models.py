from app import db
from datetime import datetime, timezone


class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256), nullable=False)
    comment = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    follower = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_set = db.Column(db.Integer, db.ForeignKey('data_set.id'), nullable=True)

    def __repr__(self):
        return f'Social<{self.id}>'


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id', name='_follower_followed_uc'),)

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower_id=self.id, followed_id=user.id)
            db.session.add(follow)

    def unfollow(self, user):
        follow = self.followed.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).count() > 0

    def get_followed_users(self):
        return [follow.followed_id for follow in self.followed.all()]
