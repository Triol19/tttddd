from typing import Any, Dict
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from tests.tools import first
from tttddd.domain.game import (
    Game,
    GameAlreadyFinished,
    GameNotFound,
    GameRepository,
    GameStatus,
)
from tttddd.domain.move import (
    Move,
    MoveRepository,
    WrongMove,
    WrongOrder,
    WrongUser,
)
from tttddd.domain.move.use_case import MakeMove, MakeMovePresenter
from tttddd.domain.user import UserNotFound, UserRepository


@pytest.fixture
def user_repo() -> UserRepository:
    return MagicMock(spec_set=UserRepository)


@pytest.fixture
def game_repo() -> GameRepository:
    return MagicMock(spec_set=GameRepository)


@pytest.fixture
def move_repo() -> MoveRepository:
    return MagicMock(spec_set=MoveRepository)


@pytest.fixture
def presenter() -> MakeMovePresenter:
    return MagicMock(spec_set=MakeMovePresenter)


@pytest.fixture
def use_case(
        user_repo: UserRepository,
        game_repo: GameRepository,
        move_repo: MoveRepository,
        presenter: MakeMovePresenter,
) -> MakeMove:
    return MakeMove(
        user_repository=user_repo,
        game_repository=game_repo,
        move_repository=move_repo,
        presenter=presenter,
    )


@pytest.fixture
def data(
        game: Game,
) -> Dict[str, Any]:
    return {
        'gid': game.gid,
        'uid': game.user2_id,
        'x': 0,
        'y': 1,
    }


async def test_moved(
        game: Game,
        move_user_1: Move,
        move_user_2: Move,
        data: Dict[str, Any],
        game_repo: MagicMock,
        move_repo: MagicMock,
        presenter: MagicMock,
        use_case: MakeMove,
) -> None:
    game_repo.get_by_id.return_value = game
    move_repo.get_by_gid.return_value = [move_user_1]
    move_repo.create.return_value = move_user_2

    await use_case.make(**data)

    move_repo.create.assert_called()
    presenter.moved.assert_called()
    assert isinstance(first(presenter.moved), Move)


async def test_moved__game_finished(
        game: Game,
        move_user_1: Move,
        move_user_2: Move,
        data: Dict[str, Any],
        game_repo: MagicMock,
        move_repo: MagicMock,
        presenter: MagicMock,
        use_case: MakeMove,
        mocker: MockerFixture,
) -> None:
    game_repo.get_by_id.return_value = game
    move_repo.get_by_gid.return_value = [move_user_1]
    move_repo.create.return_value = move_user_2
    is_finished_patch = mocker.patch('tttddd.services.ttt.TTT.is_finished')
    is_finished_patch.return_value = True

    await use_case.make(**data)

    move_repo.create.assert_called()
    game_repo.finish.assert_called()
    presenter.moved.assert_called()
    assert isinstance(first(presenter.moved), Move)


async def test_game_not_found(
        data: Dict[str, Any],
        game_repo: MagicMock,
        presenter: MagicMock,
        use_case: MakeMove,
) -> None:
    game_repo.get_by_id.side_effect = GameNotFound(game='')

    await use_case.make(**data)

    assert isinstance(first(presenter.game_not_found), GameNotFound)


async def test_game_finished(
        game: Game,
        data: Dict[str, Any],
        game_repo: MagicMock,
        presenter: MagicMock,
        use_case: MakeMove,
) -> None:
    game._status = GameStatus.FINISHED
    game_repo.get_by_id.return_value = game

    await use_case.make(**data)

    assert isinstance(first(presenter.game_finished), GameAlreadyFinished)


async def test_user_not_found(
        data: Dict[str, Any],
        user_repo: MagicMock,
        presenter: MagicMock,
        use_case: MakeMove,
) -> None:
    user_repo.get_by_id.side_effect = UserNotFound(user='')

    await use_case.make(**data)

    assert isinstance(first(presenter.user_not_found), UserNotFound)


async def test_wrong_user_move(
        game: Game,
        data: Dict[str, Any],
        game_repo: MagicMock,
        presenter: MagicMock,
        use_case: MakeMove,
) -> None:
    data['uid'] = uuid4()
    game_repo.get_by_id.return_value = game

    await use_case.make(**data)

    assert isinstance(first(presenter.wrong_user_move), WrongUser)


async def test_wrong_order_move(
        game: Game,
        move_user_1: Move,
        data: Dict[str, Any],
        game_repo: MagicMock,
        move_repo: MagicMock,
        presenter: MagicMock,
        use_case: MakeMove,
) -> None:
    data['uid'] = move_user_1.user_id
    game_repo.get_by_id.return_value = game
    move_repo.get_by_gid.return_value = [move_user_1]

    await use_case.make(**data)

    assert isinstance(first(presenter.wrong_order_move), WrongOrder)


async def test_wrong_move__occupied_field(
        game: Game,
        move_user_1: Move,
        data: Dict[str, Any],
        game_repo: MagicMock,
        move_repo: MagicMock,
        presenter: MagicMock,
        use_case: MakeMove,
) -> None:
    data['x'] = move_user_1.x
    data['y'] = move_user_1.y
    game_repo.get_by_id.return_value = game
    move_repo.get_by_gid.return_value = [move_user_1]

    await use_case.make(**data)

    assert isinstance(first(presenter.wrong_move), WrongMove)


async def test_wrong_move__out_of_range_field(
        game: Game,
        move_user_1: Move,
        data: Dict[str, Any],
        game_repo: MagicMock,
        move_repo: MagicMock,
        presenter: MagicMock,
        use_case: MakeMove,
) -> None:
    data['y'] = 10000000
    game_repo.get_by_id.return_value = game
    move_repo.get_by_gid.return_value = [move_user_1]

    await use_case.make(**data)

    assert isinstance(first(presenter.wrong_move), WrongMove)
