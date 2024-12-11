import pytest
from unittest.mock import MagicMock, patch, mock_open
from flask import Flask
from app.modules.dashboard.routes import dashboard_bp
import os

class MockUser:
    def __init__(self, id=1, authenticated=True):
        self.id = id
        self.is_authenticated = authenticated

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
def mock_current_user_authenticated():
    """Fixture para simular un usuario autenticado."""
    return MockUser()

@pytest.fixture
def mock_current_user_unauthenticated():
    """Fixture para simular un usuario no autenticado."""
    return MockUser(authenticated=False)

def test_index_route_unauthenticated_user(app_client, mock_current_user_unauthenticated):
    """Test que verifica el comportamiento cuando el usuario no está autenticado."""
    mock_dataset_service = MagicMock()
    mock_feature_model_service = MagicMock()

    # Valores de retorno
    mock_dataset_service.count_synchronized_datasets.return_value = 10
   
    mock_dataset_service.count_unsynchronized_datasets.return_value = 5
    mock_dataset_service.total_dataset_downloads.return_value = 20
    mock_dataset_service.total_dataset_views.return_value = 30
    mock_dataset_service.get_synchronized.return_value = [1, 2, 3]
    mock_feature_model_service.count_feature_models.return_value = 7
    mock_feature_model_service.total_feature_model_downloads.return_value = 15
    mock_feature_model_service.total_feature_model_views.return_value = 25

    # Simular contenido del HTML
    mock_html = "<div class='card h-100'></div><div class='card h-100'></div>"

    with patch('app.modules.dashboard.routes.DataSetService', return_value=mock_dataset_service), \
         patch('app.modules.dashboard.routes.FeatureModelService', return_value=mock_feature_model_service), \
         patch('app.modules.dashboard.routes.current_user', new=mock_current_user_unauthenticated), \
         patch('app.modules.dashboard.routes.open', mock_open(read_data=mock_html), create=True), \
         patch('app.modules.dashboard.routes.render_template') as mock_render_template:

        response = app_client.get('/dashboard/')
        assert response.status_code == 200

        mock_render_template.assert_called_once_with(
            'dashboard.html',
            total_datasets=10,
            total_unsynchronized_datasets=0,
            user_datasets_count=0,
            total_feature_models=7,
            total_dataset_downloads=20,
            total_feature_model_downloads=15,
            total_dataset_views=30,
            total_feature_model_views=25,
            total_teams=2
        )


def test_index_route_no_data(app_client, mock_current_user_authenticated):
    """Test que verifica el comportamiento cuando todos los datos devueltos son 0."""
    mock_dataset_service = MagicMock()
    mock_feature_model_service = MagicMock()

    # Todos los valores en 0
    mock_dataset_service.count_synchronized_datasets.return_value = 0
    mock_dataset_service.count_unsynchronized_datasets.return_value = 0
    mock_dataset_service.total_dataset_downloads.return_value = 0
    mock_dataset_service.total_dataset_views.return_value = 0
    mock_dataset_service.get_synchronized.return_value = []  
    mock_feature_model_service.count_feature_models.return_value = 0
    mock_feature_model_service.total_feature_model_downloads.return_value = 0
    mock_feature_model_service.total_feature_model_views.return_value = 0

    # HTML con una sola tarjeta
    mock_html = "<div class='card h-100'></div>"

    with patch('app.modules.dashboard.routes.DataSetService', return_value=mock_dataset_service), \
         patch('app.modules.dashboard.routes.FeatureModelService', return_value=mock_feature_model_service), \
         patch('app.modules.dashboard.routes.current_user', new=mock_current_user_authenticated), \
         patch('app.modules.dashboard.routes.open', mock_open(read_data=mock_html), create=True), \
         patch('app.modules.dashboard.routes.render_template') as mock_render_template:

        response = app_client.get('/dashboard/')
        assert response.status_code == 200

        mock_render_template.assert_called_once_with(
            'dashboard.html',
            total_datasets=0,
            total_unsynchronized_datasets=0,
            user_datasets_count=0, 
            total_feature_models=0,
            total_dataset_downloads=0,
            total_feature_model_downloads=0,
            total_dataset_views=0,
            total_feature_model_views=0,
            total_teams=1
        )

def test_index_route_no_teams(app_client, mock_current_user_authenticated):
    """Test que verifica el comportamiento cuando no hay equipos (no se encuentran tarjetas en el HTML)."""
    mock_dataset_service = MagicMock()
    mock_feature_model_service = MagicMock()

    mock_dataset_service.count_synchronized_datasets.return_value = 10
    mock_dataset_service.count_unsynchronized_datasets.return_value = 2
    mock_dataset_service.total_dataset_downloads.return_value = 5
    mock_dataset_service.total_dataset_views.return_value = 5
    mock_dataset_service.get_synchronized.return_value = [1]  
    mock_feature_model_service.count_feature_models.return_value = 3
    mock_feature_model_service.total_feature_model_downloads.return_value = 1
    mock_feature_model_service.total_feature_model_views.return_value = 2

    # HTML sin tarjetas
    mock_html = ""

    with patch('app.modules.dashboard.routes.DataSetService', return_value=mock_dataset_service), \
         patch('app.modules.dashboard.routes.FeatureModelService', return_value=mock_feature_model_service), \
         patch('app.modules.dashboard.routes.current_user', new=mock_current_user_authenticated), \
         patch('app.modules.dashboard.routes.open', mock_open(read_data=mock_html), create=True), \
         patch('app.modules.dashboard.routes.render_template') as mock_render_template:

        response = app_client.get('/dashboard/')
        assert response.status_code == 200

        mock_render_template.assert_called_once_with(
            'dashboard.html',
            total_datasets=10,
            total_unsynchronized_datasets=2,
            user_datasets_count=1,
            total_feature_models=3,
            total_dataset_downloads=5,
            total_feature_model_downloads=1,
            total_dataset_views=5,
            total_feature_model_views=2,
            total_teams=0
        )

def test_index_route_exception_reading_file(app_client, mock_current_user_authenticated):
    """Test que verifica el comportamiento cuando se produce una excepción al leer el archivo HTML."""
    mock_dataset_service = MagicMock()
    mock_feature_model_service = MagicMock()

    mock_dataset_service.count_synchronized_datasets.return_value = 10
    mock_dataset_service.count_unsynchronized_datasets.return_value = 2
    mock_dataset_service.total_dataset_downloads.return_value = 5
    mock_dataset_service.total_dataset_views.return_value = 5
    mock_dataset_service.get_synchronized.return_value = [1, 2]  
    mock_feature_model_service.count_feature_models.return_value = 3
    mock_feature_model_service.total_feature_model_downloads.return_value = 1
    mock_feature_model_service.total_feature_model_views.return_value = 2

    with patch('app.modules.dashboard.routes.DataSetService', return_value=mock_dataset_service), \
         patch('app.modules.dashboard.routes.FeatureModelService', return_value=mock_feature_model_service), \
         patch('app.modules.dashboard.routes.current_user', new=mock_current_user_authenticated), \
         patch('app.modules.dashboard.routes.open', side_effect=Exception("File error")), \
         patch('app.modules.dashboard.routes.render_template') as mock_render_template:

        response = app_client.get('/dashboard/')
        assert response.status_code == 200

        mock_render_template.assert_called_once_with(
            'dashboard.html',
            total_datasets=10,
            total_unsynchronized_datasets=2,
            user_datasets_count=2,
            total_feature_models=3,
            total_dataset_downloads=5,
            total_feature_model_downloads=1,
            total_dataset_views=5,
            total_feature_model_views=2,
            total_teams=0
        )

def test_index_route_no_synced_datasets_for_user(app_client, mock_current_user_authenticated):
    """Test que verifica el comportamiento cuando el usuario está autenticado pero no tiene datasets sincronizados."""
    mock_dataset_service = MagicMock()
    mock_feature_model_service = MagicMock()

    # Estadísticas genéricas
    mock_dataset_service.count_synchronized_datasets.return_value = 10
    mock_dataset_service.count_unsynchronized_datasets.return_value = 2
    mock_dataset_service.total_dataset_downloads.return_value = 5
    mock_dataset_service.total_dataset_views.return_value = 5
    # Usuario autenticado sin datasets sincronizados
    mock_dataset_service.get_synchronized.return_value = []  
    mock_feature_model_service.count_feature_models.return_value = 3
    mock_feature_model_service.total_feature_model_downloads.return_value = 1
    mock_feature_model_service.total_feature_model_views.return_value = 2

    # HTML con dos equipos
    mock_html = "<div class='card h-100'></div><div class='card h-100'></div>"

    with patch('app.modules.dashboard.routes.DataSetService', return_value=mock_dataset_service), \
         patch('app.modules.dashboard.routes.FeatureModelService', return_value=mock_feature_model_service), \
         patch('app.modules.dashboard.routes.current_user', new=mock_current_user_authenticated), \
         patch('app.modules.dashboard.routes.open', mock_open(read_data=mock_html), create=True), \
         patch('app.modules.dashboard.routes.render_template') as mock_render_template:

        response = app_client.get('/dashboard/')
        assert response.status_code == 200

        mock_render_template.assert_called_once_with(
            'dashboard.html',
            total_datasets=10,
            total_unsynchronized_datasets=2,
            user_datasets_count=0,
            total_feature_models=3,
            total_dataset_downloads=5,
            total_feature_model_downloads=1,
            total_dataset_views=5,
            total_feature_model_views=2,
            total_teams=2
        )

def test_index_route_mixed_html_teams(app_client, mock_current_user_authenticated):
    """Test que verifica el conteo de equipos cuando el HTML tiene divs similares pero no todos con clase 'card h-100'."""
    mock_dataset_service = MagicMock()
    mock_feature_model_service = MagicMock()

    # Estadísticas genéricas
    mock_dataset_service.count_synchronized_datasets.return_value = 5
    mock_dataset_service.count_unsynchronized_datasets.return_value = 1
    mock_dataset_service.total_dataset_downloads.return_value = 10
    mock_dataset_service.total_dataset_views.return_value = 20
    mock_dataset_service.get_synchronized.return_value = [1, 2]  
    mock_feature_model_service.count_feature_models.return_value = 4
    mock_feature_model_service.total_feature_model_downloads.return_value = 3
    mock_feature_model_service.total_feature_model_views.return_value = 5

    # HTML con diferentes divs, solo algunos con 'card h-100'
    mock_html = """
    <div class="card h-100"></div>
    <div class="card"></div>
    <div class="card h-100"></div>
    <div class="card h-100 extra-class"></div>
    <div class="no-card"></div>
    """

    with patch('app.modules.dashboard.routes.DataSetService', return_value=mock_dataset_service), \
         patch('app.modules.dashboard.routes.FeatureModelService', return_value=mock_feature_model_service), \
         patch('app.modules.dashboard.routes.current_user', new=mock_current_user_authenticated), \
         patch('app.modules.dashboard.routes.open', mock_open(read_data=mock_html), create=True), \
         patch('app.modules.dashboard.routes.render_template') as mock_render_template:

        response = app_client.get('/dashboard/')
        assert response.status_code == 200

        mock_render_template.assert_called_once_with(
            'dashboard.html',
            total_datasets=5,
            total_unsynchronized_datasets=1,
            user_datasets_count=2,
            total_feature_models=4,
            total_dataset_downloads=10,
            total_feature_model_downloads=3,
            total_dataset_views=20,
            total_feature_model_views=5,
            total_teams=3
        )