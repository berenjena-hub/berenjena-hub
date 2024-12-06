import pytest
from unittest.mock import patch, MagicMock
from app.modules.dataset.routes import get_file_content
from app import create_app
import os


@pytest.fixture
def app():
    app = create_app()  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


def test_get_file_content(app):
    file_id = 1
    dataset_id = 1

    with patch('app.modules.dataset.services.DataSetService.get_or_404') as mock_get_or_404:
        mock_dataset = MagicMock()
        mock_dataset.id = dataset_id
        mock_dataset.name = "Dataset 1"
        mock_get_or_404.return_value = mock_dataset
        
        with patch('app.modules.dataset.routes.render_template') as mock_render_template:
            with app.app_context():
                get_file_content(file_id, dataset_id)

            mock_render_template.assert_called_once_with(
                'dataset/file_content.html',  
                file_id=file_id, 
                dataset=mock_dataset 
            )
          

def test_delete_file(app):
    file_name = "test_file.txt"

    file_path = os.path.join('/mock/temp/folder', file_name)

    with patch('app.modules.dataset.routes.current_user') as mock_user:
        mock_user.temp_folder = MagicMock(return_value='/mock/temp/folder') 

        with patch('os.path.exists', return_value=True):
            with patch('os.remove') as mock_remove:
                with app.test_client() as client:
                    response = client.post('/dataset/file/delete', json={"file": file_name})

                mock_remove.assert_called_once_with(file_path)

                assert response.status_code == 200
                assert response.json == {"message": "File deleted successfully"}


def test_delete_file_negative(app):
    file_name = "test_file.txt"

    with patch('app.modules.dataset.routes.current_user') as mock_user:
        mock_user.temp_folder = MagicMock(return_value='/mock/temp/folder')
    
        with patch('os.path.exists', return_value=False):
            with app.test_client() as client:
                response = client.post('/dataset/file/delete', json={"file": file_name})

            assert response.status_code == 200  

            assert response.json == {"error": "Error: File not found"}
