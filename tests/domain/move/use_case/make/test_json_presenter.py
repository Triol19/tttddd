import pytest
from fastapi import status
from pampy import match

from tttddd.domain.game import GameAlreadyFinished, GameNotFound
from tttddd.domain.move import Move, WrongMove, WrongOrder, WrongUser
from tttddd.domain.move.use_case import (
    JsonMakeMovePresenter,
    MakeMovePresenter,
)
from tttddd.domain.user import UserNotFound


@pytest.fixture
def presenter() -> MakeMovePresenter:
    return JsonMakeMovePresenter()


def test_moved(
        move_user_1: Move,
        presenter: MakeMovePresenter,
) -> None:
    result = presenter.moved(move_user_1)

    assert isinstance(result, dict)
    assert match(result, {
        'code': status.HTTP_201_CREATED,
        'data': {
            'move_id': str,
            'game_id': str,
            'user_id': str,
            'x': int,
            'y': int,
        }
    }, True)


def test_game_not_found(
        presenter: MakeMovePresenter,
) -> None:
    result = presenter.game_not_found(GameNotFound(game=''))

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


def test_game_finished(
        presenter: MakeMovePresenter,
) -> None:
    result = presenter.game_finished(GameAlreadyFinished(game=''))

    assert isinstance(result, dict)
    assert match(result, {
        'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        'error': {
            'type': str,
            'message': str,
            'details': {
                'error': str,
            },
        }
    }, True)


def test_user_not_found(
        presenter: MakeMovePresenter,
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


def test_wrong_user_move(
        presenter: MakeMovePresenter,
) -> None:
    result = presenter.wrong_user_move(WrongUser(user=''))

    assert isinstance(result, dict)
    assert match(result, {
        'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        'error': {
            'type': str,
            'message': str,
            'details': {
                'error': str,
            },
        }
    }, True)


def test_wrong_order_move(
        presenter: MakeMovePresenter,
) -> None:
    result = presenter.wrong_order_move(WrongOrder(user=''))

    assert isinstance(result, dict)
    assert match(result, {
        'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        'error': {
            'type': str,
            'message': str,
            'details': {
                'error': str,
            },
        }
    }, True)


def test_wrong_move(
        presenter: MakeMovePresenter,
) -> None:
    result = presenter.wrong_move(WrongMove(x=0, y=0))

    assert isinstance(result, dict)
    assert match(result, {
        'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        'error': {
            'type': str,
            'message': str,
            'details': {
                'error': str,
            },
        }
    }, True)
