"""tweet like counts

Revision ID: 5bad5c4d6530
Revises: fe09a0828d31
Create Date: 2023-10-04 21:10:24.920717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bad5c4d6530'
down_revision: Union[str, None] = 'fe09a0828d31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tweet_like',
    sa.Column('tweet_id', sa.String(), nullable=False),
    sa.Column('like_count', sa.BIGINT(), nullable=True),
    sa.PrimaryKeyConstraint('tweet_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tweet_like')
    # ### end Alembic commands ###
