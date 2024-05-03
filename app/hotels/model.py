import asyncio

from sqlalchemy import JSON, CheckConstraint, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.core import Base, session_factory
from app.db.types import IntPrimaryKey


class HotelModel(Base):
    __tablename__ = "hotels"

    id: Mapped[IntPrimaryKey]
    name: Mapped[str]
    location: Mapped[str]
    stars: Mapped[int] = mapped_column(SmallInteger)
    services: Mapped[dict | None] = mapped_column(JSON)

    __table_args__ = (
        CheckConstraint("stars BETWEEN 1 AND 5", name="hotels_stars_range_check"),
    )


async def _insert_mock_hotels():
    async with session_factory() as session:
        instances = [
            HotelModel(
                id=1,
                name="Seaside Resort",
                location="Oceanview Boulevard, Miami",
                stars=4,
                services={"wifi": True, "pool": True, "gym": False},
            ),
            HotelModel(
                id=2,
                name="Mountain Escape",
                location="Highlands Lane, Denver",
                stars=5,
                services={"wifi": True, "pool": False, "ski": True},
            ),
            HotelModel(
                id=3,
                name="Urban Hotel Central",
                location="Downtown Crossing, New York",
                stars=5,
                services={"wifi": True, "parking": True, "valet": True},
            ),
        ]
        session.add_all(instances)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(_insert_mock_hotels())
