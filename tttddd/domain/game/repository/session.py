from uuid import UUID

from sqlalchemy.orm import Session

from tttddd.core.database import db_exceptions_handling
from .exceptions import GameNotFound
from .interface import GameRepository
from ..entity import Game
from ..table import game as game_table

__all__ = (
    'SessionGameRepository',
)


class SessionGameRepository(GameRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, gid: UUID) -> Game:
        game = self.session.query(Game).filter(
            game_table.c.gid == gid
        ).first()
        if not game:
            raise GameNotFound(game=str(gid))
        return game

    def create(
            self,
            user1: UUID,
            user2: UUID,
            size: int,
    ) -> Game:
        game = Game(
            user1_id=user1,
            user2_id=user2,
            size=size,
        )
        self._save(game)
        return game

    def finish(self, game: Game) -> None:
        game.finish()
        self._save(game)

    def _save(self, game: Game) -> None:
        with db_exceptions_handling(self.session):
            self.session.add(game)
            self.session.commit()
