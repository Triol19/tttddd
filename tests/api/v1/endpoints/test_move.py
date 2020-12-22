from typing import Any, Dict

import pytest
from fastapi import status
from pampy import match
from requests import Session

from tttddd.domain.game import Game


@pytest.fixture
def data(
        game: Game,
) -> Dict[str, Any]:
    return {
        'user_id': str(game.user1_id),
        'x': 0,
        'y': 0,
    }


def test_incorrect_game_id(
        data: Dict[str, str],
        client: Session,
) -> None:
    result = client.post(
        '/v1/games/incorrect_game_id/moves', json=data
    )

    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert match(result.json(), {
        'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        'error': {
            'type': 'VALIDATION_ERROR',
            'message': 'VALUE_ERROR',
            'details': {
                'fields': [
                    {
                        'name': str,
                        'reason': {
                            'type': 'UUID',
                            'message': str,
                        },
                    },
                ],
            },
        },
    }, True)


@pytest.mark.parametrize(
    'missed', ['user_id', 'x', 'y']
)
def test_missed_data(
        missed: str,
        game: Game,
        data: Dict[str, str],
        client: Session,
) -> None:
    data.pop(missed)

    result = client.post(
        f'/v1/games/{game.gid}/moves', json=data
    )

    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert match(result.json(), {
        'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        'error': {
            'type': 'VALIDATION_ERROR',
            'message': 'VALUE_ERROR',
            'details': {
                'fields': [
                    {
                        'name': str,
                        'reason': {
                            'type': 'MISSING',
                            'message': str,
                        },
                    },
                ],
            },
        },
    }, True)


def test_moved(
        data: Dict[str, str],
        game: Game,
        client: Session,
) -> None:
    result = client.post(
        f'/v1/games/{game.gid}/moves', json=data
    )

    assert result.status_code == status.HTTP_201_CREATED
