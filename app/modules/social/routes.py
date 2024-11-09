from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.modules.social import social_bp
from app.modules.social.forms import SocialForm
from app.modules.social.services import SocialService


@social_bp.route('/social', methods=['GET'])
def index():
    return render_template('social/index.html')
