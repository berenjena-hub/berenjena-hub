from app import db


class SocialModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower = db.relationship('User', backref='social_model', lazy=True, cascade="all, delete")
    followed = db.relationship('User', backref='social_model', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f'SocialModule<{self.id}>'



