"""add user table

Revision ID: 804c08021e77
Revises: 63e084fafe76
Create Date: 2022-06-01 15:22:00.771337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '804c08021e77'
down_revision = '63e084fafe76'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('NOW()'), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('users')
