from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime, timezone
from app import db
from app.modules.auth.models import User
from app.modules.dataset.models import DataSet
from app.modules.social.models import Social, Follow
from app.modules.social import social_bp
from app.modules.social.forms import SocialForm, FollowForm
from app.modules.social.services import SocialService, FollowService


@social_bp.route('/social', methods=['GET'])
def index():
    return render_template('social/index.html')


@social_bp.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
    follow_service = FollowService()
    success, message = follow_service.follow_user(current_user.id, user_id)
    if success:
        flash("Ahora sigues a este usuario.", "success")
    else:
        flash(message, "error")
    return redirect(url_for('profile.other_profile', user_id=user_id))


@social_bp.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    follow_service = FollowService()
    success, message = follow_service.unfollow_user(current_user.id, user_id)
    if success:
        flash("Has dejado de seguir a este usuario.", "success")
    else:
        flash(message, "error")
    return redirect(url_for('profile.other_profile', user_id=user_id))
