import sqlalchemy as sa

from repositories.sqlalchemy.common import meta


users_table = sa.Table(
    'users',
    meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('username', sa.String(100), unique=True),
    sa.Column('date_joined', sa.DateTime, default=sa.func.now()),
)
