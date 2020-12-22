from typing import Any, Dict
from unittest.mock import MagicMock, call
from uuid import uuid4

import pytest

from tests.tools import first
from tttddd.domain.game import Game, GameRepository
from tttddd.domain.game.use_case import CreateGame, CreateGamePresenter
from tttddd.domain.user import UserNotFound, UserRepository


@pytest.fixture
def user_repo() -> UserRepository:
    return MagicMock(spec_set=UserRepository)


@pytest.fixture
def game_repo() -> GameRepository:
    return MagicMock(spec_set=GameRepository)


@pytest.fixture
def presenter() -> CreateGamePresenter:
    return MagicMock(spec_set=CreateGamePresenter)


@pytest.fixture
def use_case(
        user_repo: UserRepository,
        game_repo: GameRepository,
        presenter: CreateGamePresenter,
) -> CreateGame:
    return CreateGame(
        user_repository=user_repo,
        game_repository=game_repo,
        presenter=presenter,
    )


@pytest.fixture
def data() -> Dict[str, Any]:
    return {
        'uid1': uuid4(),
        'uid2': uuid4(),
        'size': 5,
    }


async def test_created(
        game: Game,
        data: Dict[str, Any],
        user_repo: MagicMock,
        game_repo: MagicMock,
        presenter: MagicMock,
        use_case: CreateGame,
) -> None:
    game_repo.create.return_value = game

    await use_case.create(**data)

    user_repo.get_by_id.assert_has_calls([
        call(uid=data['uid1']),
        call(uid=data['uid2']),
    ])

    presenter.created.assert_called()
    assert isinstance(first(presenter.created), Game)


async def test_user_not_found(
        data: Dict[str, Any],
        user_repo: MagicMock,
        presenter: MagicMock,
        use_case: CreateGame,
) -> None:
    user_repo.get_by_id.side_effect = UserNotFound(user='')

    await use_case.create(**data)

    assert isinstance(first(presenter.user_not_found), UserNotFound)
