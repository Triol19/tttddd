# flake8: noqa: B00

from fastapi import APIRouter, Depends, status

from tttddd.api.responses import JSONResponse
from tttddd.core.schema import ErrorResponseSchema, SuccessResponseSchema
from tttddd.domain.game import GameBoard, GameBoardRead, GameRepository
from tttddd.domain.game.use_case import CreateGame, JsonCreateGamePresenter
from tttddd.domain.user import UserRepository
from tttddd.injector import injector

router = APIRouter()


def create_game_use_case() -> CreateGame:
    return CreateGame(
        user_repository=injector.get(UserRepository),  # type: ignore
        game_repository=injector.get(GameRepository),  # type: ignore
        presenter=JsonCreateGamePresenter(),
    )


@router.post(
    '/games',
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponseSchema[GameBoardRead],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {'model': ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponseSchema},
    },
)
async def create_game(
        game_board: GameBoard,
        use_case: CreateGame = Depends(create_game_use_case),
) -> JSONResponse:
    data = await use_case.create(**game_board.dict())
    return JSONResponse(
        status_code=data['code'],
        content=data,
    )
