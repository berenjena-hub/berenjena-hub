import pytest
from unittest.mock import patch


@pytest.fixture
def rating_service():
    from app.modules.dataset.services import RatingService
    return RatingService()


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