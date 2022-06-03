"""add phone number

Revision ID: 1251888b80b7
Revises: b994c8c07b1e
Create Date: 2022-06-01 17:00:10.966333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1251888b80b7'
down_revision = 'b994c8c07b1e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###