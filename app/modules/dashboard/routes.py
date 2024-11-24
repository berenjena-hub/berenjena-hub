# app/modules/dashboard/router.py

from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates')

@dashboard_bp.route('/')
def index():
    # Datos de ejemplo
    total_datasets = 100
    total_views = 2500
    new_uploads = 20
    active_users = 75

    return render_template('dashboard.html', 
                           total_datasets=total_datasets,
                           total_views=total_views,
                           new_uploads=new_uploads,
                           active_users=active_users)
