"""create posts table

Revision ID: 6d53c21dfa8d
Revises: 
Create Date: 2022-06-01 14:40:22.692555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d53c21dfa8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )


def downgrade() -> None:
    # Logic for undo the changes. Roll back mechanism
    # i.e. delete the table
    op.drop_table('posts')
    pass
