"""add all tables and columns

Revision ID: acf279ae53d7
Revises: 
Create Date: 2025-02-22 21:52:24.141612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acf279ae53d7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=90), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('gamerooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_name', sa.String(length=30), nullable=False),
    sa.Column('player1', sa.Integer(), nullable=False),
    sa.Column('player2', sa.Integer(), nullable=True),
    sa.Column('player3', sa.Integer(), nullable=True),
    sa.Column('player4', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['player1'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['player2'], ['users.id'], ),
    sa.ForeignKeyConstraint(['player3'], ['users.id'], ),
    sa.ForeignKeyConstraint(['player4'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('roundnumber', sa.Integer(), nullable=False),
    sa.Column('ateamscore', sa.Integer(), nullable=False),
    sa.Column('bteamscore', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['gamerooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gameplayscores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player1_predict', sa.Integer(), nullable=False),
    sa.Column('player2_predict', sa.Integer(), nullable=False),
    sa.Column('player3_predict', sa.Integer(), nullable=False),
    sa.Column('player4_predict', sa.Integer(), nullable=False),
    sa.Column('roundwinner', sa.String(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('score_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['gamerooms.id'], ),
    sa.ForeignKeyConstraint(['score_id'], ['scores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('gameplayscores')
    op.drop_table('scores')
    op.drop_table('gamerooms')
    op.drop_table('users')
    # ### end Alembic commands ###
