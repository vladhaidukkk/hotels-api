"""Make hotels services required.

Revision ID: e8cc3ca09d6f
Revises: 3e11d1555e35
Create Date: 2024-05-04 08:11:50.843221+00:00

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "e8cc3ca09d6f"
down_revision: str | None = "3e11d1555e35"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "hotels",
        "services",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "hotels",
        "services",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=True,
    )
    # ### end Alembic commands ###
