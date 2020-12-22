from uuid import uuid4

import pytest

from tttddd.domain.user import User, UserNotFound, UserRepository


def test_get_by_id(user1: User, user_repository: UserRepository) -> None:
    result = user_repository.get_by_id(uid=user1.uid)

    assert result.email == user1.email


def test_get_by_id__not_found(user_repository: UserRepository) -> None:
    with pytest.raises(UserNotFound):
        user_repository.get_by_id(uid=uuid4())
