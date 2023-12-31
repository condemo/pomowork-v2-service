"""added updated cards table

Revision ID: 213abe8edfa5
Revises: 9f00c8ad9cef
Create Date: 2023-10-26 01:21:14.633752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '213abe8edfa5'
down_revision = '9f00c8ad9cef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('pomo_count', sa.Integer(), nullable=False),
    sa.Column('price_per_hour', sa.Float(), nullable=True),
    sa.Column('total_price', sa.Float(), nullable=True),
    sa.Column('collected', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cards')
    # ### end Alembic commands ###
