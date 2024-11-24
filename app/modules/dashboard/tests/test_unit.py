import pytest
from flask import Flask
from app.modules.dashboard.routes import dashboard_bp
from app.modules.dashboard.dashboard import create_dashboard
from dash import dcc, html



@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def test_dashboard_route(client):
    response = client.get('/dashboard/')
    
    # Imprimir contenido del error si el estado no es 200
    if response.status_code != 200:
        print("Error en la ruta /dashboard/:", response.data.decode()) 
    
    assert response.status_code == 200
    assert b"Dashboard" in response.data
    assert b"Total Datasets" in response.data
    assert b"Total Views" in response.data
    assert b"New Uploads" in response.data
    assert b"Active Users" in response.data
