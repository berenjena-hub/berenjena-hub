from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.modules.auth.models import User
from app.modules.social import social_bp
from app.modules.social.services import SocialService, FollowService


@social_bp.route('/social', methods=['GET'])
def index():
    follow_service = FollowService()
    friends_data = follow_service.get_follow_between(current_user.id)
    friends_ids = friends_data[0]
    friends = db.session.query(User).filter(User.id.in_(friends_ids)).all()
    return render_template('social/index.html', friends=friends)


@social_bp.route('/get_messages', methods=['GET'])
@login_required
def get_messages():
    social_service = SocialService()
    followed_id = request.args.get('friend_id')
    messages = social_service.fetch_messages(current_user.id, followed_id)
    print(messages)
    return jsonify(messages)


@social_bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    social_service = SocialService()
    data = request.json
    follower_id = current_user.id
    followed_id = data['followed_id']
    text = data['text']
    social_service.send_message(follower_id, followed_id, text)
    return '', 204


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
