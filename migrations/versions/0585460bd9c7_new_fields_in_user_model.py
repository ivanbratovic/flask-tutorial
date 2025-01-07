"""new fields in user model

Revision ID: 0585460bd9c7
Revises: 4a6e6b1c35ea
Create Date: 2025-01-07 10:30:25.591247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0585460bd9c7'
down_revision = '4a6e6b1c35ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about_me', sa.String(length=140), nullable=True))
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_seen')
        batch_op.drop_column('about_me')

    # ### end Alembic commands ###
