from sqlalchemy import CheckConstraint, Column, DateTime, String, Table, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper

from tttddd.core.database import metadata
from .entity import User

__all__ = ('user',)


user = Table(
    'users', metadata,
    Column('uid', UUID(as_uuid=True), primary_key=True, index=True),
    Column('email', String, unique=True, index=True, nullable=False),
    Column('created_at', DateTime(), nullable=False, server_default=func.now()),
    Column(
        'updated_at', DateTime(),
        nullable=False, server_default=func.now(), onupdate=func.now(),
    ),

    CheckConstraint('email = LOWER(email)', name='users_email_lower')
)

mapper(
    User, user,
    properties={
        '_email': user.c.email,
        '_uid': user.c.uid,
    },
    exclude_properties=['created_at', 'updated_at'],
)
