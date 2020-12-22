from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from arrow import utcnow

from .schema import GameStatus

__all__ = (
    'Game',
)


class Game:
    def __init__(
            self,
            user1_id: UUID,
            user2_id: UUID,
            size: int,
            *,
            gid: Optional[UUID] = None,
    ) -> None:
        self._gid = gid or uuid4()
        self._user1_id = user1_id
        self._user2_id = user2_id
        self._size = size
        self._status = GameStatus.IN_PROGRESS
        self._finished_at = None

    @property
    def gid(self) -> UUID:
        return self._gid

    @property
    def user1_id(self) -> UUID:
        return self._user1_id

    @property
    def user2_id(self) -> UUID:
        return self._user2_id

    @property
    def size(self) -> int:
        return self._size

    @property
    def status(self) -> GameStatus:
        return self._status

    @property
    def finished_at(self) -> Optional[datetime]:
        return self._finished_at

    def finish(self) -> None:
        self._finished_at = utcnow().datetime
