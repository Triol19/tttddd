from databases import Database
from injector import Injector, Module, provider, singleton
from sqlalchemy.orm import Session

from tttddd.core.conf import postgres_settings
from tttddd.core.database import AsyncDBEngine, SessionLocal
from tttddd.domain.game import GameRepository, SessionGameRepository
from tttddd.domain.move.repository import MoveRepository, SessionMoveRepository
from tttddd.domain.user import SessionUserRepository, UserRepository

__all__ = (
    'injector',
)


class AsyncDBEngineModule(Module):

    @singleton
    @provider
    def session(self) -> AsyncDBEngine:
        return AsyncDBEngine(str(postgres_settings.URI))


class DataBaseModule(Module):

    @singleton
    @provider
    def session(self, session: AsyncDBEngine) -> Database:
        return session.engine  # type: ignore


class DBSessionModule(Module):

    @singleton
    @provider
    def session(self) -> Session:
        return SessionLocal()


class UserRepositoryModule(Module):

    @singleton
    @provider
    def repo(self, session: Session) -> UserRepository:
        return SessionUserRepository(session)


class GameRepositoryModule(Module):

    @singleton
    @provider
    def repo(self, session: Session) -> GameRepository:
        return SessionGameRepository(session)


class MoveRepositoryModule(Module):

    @singleton
    @provider
    def repo(self, session: Session) -> MoveRepository:
        return SessionMoveRepository(session)


injector = Injector([
    AsyncDBEngineModule,
    DataBaseModule,
    DBSessionModule,
    UserRepositoryModule,
    GameRepositoryModule,
    MoveRepositoryModule,
])
