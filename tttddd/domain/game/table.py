from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Table, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper

from tttddd.core.database import metadata
from .entity import Game
from .schema import GameStatus

__all__ = ('game',)


game = Table(
    'games', metadata,
    Column('gid', UUID(as_uuid=True), primary_key=True, index=True),
    Column(
        'user1_id', UUID(as_uuid=True),
        ForeignKey('users.uid'), nullable=False,
    ),
    Column(
        'user2_id', UUID(as_uuid=True),
        ForeignKey('users.uid'), nullable=False,
    ),
    Column(
        'size', Integer, nullable=False,
    ),
    Column(
        'status',
        Enum(
            GameStatus,
            native_enum=False,
            values_callable=lambda s: [i.value for i in s]
        ),
        nullable=False,
    ),
    Column('created_at', DateTime(), nullable=False, server_default=func.now()),
    Column(
        'updated_at', DateTime(),
        nullable=False, server_default=func.now(), onupdate=func.now(),
    ),
    Column(
        'finished_at', DateTime(), nullable=True,
    ),
)

mapper(
    Game, game,
    properties={
        '_gid': game.c.gid,
        '_user1_id': game.c.user1_id,
        '_user2_id': game.c.user2_id,
        '_size': game.c.size,
        '_status': game.c.status,
        '_finished_at': game.c.finished_at,
    },
    exclude_properties=['created_at', 'updated_at'],
)
