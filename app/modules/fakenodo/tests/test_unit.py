import pytest
import json
from unittest.mock import patch, mock_open
from flask import Flask
from app.modules.fakenodo import fakenodo_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(fakenodo_bp)
    with app.test_client() as client:
        yield client

def test_get_all(client):
    with patch("builtins.open", mock_open(read_data='{"access": {}, "created": "2024-11-12T20:15:58.781361+00:00", "metadata": {}}')):
        response = client.get('/fakenodo/deposit/depositions')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "access" in data
        assert "created" in data
        assert "metadata" in data

def test_create(client):
    response = client.post('/fakenodo/deposit/depositions')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Deposition created"
    assert data["id"] == 14109910
    assert data["conceptrecid"] == 14109909

def test_upload(client):
    response = client.post('/fakenodo/deposit/depositions/14109910/files')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "File uploaded to deposition 14109910"

def test_publish(client):
    response = client.post('/fakenodo/deposit/depositions/14109910/actions/publish')
    assert response.status_code == 202
    data = json.loads(response.data)
    assert data["message"] == "Deposition 14109910 published"

def test_delete(client):
    response = client.delete('/fakenodo/deposit/depositions/14109910')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Deposition 14109910 deleted"

def test_get_deposition(client):
    with patch("builtins.open", mock_open(read_data='{"pids": {"doi": {"identifier": "10.5281/zenodo.14109910"}}}')):
        response = client.get('/fakenodo/deposit/depositions/14109910')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "pids" in data
        assert "doi" in data["pids"]
        assert "identifier" in data["pids"]["doi"]
