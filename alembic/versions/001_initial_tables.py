"""Initial tables for doctors and appointments

Revision ID: 001_initial_tables
Revises: 
Create Date: 2026-10-13 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001_initial_tables'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create doctors table
    op.create_table(
        'doctors',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('specialization', sa.String(), nullable=False),
        sa.Column('start_hour', sa.Integer(), nullable=False),
        sa.Column('end_hour', sa.Integer(), nullable=False),
    )
    op.create_index(op.f('ix_doctors_id'), 'doctors', ['id'], unique=False)

    # Create appointments table
    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('doctor_id', sa.Integer(), sa.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False),
        sa.Column('patient_name', sa.String(), nullable=False),
        sa.Column('slot', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_appointments_id'), 'appointments', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_appointments_id'), table_name='appointments')
    op.drop_table('appointments')
    op.drop_index(op.f('ix_doctors_id'), table_name='doctors')
    op.drop_table('doctors')
