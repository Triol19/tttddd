from abc import ABC, abstractmethod
from uuid import UUID

from tttddd.domain.user.entity import User

__all__ = (
    'UserRepository',
)


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, uid: UUID) -> User:
        """
        :raise UserNotFound:
        :raise RepositoryStorageError:
        """
