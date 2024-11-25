from flask import Blueprint, render_template
from app.modules.dataset.services import DataSetService
from app.modules.featuremodel.services import FeatureModelService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates')

@dashboard_bp.route('/')
def index():
    dataset_service = DataSetService()
    feature_model_service = FeatureModelService()

    # Obtener estadísticas
    total_datasets = dataset_service.count_synchronized_datasets()
    total_feature_models = feature_model_service.count_feature_models()
    total_dataset_downloads = dataset_service.total_dataset_downloads()
    total_feature_model_downloads = feature_model_service.total_feature_model_downloads()
    total_dataset_views = dataset_service.total_dataset_views()
    total_feature_model_views = feature_model_service.total_feature_model_views()

    return render_template('dashboard.html',
                           total_datasets=total_datasets,
                           total_feature_models=total_feature_models,
                           total_dataset_downloads=total_dataset_downloads,
                           total_feature_model_downloads=total_feature_model_downloads,
                           total_dataset_views=total_dataset_views,
                           total_feature_model_views=total_feature_model_views)
