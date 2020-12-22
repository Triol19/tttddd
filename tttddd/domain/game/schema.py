from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, validator

__all__ = (
    'GameBoard',
    'GameBoardRead',
    'GameStatus',
)


class GameStatus(Enum):
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'


class GameBoard(BaseModel):
    uid1: UUID
    uid2: UUID
    size: int = Field(default=4)


class GameBoardRead(BaseModel):
    gid: UUID
    user1_id: UUID
    user2_id: UUID
    size: int
    status: GameStatus

    @validator('gid', 'user1_id', 'user2_id')
    def uuid_to_str(cls, v: UUID) -> str:
        return str(v)
