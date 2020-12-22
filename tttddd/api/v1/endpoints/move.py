# flake8: noqa: B00
from uuid import UUID

from fastapi import APIRouter, Depends, status

from tttddd.api.responses import JSONResponse
from tttddd.core.schema import EmptyResponseSchema, ErrorResponseSchema
from tttddd.domain.game import GameRepository
from tttddd.domain.move import MoveRepository, UserMove
from tttddd.domain.move.use_case import JsonMakeMovePresenter, MakeMove
from tttddd.domain.user import UserRepository
from tttddd.injector import injector

router = APIRouter()


def make_move_use_case() -> MakeMove:
    return MakeMove(
        game_repository=injector.get(GameRepository),  # type: ignore
        user_repository=injector.get(UserRepository),  # type: ignore
        move_repository=injector.get(MoveRepository),  # type: ignore
        presenter=JsonMakeMovePresenter(),
    )


@router.post(
    '/games/{game_id}/moves',
    status_code=status.HTTP_201_CREATED,
    response_model=EmptyResponseSchema,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {'model': ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponseSchema},
    },
)
async def make_move(
        game_id: UUID,
        move: UserMove,
        use_case: MakeMove = Depends(make_move_use_case),
) -> JSONResponse:
    data = await use_case.make(game_id, **move.dict())
    return JSONResponse(
        status_code=data['code'],
        content=data,
    )
