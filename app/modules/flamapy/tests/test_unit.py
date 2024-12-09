import pytest
from flask import Flask
from unittest.mock import patch, MagicMock, mock_open
from app.modules.flamapy.routes import flamapy_bp


# TEST DE GLENCOE
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(flamapy_bp)  # Registra el blueprint con las rutas
    with app.test_client() as client:
        yield client


@patch('app.modules.hubfile.services.HubfileService.get_or_404')
@patch('os.path.isfile')
@patch('flamapy.metamodels.fm_metamodel.transformations.UVLReader')
@patch('flamapy.metamodels.fm_metamodel.transformations.GlencoeWriter')
def test_to_glencoe_success(mock_glencoe_writer, mock_uvl_reader, mock_isfile, mock_get_or_404, client):
    # Simula que el archivo existe
    mock_isfile.return_value = True

    # Mock del HubfileService para devolver un archivo simulado
    mock_hubfile = MagicMock()
    mock_hubfile.name = "file10.uvl"
    mock_hubfile.get_path.return_value = "/mock/path/to/file10.uvl"
    mock_get_or_404.return_value = mock_hubfile

    # Mock de UVLReader y GlencoeWriter
    mock_uvl_reader.return_value.transform.return_value = "mocked_feature_model"
    mock_glencoe_writer.return_value.transform.return_value = None
    
    # Simula un parse tree válido para UVLReader
    mock_uvl_reader.return_value.parse_tree = MagicMock()
    mock_uvl_reader.return_value.parse_tree.features.return_value.feature.return_value = "mocked_feature"

    # Simula la apertura del archivo y su lectura con bytes en vez de str
    with patch("builtins.open", mock_open(read_data=b"namespace example;")):
        response = client.get('/flamapy/to_glencoe/10')

    # Asegura que la respuesta sea correcta
    assert response.status_code == 200
