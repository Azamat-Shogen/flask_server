"""empty message

Revision ID: ce1e373da0d1
Revises: 9694a1652e1e
Create Date: 2021-11-21 19:38:11.393442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce1e373da0d1'
down_revision = '9694a1652e1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('genre', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('genre')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genres')
    # ### end Alembic commands ###
