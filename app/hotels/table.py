from sqlalchemy import (
    JSON,
    CheckConstraint,
    Column,
    Integer,
    SmallInteger,
    String,
    Table,
)
from sqlalchemy.sql import insert

from app.db.core import metadata, sync_engine

hotels_table = Table(
    "hotels",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("location", String, nullable=False),
    Column("stars", SmallInteger, nullable=False),
    CheckConstraint("stars BETWEEN 1 AND 5", name="hotels_stars_range_check"),
    Column("services", JSON),
)


def _insert_mock_hotels():
    with sync_engine.begin() as conn:
        insert_stmt = insert(hotels_table).values(
            [
                {
                    "id": 1,
                    "name": "Seaside Resort",
                    "location": "Oceanview Boulevard, Miami",
                    "stars": 4,
                    "services": {"wifi": True, "pool": True, "gym": False},
                },
                {
                    "id": 2,
                    "name": "Mountain Escape",
                    "location": "Highlands Lane, Denver",
                    "stars": 5,
                    "services": {"wifi": True, "pool": False, "ski": True},
                },
                {
                    "id": 3,
                    "name": "Urban Hotel Central",
                    "location": "Downtown Crossing, New York",
                    "stars": 5,
                    "services": {"wifi": True, "parking": True, "valet": True},
                },
            ]
        )
        conn.execute(insert_stmt)


if __name__ == "__main__":
    _insert_mock_hotels()
