"""changed ban property type

Revision ID: 3865399b484f
Revises: a338b9e81849
Create Date: 2023-06-19 23:10:46.208203

"""
from datetime import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3865399b484f'
down_revision = 'a338b9e81849'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('api_keys', 'banned_at')
    op.add_column('api_keys', sa.Column('banned_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
