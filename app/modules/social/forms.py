from flask_wtf import FlaskForm
from wtforms import SubmitField


class SocialForm(FlaskForm):
    submit = SubmitField('Save social')


class FollowForm(FlaskForm):
    submit = SubmitField('Save follows')
