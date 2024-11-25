import pytest
from unittest.mock import patch
from app.modules.social.services import FollowService, SocialService
from datetime import datetime, timezone
from app.modules.social.models import Social
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from app.modules.dataset.models import DataSet


@pytest.fixture
def follow_service():
    return FollowService()


@pytest.fixture
def social_service():
    return SocialService()


def test_user1_follows_user2_successful(follow_service):
    """Verifica que el Jonh pueda seguir al Jane, si aún no lo sigue."""
    with patch.object(follow_service.repository, 'get_user_following') as mock_get_following, \
         patch.object(follow_service.repository, 'create') as mock_create:

        mock_get_following.return_value = []

        mock_create.return_value = True

        follower_id = 1
        followed_id = 2

        result, message = follow_service.follow_user(follower_id, followed_id)

        mock_create.assert_called_once_with(follower_id, followed_id)

        assert result is True
        assert message is None


def test_user2_unfollows_user1(follow_service):
    """Verifica que el Jane pueda dejar de seguir al Jonh."""
    with patch.object(follow_service.repository, 'delete') as mock_delete:
        mock_delete.return_value = True

        follower_id = 1
        followed_id = 2
        result, message = follow_service.unfollow_user(follower_id, followed_id)

        assert result is True
        assert message is None
        mock_delete.assert_called_once_with(follower_id, followed_id)


def test_user2_unfollow_user1_without_following(follow_service):
    """Verifica que el Jane no pueda dejar de seguir al Jonh, ya que nunca lo ha seguido."""
    with patch.object(follow_service.repository, 'delete') as mock_delete:
        mock_delete.return_value = None

        follower_id = 2
        followed_id = 1
        result, message = follow_service.unfollow_user(follower_id, followed_id)

        assert result is True
        assert message is None
        mock_delete.assert_called_once_with(follower_id, followed_id)


def test_user1_follows_user2_unsuccessful(follow_service):
    """Verifica que el Jonh no pueda seguir al Jane, ya que lo sigue."""
    with patch.object(follow_service.repository, 'get_user_following') as mock_get_following:
        mock_get_following.return_value = [2]

        follower_id = 1
        followed_id = 2
        result, message = follow_service.follow_user(follower_id, followed_id)

        assert result is False
        assert message == "Ya sigues a este usuario."
        mock_get_following.assert_called_once_with(follower_id)


def test_user1_send_message_user2_succcessful(social_service):
    """Verifica que Jonh le puede enviar un mensaje a Jane."""
    with patch.object(social_service.repository, 'save_message') as mock_send_message:
        mock_send_message.return_value = None

        follower_id = 1
        followed_id = 2
        text = "Esto es un caso de prueba positivo"
        result, message = social_service.send_message(follower_id, followed_id, text)

        assert result is True
        assert message is None
        mock_send_message.assert_called_once_with(follower_id, followed_id, text)


def test_user1_send_comments_dataset_succcessful(social_service):
    """Verifica que Jonh le puede comentar un dataset."""
    with patch.object(social_service.repository, 'save_comments') as mock_send_comment:
        mock_send_comment.return_value = None

        follower_id = 1
        followed_id = 2
        dataset_id = 5
        text = "Esto es un caso de prueba positivo"
        result, message = social_service.send_comments(follower_id, followed_id, dataset_id, text)

        assert result is True
        assert message is None
        mock_send_comment.assert_called_once_with(follower_id, followed_id, dataset_id, text)


def test_fetch_messages_positive(social_service):
    """Verifica que fetch_messages retorna los mensajes correctamente entre dos usuarios."""

    # Simulamos datos de usuarios
    user1 = User(id=1, profile=UserProfile(name="John", surname="Doe", user_id=1))
    user2 = User(id=2, profile=UserProfile(name="Jane", surname="Doe", user_id=2))

    # Simulamos mensajes
    messages = [
        Social(
            text="Hola Jane",
            comment=False,
            created_at=datetime.now(timezone.utc),
            follower=user1.id,
            followed=user2.id
        ),
        Social(
            text="Hola John",
            comment=False,
            created_at=datetime.now(timezone.utc),
            follower=user2.id,
            followed=user1.id
        ),
    ]

    # Mockear el método de la repository para devolver estos mensajes simulados
    with patch.object(social_service.repository, 'get_messages_between') as mock_get_messages, \
         patch('app.modules.social.services.db.session') as mock_db_session:

        # Configuramos el mock para devolver los mensajes simulados
        mock_get_messages.return_value = messages

        # Simulamos el comportamiento de los objetos User y UserProfile para el fetch
        mock_db_session.query.return_value.filter.return_value.first.side_effect = [
            user1,  # Simula que el primer usuario es 'user1'
            user2   # Simula que el segundo usuario es 'user2'
        ]

        # Llamar a la función fetch_messages
        follower_id = 1
        followed_id = 2
        result = social_service.fetch_messages(follower_id, followed_id)

        # Verificar que el resultado es el esperado
        assert len(result) == 2
        assert result[0]["text"] == "Hola Jane"
        assert result[0]["sender"] == "John Doe"
        assert result[1]["text"] == "Hola John"
        assert result[1]["sender"] == "Jane Doe"
        assert "created_at" in result[0]  # Comprobar que la fecha está presente
        assert "created_at" in result[1]  # Comprobar que la fecha está presente


def test_fetch_comments_positive(social_service):
    """Verifica que fetch_comments devuelva los comentarios correctamente."""

    # Simulamos datos de usuarios
    user1 = User(id=1, profile=UserProfile(name="John", surname="Doe", user_id=1))
    user2 = User(id=2, profile=UserProfile(name="Jane", surname="Doe", user_id=2))
    dataset = DataSet(id=3)

    # Simulamos mensajes
    messages = [
        Social(
            text="Esto es un caso de prueba positivo",
            comment=True,
            created_at=datetime.now(timezone.utc),
            follower=user1.id,
            followed=user2.id,
            data_set=dataset.id
        )
    ]

    # Mockear el método de la repository para devolver estos mensajes simulados
    with patch.object(social_service.repository, 'get_comments') as mock_get_comments, \
         patch('app.modules.social.services.db.session') as mock_db_session:

        # Configuramos el mock para devolver los mensajes simulados
        mock_get_comments.return_value = messages

        # Simulamos el comportamiento de los objetos User y UserProfile para el fetch
        # Debemos simular que la consulta devuelve ambos usuarios
        mock_db_session.query.return_value.filter.return_value.all.return_value = [user1]

        data_set = 3
        result = social_service.fetch_comments(data_set)

        # Verificar que el resultado es el esperado
        assert len(result) == 1
        assert result[0]["text"] == "Esto es un caso de prueba positivo"
        assert result[0]["sender"] == "John Doe"
        assert "created_at" in result[0]  # Comprobar que la fecha está presente
