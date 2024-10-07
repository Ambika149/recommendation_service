"""Create job_postings and user_profiles tables

Revision ID: cfbd8bdf160e
Revises: 
Create Date: 2024-10-07 17:10:20.924339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'cfbd8bdf160e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create job_postings table
    op.create_table(
        'job_postings_1',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('job_title', sa.String(), nullable=False),
        sa.Column('company', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('job_type', sa.String(), nullable=False),
        sa.Column('required_skills', sa.String(), nullable=False),  # Store skills as comma-separated
        sa.Column('experience_level', sa.String(), nullable=False),
    )

    # Create user_profiles table
    op.create_table(
        'user_profiles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('skills', sa.String(), nullable=False),  # Store skills as comma-separated
        sa.Column('experience_level', sa.String(), nullable=False),
        sa.Column('preferences', sa.String(), nullable=False),  # Store preferences as a JSON string
    )


def downgrade():
    # Drop user_profiles and job_postings tables
    op.drop_table('user_profiles')
    op.drop_table('job_postings')
