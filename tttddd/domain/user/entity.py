from typing import Optional
from uuid import UUID, uuid4

__all__ = (
    'User',
)


class User:
    def __init__(
            self,
            email: str,
            *,
            uid: Optional[UUID] = None,
    ) -> None:
        self._email = email
        self._uid = uid or uuid4()

    @property
    def email(self) -> str:
        return self._email

    @property
    def uid(self) -> UUID:
        return self._uid
