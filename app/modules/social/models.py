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
