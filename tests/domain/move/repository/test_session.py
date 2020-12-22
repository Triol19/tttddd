from uuid import uuid4

import pytest

from tttddd.core.exception import RepositoryStorageError
from tttddd.domain.game import Game
from tttddd.domain.move import Move, MoveRepository
from tttddd.domain.user import User


def test_get_by_uid(
        game: Game,
        move_user_1: Move,
        move_repository: MoveRepository,
) -> None:
    result = move_repository.get_by_gid(gid=game.gid)

    assert move_user_1.mid in [m.mid for m in result]


def test_create(
        game: Game,
        user1: User,
        move_repository: MoveRepository,
) -> None:
    move = move_repository.create(  # act
        gid=game.gid,
        uid=user1.uid,
        x=3,
        y=3,
    )

    assert move.mid
    assert move.game_id
    assert move.user_id
    assert move.x
    assert move.y


def test_create__database_error(
        move_repository: MoveRepository,
) -> None:
    with pytest.raises(RepositoryStorageError):
        move_repository.create(
            gid=uuid4(),
            uid=uuid4(),
            x=3,
            y=3,
        )
