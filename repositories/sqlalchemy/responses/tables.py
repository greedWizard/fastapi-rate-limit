import sqlalchemy as sa

from repositories.sqlalchemy.common import meta


responses_table = sa.Table(
    'responses',
    meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('api_key_id', sa.ForeignKey('api_keys.id'), nullable=False),
    sa.Column('status_code', sa.Integer, nullable=False,),
    sa.Column('responded_at', sa.DateTime, default=sa.func.now()),
    sa.Column('url', sa.String(512), nullable=False),
)
