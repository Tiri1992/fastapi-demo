"""add foreign key to posts table

Revision ID: 766769e57d20
Revises: 804c08021e77
Create Date: 2022-06-01 15:33:25.550883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '766769e57d20'
down_revision = '804c08021e77'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'posts_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    # Rollback fk constraint
    # op.execute("ALTER TABLE posts DROP CONSTRAINT IF EXISTS posts_users_fk")
    op.drop_constraint('posts_users_fk', 'posts')
    # Drop col
    op.drop_column('posts', 'owner_id')
