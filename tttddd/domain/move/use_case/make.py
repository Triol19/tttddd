from abc import ABC, abstractmethod
from typing import Any, Dict
from uuid import UUID

from fastapi import status

from tttddd.domain.game import (
    GameAlreadyFinished,
    GameNotFound,
    GameRepository,
    GameStatus,
)
from tttddd.domain.move import Move, MoveRead
from tttddd.domain.move.repository import (
    MoveRepository,
    WrongMove,
    WrongOrder,
    WrongUser,
)
from tttddd.domain.user import UserNotFound, UserRepository
from tttddd.services.ttt import TTT  # type: ignore

__all__ = (
    'MakeMove',
    'MakeMovePresenter',
    'JsonMakeMovePresenter',
)


class MakeMovePresenter(ABC):
    # flake8: noqa: E704
    @abstractmethod
    def moved(self, move: Move) -> Any: ...

    @abstractmethod
    def game_not_found(self, exc: GameNotFound) -> Any: ...

    @abstractmethod
    def game_finished(self, exc: GameAlreadyFinished) -> Any: ...

    @abstractmethod
    def user_not_found(self, exc: UserNotFound) -> Any: ...

    @abstractmethod
    def wrong_user_move(self, exc: WrongUser) -> Any: ...

    @abstractmethod
    def wrong_order_move(self, exc: WrongOrder) -> Any: ...

    @abstractmethod
    def wrong_move(self, exc: WrongMove) -> Any: ...


class JsonMakeMovePresenter(MakeMovePresenter):
    def moved(self, move: Move) -> Dict[str, Any]:
        data = MoveRead(
            move_id=move.mid,
            game_id=move.game_id,
            user_id=move.user_id,
            x=move.x,
            y=move.y,
        ).dict()
        return {
            'code': status.HTTP_201_CREATED,
            'data': data,
        }

    def game_not_found(self, exc: GameNotFound) -> Dict[str, Any]:
        return {
            'code': status.HTTP_404_NOT_FOUND,
            'error': {
                'type': 'GAME_NOT_FOUND',
                'message': 'GAME_ERROR',
                'details': {'error': str(exc)},
            },
        }

    def game_finished(self, exc: GameAlreadyFinished) -> Dict[str, Any]:
        return {
            'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
            'error': {
                'type': 'VALIDATION_ERROR',
                'message': 'GAME_ERROR',
                'details': {'error': str(exc)},
            },
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

    def wrong_user_move(self, exc: WrongUser) -> Dict[str, Any]:
        return {
            'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
            'error': {
                'type': 'VALIDATION_ERROR',
                'message': 'GAME_ERROR',
                'details': {'error': str(exc)},
            },
        }

    def wrong_order_move(self, exc: WrongOrder) -> Dict[str, Any]:
        return {
            'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
            'error': {
                'type': 'VALIDATION_ERROR',
                'message': 'GAME_ERROR',
                'details': {'error': str(exc)},
            },
        }

    def wrong_move(self, exc: WrongMove) -> Dict[str, Any]:
        return {
            'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
            'error': {
                'type': 'VALIDATION_ERROR',
                'message': 'GAME_ERROR',
                'details': {'error': str(exc)},
            },
        }


class MakeMove:
    def __init__(
            self,
            game_repository: GameRepository,
            user_repository: UserRepository,
            move_repository: MoveRepository,
            presenter: MakeMovePresenter,
    ) -> None:
        self.__game_repository = game_repository
        self.__user_repository = user_repository
        self.__move_repository = move_repository
        self.__presenter = presenter

    async def make(self, gid: UUID, user_id: UUID, x: int, y: int) -> Any:
        try:
            game = self.__game_repository.get_by_id(gid=gid)
            if game.status == GameStatus.FINISHED:
                raise GameAlreadyFinished(game=str(gid))
            self.__user_repository.get_by_id(uid=user_id)
            if user_id not in [
                game.user1_id,
                game.user2_id
            ]:
                raise WrongUser(user=str(user_id))
            moves = self.__move_repository.get_by_gid(gid=gid)
            if moves and moves[-1].user_id == user_id:
                raise WrongOrder(user=str(user_id))
            ttt_service = TTT(
                moves=moves,
                size=game.size,
                x=x,
                y=y,
            )
            ttt_service.validate_and_move()
            move = self.__move_repository.create(
                gid=gid,
                uid=user_id,
                x=x,
                y=y,
            )
            is_finished = ttt_service.is_finished()
            if is_finished:
                self.__game_repository.finish(game)
            return self.__presenter.moved(move)
        except GameNotFound as exc:
            return self.__presenter.game_not_found(exc)
        except GameAlreadyFinished as exc:
            return self.__presenter.game_finished(exc)
        except UserNotFound as exc:
            return self.__presenter.user_not_found(exc)
        except WrongUser as exc:
            return self.__presenter.wrong_user_move(exc)
        except WrongOrder as exc:
            return self.__presenter.wrong_order_move(exc)
        except WrongMove as exc:
            return self.__presenter.wrong_move(exc)
