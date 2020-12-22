import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '202012201650'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('email = LOWER(email)', name='users_email_lower'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_uid'), 'users', ['uid'], unique=False)
    op.create_table('games',
    sa.Column('gid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user1_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user2_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('finished_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user1_id'], ['users.uid'], ),
    sa.ForeignKeyConstraint(['user2_id'], ['users.uid'], ),
    sa.PrimaryKeyConstraint('gid')
    )
    op.create_index(op.f('ix_games_gid'), 'games', ['gid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    pass
