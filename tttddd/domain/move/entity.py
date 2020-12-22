from typing import Optional
from uuid import UUID, uuid4

__all__ = (
    'Move',
)


class Move:
    def __init__(
            self,
            game_id: UUID,
            user_id: UUID,
            x: int,
            y: int,
            *,
            mid: Optional[UUID] = None,
    ) -> None:
        self._mid = mid or uuid4()
        self._game_id = game_id
        self._user_id = user_id
        self._x = x
        self._y = y

    @property
    def mid(self) -> UUID:
        return self._mid

    @property
    def game_id(self) -> UUID:
        return self._game_id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y
