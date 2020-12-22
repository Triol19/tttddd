from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper

from tttddd.core.database import metadata
from .entity import Move

__all__ = ('move',)


move = Table(
    'moves', metadata,
    Column('mid', UUID(as_uuid=True), primary_key=True, index=True),
    Column(
        'game_id', UUID(as_uuid=True),
        ForeignKey('games.gid'), nullable=False,
    ),
    Column(
        'user_id', UUID(as_uuid=True),
        ForeignKey('users.uid'), nullable=False,
    ),
    Column('x', Integer, nullable=False),
    Column('y', Integer, nullable=False),
    Column('created_at', DateTime(), nullable=False, server_default=func.now()),
)

mapper(
    Move, move,
    properties={
        '_mid': move.c.mid,
        '_game_id': move.c.game_id,
        '_user_id': move.c.user_id,
        '_x': move.c.x,
        '_y': move.c.y,
    },
    exclude_properties=['created_at'],
)
