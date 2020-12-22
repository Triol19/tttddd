from abc import ABC, abstractmethod
from typing import Any, Dict
from uuid import UUID

from fastapi import status

from tttddd.domain.game import Game, GameBoardRead, GameRepository
from tttddd.domain.user import UserNotFound, UserRepository

__all__ = (
    'CreateGame',
    'CreateGamePresenter',
    'JsonCreateGamePresenter',
)


class CreateGamePresenter(ABC):
    # flake8: noqa: E704
    @abstractmethod
    def created(self, game: Game) -> Any: ...

    @abstractmethod
    def user_not_found(self, exc: UserNotFound) -> Any: ...


class JsonCreateGamePresenter(CreateGamePresenter):
    def created(self, game: Game) -> Dict[str, Any]:
        data = GameBoardRead(
            gid=game.gid,
            user1_id=game.user1_id,
            user2_id=game.user2_id,
            size=game.size,
            status=game.status,
        ).dict()
        return {
            'code': status.HTTP_201_CREATED,
            'data': data,
        }

    def user_not_found(self, exc: UserNotFound) -> Dict[str, Any]:
        return {
            'code': status.HTTP_404_NOT_FOUND,
            'error': {
                'type': 'USER_NOT_FOUND',
                'message': 'USER_ERROR',
                'details': {'error': str(exc)},
            },
        }


class CreateGame:
    def __init__(
            self,
            user_repository: UserRepository,
            game_repository: GameRepository,
            presenter: CreateGamePresenter,
    ) -> None:
        self.__user_repository = user_repository
        self.__game_repository = game_repository
        self.__presenter = presenter

    async def create(self, uid1: UUID, uid2: UUID, size: int) -> Any:
        try:
            self.__user_repository.get_by_id(uid=uid1)
            self.__user_repository.get_by_id(uid=uid2)
        except UserNotFound as exc:
            return self.__presenter.user_not_found(exc)
        game = self.__game_repository.create(
            user1=uid1,
            user2=uid2,
            size=size,
        )
        return self.__presenter.created(game)
