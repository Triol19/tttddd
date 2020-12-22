from uuid import UUID

from pydantic import BaseModel, validator

__all__ = (
    'MoveRead',
    'UserMove',
)


class UserMove(BaseModel):
    user_id: UUID
    x: int
    y: int


class MoveRead(BaseModel):
    move_id: UUID
    game_id: UUID
    user_id: UUID
    x: int
    y: int

    @validator('move_id', 'game_id', 'user_id')
    def uuid_to_str(cls, v: UUID) -> str:
        return str(v)
