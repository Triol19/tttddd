from abc import ABC, abstractmethod
from uuid import UUID

from tttddd.domain.game.entity import Game

__all__ = (
    'GameRepository',
)


class GameRepository(ABC):
    @abstractmethod
    def get_by_id(self, gid: UUID) -> Game:
        """
        :raise GameNotFound:
        :raise RepositoryStorageError:
        """

    @abstractmethod
    def create(
            self,
            user1: UUID,
            user2: UUID,
            size: int,
    ) -> Game:
        """
        :raise RepositoryStorageError:
        """

    @abstractmethod
    def finish(self, game: Game) -> None:
        """
        :raise RepositoryStorageError:
        """
