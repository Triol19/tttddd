from uuid import uuid4

import pytest

from tttddd.core.exception import RepositoryStorageError
from tttddd.domain.game import Game, GameNotFound, GameRepository, GameStatus
from tttddd.domain.user import User


def test_get_by_uid(game: Game, game_repository: GameRepository) -> None:
    result = game_repository.get_by_id(gid=game.gid)

    assert result.gid == game.gid


def test_get_by_uid__not_found(game_repository: GameRepository) -> None:
    with pytest.raises(GameNotFound):
        game_repository.get_by_id(gid=uuid4())


def test_create(
        user1: User,
        user2: User,
        game_repository: GameRepository,
) -> None:
    game = game_repository.create(  # act
        user1=user1.uid,
        user2=user2.uid,
        size=5,
    )

    assert game.gid
    assert game.user1_id
    assert game.user2_id
    assert game.size
    assert game.status == GameStatus.IN_PROGRESS


def test_create__database_error(
        game_repository: GameRepository,
) -> None:
    with pytest.raises(RepositoryStorageError):
        game_repository.create(
            user1=uuid4(),
            user2=uuid4(),
            size=5,
        )


def test_finish(
        game: Game,
        game_repository: GameRepository,
) -> None:
    game_repository.finish(game)  # act

    assert game.finished_at
