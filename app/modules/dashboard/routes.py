from flask import Blueprint, render_template, current_app
from flask_login import current_user
from app.modules.dataset.services import DataSetService
from app.modules.featuremodel.services import FeatureModelService
from bs4 import BeautifulSoup
import os

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates')

@dashboard_bp.route('/')
def index():
    dataset_service = DataSetService()
    feature_model_service = FeatureModelService()

    # Obtener estadísticas generales
    total_datasets = dataset_service.count_synchronized_datasets()
    total_unsynchronized_datasets = dataset_service.count_unsynchronized_datasets(current_user.id)
    total_feature_models = feature_model_service.count_feature_models()
    total_dataset_downloads = dataset_service.total_dataset_downloads()
    total_feature_model_downloads = feature_model_service.total_feature_model_downloads()
    total_dataset_views = dataset_service.total_dataset_views()
    total_feature_model_views = feature_model_service.total_feature_model_views()

    # Obtener estadísticas específicas del usuario actual
    user_datasets_count = len(dataset_service.get_synchronized(current_user.id)) if current_user.is_authenticated else 0

    # Contar dinámicamente el número de equipos
    team_template_path = os.path.join(current_app.root_path, 'modules/team/templates/team/index.html')
    with open(team_template_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        total_teams = len(soup.find_all('div', class_='card h-100'))

    return render_template(
        'dashboard.html',
        total_datasets=total_datasets,
        total_unsynchronized_datasets=total_unsynchronized_datasets,
        user_datasets_count=user_datasets_count,
        total_feature_models=total_feature_models,
        total_dataset_downloads=total_dataset_downloads,
        total_feature_model_downloads=total_feature_model_downloads,
        total_dataset_views=total_dataset_views,
        total_feature_model_views=total_feature_model_views,
        total_teams=total_teams
    )
