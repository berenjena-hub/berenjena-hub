import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from app.modules.dashboard.routes import dashboard_bp
import os

class MockUser:
    def __init__(self, id=1):
        self.id = id
        self.is_authenticated = True

@pytest.fixture
def app():
    """Crea una instancia de la aplicación Flask para pruebas."""
    app = Flask(__name__)
    app.secret_key = 'test_secret'

    # Establecer el root_path al directorio raíz de la aplicación
    app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    app.root_path = app_root

    app.register_blueprint(dashboard_bp)
    return app

@pytest.fixture
def app_client(app):
    """Crea un cliente de prueba para la aplicación."""
    return app.test_client()

@pytest.fixture
def mock_current_user():
    """Fixture para simular un usuario autenticado."""
    return MockUser()

def test_index_route(app_client, mock_current_user):
    mock_dataset_service = MagicMock()
    mock_feature_model_service = MagicMock()

    # Simular valores de retorno de los servicios
    mock_dataset_service.count_synchronized_datasets.return_value = 10
    mock_dataset_service.count_unsynchronized_datasets.return_value = 5
    mock_dataset_service.total_dataset_downloads.return_value = 20
    mock_dataset_service.total_dataset_views.return_value = 30
    mock_dataset_service.get_synchronized.return_value = [1, 2, 3]
    mock_feature_model_service.count_feature_models.return_value = 7
    mock_feature_model_service.total_feature_model_downloads.return_value = 15
    mock_feature_model_service.total_feature_model_views.return_value = 25

    # Simular contenido del archivo HTML
    mock_html = """
    <div class="card h-100"></div>
    <div class="card h-100"></div>
    <div class="card h-100"></div>
    """

    with patch('app.modules.dashboard.routes.DataSetService', return_value=mock_dataset_service), \
         patch('app.modules.dashboard.routes.FeatureModelService', return_value=mock_feature_model_service), \
         patch('app.modules.dashboard.routes.current_user', new=mock_current_user), \
         patch('app.modules.dashboard.routes.open', create=True) as mock_open, \
         patch('app.modules.dashboard.routes.render_template') as mock_render_template:

        mock_open.return_value.__enter__.return_value.read.return_value = mock_html
        mock_render_template.return_value = "Rendered Template"

        # Realizar la solicitud
        response = app_client.get('/dashboard/')

        # Validar la respuesta
        assert response.status_code == 200
        assert b"Rendered Template" in response.data

        # Validar que render_template fue llamado con los valores correctos
        mock_render_template.assert_called_once_with(
            'dashboard.html',
            total_datasets=10,
            total_unsynchronized_datasets=5,
            user_datasets_count=3,
            total_feature_models=7,
            total_dataset_downloads=20,
            total_feature_model_downloads=15,
            total_dataset_views=30,
            total_feature_model_views=25,
            total_teams=3
        )
