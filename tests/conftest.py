from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from databases import Database
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm.session import Session as DBSession
from sqlalchemy_utils import database_exists
from sqlalchemy_utils.functions import quote

from tttddd.core.conf import postgres_settings
from tttddd.core.database import SessionLocal, async_engine, metadata
from tttddd.domain.game import Game, GameRepository, SessionGameRepository
from tttddd.domain.move import Move
from tttddd.domain.move.repository import MoveRepository, SessionMoveRepository
from tttddd.domain.user import SessionUserRepository, User, UserRepository


@pytest.fixture(scope='session')
def database_uri() -> str:
    return str(postgres_settings.URI)


def create_database(
        database_uri: str,
        encoding: str = 'utf8',
        template: str = 'template1',
) -> None:
    # https://github.com/kvesteri/sqlalchemy-utils/issues/432
    url = make_url(database_uri)
    database = url.database
    url.database = 'postgres'
    sa_engine = create_engine(url, isolation_level='AUTOCOMMIT')
    raw_query = "CREATE DATABASE {0} ENCODING '{1}' TEMPLATE {2}"
    # noinspection StrFormat
    raw_query = raw_query.format(
        quote(sa_engine, database), encoding, quote(sa_engine, template)
    )
    sa_engine.execute(
        raw_query,
        name=database,
        encoding=encoding,
        template=template,
    )


@pytest.fixture(scope='session')
def setup_databases(database_uri: str) -> Generator[None, None, None]:
    if not database_exists(database_uri):
        create_database(database_uri)

    bind = create_engine(database_uri)
    dir_name = Path(__file__).parent
    alembic_config = AlembicConfig(str(dir_name / '..' / 'alembic.ini'))
    alembic_config.set_main_option(
        'script_location', str(dir_name / '..' / 'migrations')
    )
    alembic_upgrade(alembic_config, 'head')

    yield

    bind.execute('delete from alembic_version;')
    metadata.drop_all(bind=bind)


@pytest.fixture(scope='session')
async def engine(setup_databases: None) -> AsyncGenerator[Database, None]:
    await async_engine.connect()

    yield async_engine

    await async_engine.disconnect()


@pytest.fixture
def session(setup_databases: None) -> Generator[DBSession, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
async def conn(engine: Database) -> AsyncGenerator[Database, None]:
    async with engine.transaction(force_rollback=True):
        yield engine


@pytest.fixture
def user1(faker: Faker, session: DBSession) -> User:
    user_ = User(faker.email())
    session.add(user_)
    session.commit()
    return user_


@pytest.fixture
def user2(faker: Faker, session: DBSession) -> User:
    user_ = User(faker.email())
    session.add(user_)
    session.commit()
    return user_


@pytest.fixture
def game(
        user1: User,
        user2: User,
        session: DBSession,
) -> Game:
    game_ = Game(
        user1_id=user1.uid,
        user2_id=user2.uid,
        size=5,
    )
    session.add(game_)
    session.commit()
    return game_


@pytest.fixture
def move_user_1(
        user1: User,
        game: Game,
        session: DBSession,
) -> Move:
    move_ = Move(
        game_id=game.gid,
        user_id=user1.uid,
        x=0,
        y=0,
    )
    session.add(move_)
    session.commit()
    return move_


@pytest.fixture
def move_user_2(
        user2: User,
        game: Game,
        session: DBSession,
) -> Move:
    move_ = Move(
        game_id=game.gid,
        user_id=user2.uid,
        x=0,
        y=1,
    )
    session.add(move_)
    session.commit()
    return move_


@pytest.fixture
def user_repository(session: DBSession) -> UserRepository:
    return SessionUserRepository(session)


@pytest.fixture
def game_repository(session: DBSession) -> GameRepository:
    return SessionGameRepository(session)


@pytest.fixture
def move_repository(session: DBSession) -> MoveRepository:
    return SessionMoveRepository(session)
