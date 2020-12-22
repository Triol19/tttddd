from uuid import UUID

from sqlalchemy.orm import Session

from .exceptions import UserNotFound
from .interface import UserRepository
from ..entity import User
from ..table import user as user_table

__all__ = (
    'SessionUserRepository',
)


class SessionUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, uid: UUID) -> User:
        user = self.session.query(User).filter(
            user_table.c.uid == uid
        ).first()
        if not user:
            raise UserNotFound(user=str(uid))
        return user
