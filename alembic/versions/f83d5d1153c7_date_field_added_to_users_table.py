"""date field added to users table

Revision ID: f83d5d1153c7
Revises: c2fa93c241ff
Create Date: 2023-07-04 00:31:41.323335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f83d5d1153c7'
down_revision = 'c2fa93c241ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_at', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'created_at')
    # ### end Alembic commands ###