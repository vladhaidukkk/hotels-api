from datetime import UTC, datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column

IntPrimaryKey = Annotated[int, mapped_column(primary_key=True)]
CreatedAt = Annotated[
    datetime,
    mapped_column(server_default=text("TIMEZONE('UTC', NOW())")),
]
UpdatedAt = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('UTC', NOW())"),
        # TODO: create a DB trigger to update this column on any update automatically
        onupdate=lambda: datetime.now(UTC),
    ),
]
