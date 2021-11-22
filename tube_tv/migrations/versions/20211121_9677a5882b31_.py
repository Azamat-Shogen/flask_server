"""empty message

Revision ID: 9677a5882b31
Revises: ce1e373da0d1
Create Date: 2021-11-21 23:00:07.816268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9677a5882b31'
down_revision = 'ce1e373da0d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('film_actors',
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.ForeignKeyConstraint(['film_id'], ['films.id'], ),
    sa.PrimaryKeyConstraint('film_id', 'actor_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('film_actors')
    # ### end Alembic commands ###