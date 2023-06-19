import sqlalchemy as sa

from repositories.sqlalchemy.common import meta


api_keys_table = sa.Table(
    'api_keys',
    meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('key', sa.String(256), nullable=False, unique=True),
    # как я понял, ключ уникальный для каждого юзера
    sa.Column('user_id', sa.ForeignKey('users.id'), nullable=False, unique=True),
    sa.Column('last_used', sa.DateTime),
    sa.Column('banned_at', sa.DateTime, default=False),
    sa.Column('created_at', sa.DateTime, default=sa.func.now()),
)
