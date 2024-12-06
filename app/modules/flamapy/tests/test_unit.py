import pytest
from unittest.mock import MagicMock, patch
from app.modules.flamapy.routes import flamapy_bp
from flask import Flask
from app.modules.common.dbutils import create_dataset_db


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        create_dataset_db(1)
        pass

    yield test_client


def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(flamapy_bp)
    with app.test_client() as client:
        yield client


@patch('os.path.isfile')
@patch('app.modules.hubfile.services.HubfileService.get_or_404')
@patch('flamapy.metamodels.fm_metamodel.transformations.UVLReader')
@patch('flamapy.metamodels.fm_metamodel.transformations.AFMWriter')
def test_afm_success(exist, get_or_404, reader, writer, client):
    exist.return_value = True
    file = MagicMock()
    file.name = 'file10.uvl'
    get_or_404.return_value = file
    reader.return_value.transform.return_value = 'mocked_model'
    writer.return_value.transform.return_value = None

    response = client.get('/flamapy/to_afm/34')
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=file10.uvl_afm.txt"
