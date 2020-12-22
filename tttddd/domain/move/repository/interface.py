from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from tttddd.domain.move.entity import Move

__all__ = (
    'MoveRepository',
)


class MoveRepository(ABC):
    @abstractmethod
    def get_by_gid(self, gid: UUID) -> List[Move]:
        ...

    @abstractmethod
    def create(
        self,
        gid: UUID,
        uid: UUID,
        x: int,
        y: int,
    ) -> Move:
        ...
