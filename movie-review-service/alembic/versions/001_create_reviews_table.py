"""create reviews table

Revision ID: 001
Revises: 
Create Date: 2024-03-14 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('movie_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('sentiment', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reviews_movie_id'), 'reviews', ['movie_id'], unique=False)
    op.create_index(op.f('ix_reviews_user_id'), 'reviews', ['user_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_reviews_user_id'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_movie_id'), table_name='reviews')
    op.drop_table('reviews') 