from typing import Dict
from uuid import uuid4

import pytest
from fastapi import status
from pampy import match
from requests import Session

from tttddd.domain.user import User


@pytest.fixture
def data(
        user1: User,
        user2: User,
) -> Dict[str, str]:
    return {
        'uid1': str(user1.uid),
        'uid2': str(user2.uid),
    }


@pytest.mark.parametrize(
    'missed', ['uid1', 'uid2']
)
def test_missed_data(
        missed: str,
        data: Dict[str, str],
        client: Session,
) -> None:
    data.pop(missed)

    result = client.post('/v1/games', json=data)

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


@pytest.mark.parametrize(
    'wrong', ['uid1', 'uid2']
)
def test_wrong_user(
        wrong: str,
        data: Dict[str, str],
        client: Session,
) -> None:
    data[wrong] = str(uuid4())

    result = client.post('/v1/games', json=data)

    assert result.status_code == status.HTTP_404_NOT_FOUND
    assert match(result.json(), {
        'code': status.HTTP_404_NOT_FOUND,
        'error': {
            'type': 'USER_NOT_FOUND',
            'message': 'USER_ERROR',
            'details': {
                'error': str,
            },
        },
    }, True)


def test_created(
        data: Dict[str, str],
        client: Session,
) -> None:
    result = client.post('/v1/games', json=data)

    assert result.status_code == status.HTTP_201_CREATED
