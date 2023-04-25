"""Add bike usage

Revision ID: 0c143aa99437
Revises: c128ed76c460
Create Date: 2023-04-25 23:08:15.332167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c143aa99437'
down_revision = 'c128ed76c460'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bike_usage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scraped_at', sa.DateTime(), nullable=False),
    sa.Column('station_number', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('station_name', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('connected', sa.Boolean(), nullable=True),
    sa.Column('bikes', sa.Integer(), nullable=True),
    sa.Column('stands', sa.Integer(), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bike_usage')
    # ### end Alembic commands ###
