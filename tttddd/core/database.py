from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator, Optional

from asyncpg import InterfaceError, InternalClientError, PostgresError
from databases import Database
from lazy_load import lazy
from sqlalchemy import MetaData, create_engine
from sqlalchemy.exc import IntegrityError, ProgrammingError, StatementError
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .conf import postgres_settings
from .exception import RepositoryStorageError
from .json import dumps

__all__ = (
    'asyncpg_exceptions_handling',
    'db_exceptions_handling',
    'AsyncDBEngine',
    'async_engine',
    'engine',
    'metadata',
    'SessionLocal',
)

metadata = MetaData()
async_engine = lazy(lambda: Database(str(postgres_settings.URI)))

engine = create_engine(
    str(postgres_settings.URI),
    json_serializer=dumps
)
session_factory = sessionmaker(bind=engine)
SessionLocal = scoped_session(session_factory)


@asynccontextmanager
async def asyncpg_exceptions_handling(
        engine: Database,
) -> AsyncGenerator[None, None]:
    try:
        async with engine.transaction():
            yield
    except (InterfaceError, InternalClientError, PostgresError) as exc:
        raise RepositoryStorageError(exc)


@contextmanager
def db_exceptions_handling(
        session: Session,
) -> Generator[None, None, None]:
    try:
        yield
    except (IntegrityError, ProgrammingError, StatementError) as exc:
        session.rollback()
        raise RepositoryStorageError(exc)


class AsyncDBEngine:
    def __init__(self, uri: str) -> None:
        self.uri = uri
        self.engine: Optional[Database] = None

    async def connect(self) -> Database:
        if not self.engine:
            self.engine = Database(self.uri)
            await self.engine.connect()

        return self.engine

    async def disconnect(self) -> None:
        if self.engine:
            await self.engine.disconnect()
            self.engine = None

    async def __call__(self) -> Database:
        return await self.connect()
