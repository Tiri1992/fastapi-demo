"""last few columns

Revision ID: 2e2eeee03fc4
Revises: 766769e57d20
Create Date: 2022-06-01 15:45:44.371657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e2eeee03fc4'
down_revision = '766769e57d20'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='TRUE')
    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('NOW()'))
    )


def downgrade() -> None:
    # Rollback, delete the columns added. Negation the above.
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
