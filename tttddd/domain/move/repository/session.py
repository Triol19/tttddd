from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from tttddd.core.database import db_exceptions_handling
from .interface import MoveRepository
from ..entity import Move
from ..table import move as move_table

__all__ = (
    'SessionMoveRepository',
)


class SessionMoveRepository(MoveRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_gid(self, gid: UUID) -> List[Move]:
        return self.session.query(Move).filter(
            move_table.c.game_id == gid
        ).order_by(move_table.c.created_at).all()

    def create(
            self,
            gid: UUID,
            uid: UUID,
            x: int,
            y: int,
    ) -> Move:
        move = Move(
            game_id=gid,
            user_id=uid,
            x=x,
            y=y,
        )
        self._save(move)
        return move

    def _save(self, move: Move) -> None:
        with db_exceptions_handling(self.session):
            self.session.add(move)
            self.session.commit()
