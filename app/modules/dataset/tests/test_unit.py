import pytest
from unittest.mock import patch, MagicMock
from app.modules.dataset.routes import get_file_content
from app import create_app
import os
from werkzeug.exceptions import NotFound


@pytest.fixture
def app():
    app = create_app()  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


@pytest.fixture
def rating_service():
    from app.modules.dataset.services import RatingService
    return RatingService()


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
      
            
def test_get_file_content_not_found(app):
    file_id = 1
    dataset_id = 999 

    with patch('app.modules.dataset.services.DataSetService.get_or_404') as mock_get_or_404:
        mock_get_or_404.side_effect = NotFound()

        with patch('app.modules.dataset.routes.render_template') as mock_render_template:
            with app.app_context():
                try:
                    get_file_content(file_id, dataset_id)
                except NotFound:
                    pass  

            mock_render_template.assert_not_called()
          

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
   
   
def test_add_rating_successful(rating_service):
    """Verifica que se pueda agregar una calificación correctamente."""
    with patch.object(rating_service.repository, 'add_rating') as mock_add_rating:
        mock_add_rating.return_value = True

        user_id = 1
        dataset_id = 2
        quality = 5
        size = 4
        usability = 5

        result = rating_service.add_rating(user_id, dataset_id, quality, size, usability)

        mock_add_rating.assert_called_once_with(
            dataset_id=dataset_id,
            user_id=user_id,
            quality=quality,
            size=size,
            usability=usability
        )

        assert result is True


def test_get_average_rating_successful(rating_service):
    """Verifica que se puedan obtener las calificaciones promedio de un dataset."""
    with patch.object(rating_service.repository, 'get_average_rating') as mock_get_average_rating:
        mock_get_average_rating.return_value = {
            "average_quality": 4.5,
            "average_size": 4.2,
            "average_usability": 4.7,
            "average_total": 4.47,
        }

        dataset_id = 1

        result = rating_service.get_average_rating(dataset_id)

        mock_get_average_rating.assert_called_once_with(dataset_id)

        assert result["average_quality"] == 4.5
        assert result["average_size"] == 4.2
        assert result["average_usability"] == 4.7
        assert result["average_total"] == 4.47


def test_add_rating_invalid_parameters(rating_service):
    """Verifica que agregar una calificación con parámetros inválidos falle."""
    with patch.object(rating_service.repository, 'add_rating') as mock_add_rating:
        mock_add_rating.return_value = None

        user_id = -1  
        dataset_id = -1  
        quality = 6  
        size = 0  
        usability = -1  

        result = rating_service.add_rating(user_id, dataset_id, quality, size, usability)

        mock_add_rating.assert_called_once_with(
            dataset_id=dataset_id,
            user_id=user_id,
            quality=quality,
            size=size,
            usability=usability
        )

        assert result is None


def test_get_average_rating_no_dataset(rating_service):
    """Verifica que get_average_rating falle si el dataset no existe."""
    with patch.object(rating_service.repository, 'get_average_rating') as mock_get_average_rating:
        mock_get_average_rating.return_value = None

        dataset_id = 999  

        result = rating_service.get_average_rating(dataset_id)

        mock_get_average_rating.assert_called_once_with(dataset_id)

        assert result is None
