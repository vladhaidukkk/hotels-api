"""Create rooms table.

Revision ID: 7898385cb572
Revises: e8cc3ca09d6f
Create Date: 2024-05-04 17:07:36.100862+00:00

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "7898385cb572"
down_revision: str | None = "e8cc3ca09d6f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("services", sa.JSON(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.CheckConstraint("capacity >= 1", name="rooms_capacity_positive_check"),
        sa.CheckConstraint("price >= 1", name="rooms_price_positive_check"),
        sa.CheckConstraint("quantity >= 0", name="rooms_quantity_non_negative_check"),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("rooms")
    # ### end Alembic commands ###