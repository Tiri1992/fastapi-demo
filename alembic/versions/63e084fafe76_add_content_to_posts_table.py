"""add content to posts table

Revision ID: 63e084fafe76
Revises: 6d53c21dfa8d
Create Date: 2022-06-01 15:13:25.330299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63e084fafe76'
down_revision = '6d53c21dfa8d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column(
        'posts',
        'content'
    )
