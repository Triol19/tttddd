from uuid import UUID

from pydantic import BaseModel

__all__ = (
    'UserRead',
)


class UserRead(BaseModel):
    uid: UUID
    email: str
