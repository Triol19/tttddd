import pytest
from fastapi import status
from pampy import match

from tttddd.domain.game import Game, GameStatus
from tttddd.domain.game.use_case import (
    CreateGamePresenter,
    JsonCreateGamePresenter,
)
from tttddd.domain.user import UserNotFound


@pytest.fixture
def presenter() -> CreateGamePresenter:
    return JsonCreateGamePresenter()


def test_created(
        game: Game,
        presenter: CreateGamePresenter,
) -> None:
    result = presenter.created(game)

    assert isinstance(result, dict)
    assert match(result, {
        'code': status.HTTP_201_CREATED,
        'data': {
            'gid': str,
            'user1_id': str,
            'user2_id': str,
            'size': int,
            'status': GameStatus.IN_PROGRESS,
        }
    }, True)


def test_user_not_found(
        presenter: CreateGamePresenter,
) -> None:
    result = presenter.user_not_found(UserNotFound(user=''))

    assert isinstance(result, dict)
    assert match(result, {
        'code': status.HTTP_404_NOT_FOUND,
        'error': {
            'type': str,
            'message': str,
            'details': {
                'error': str,
            },
        }
    }, True)
