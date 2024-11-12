import pytest
from unittest.mock import patch
from app.modules.social.services import FollowService


@pytest.fixture
def follow_service():
    return FollowService()


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
