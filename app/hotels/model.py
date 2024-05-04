import asyncio

from sqlalchemy import JSON, CheckConstraint, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.core import Base, session_factory
from app.db.mixins import ReprMixin
from app.db.types import IntPrimaryKey


class HotelModel(ReprMixin, Base):
    __tablename__ = "hotels"

    id: Mapped[IntPrimaryKey]
    name: Mapped[str]
    location: Mapped[str]
    stars: Mapped[int] = mapped_column(SmallInteger)
    services: Mapped[list[str]] = mapped_column(JSON)

    __table_args__ = (
        CheckConstraint("stars BETWEEN 1 AND 5", name="hotels_stars_range_check"),
    )


async def _insert_mock_hotels():
    async with session_factory() as session:
        instances = [
            HotelModel(
                name="Seaside Resort",
                location="Oceanview Boulevard, Miami",
                stars=4,
                services=["wifi", "pool"],
            ),
            HotelModel(
                name="Mountain Escape",
                location="Highlands Lane, Denver",
                stars=5,
                services=["wifi", "ski"],
            ),
            HotelModel(
                name="Urban Hotel Central",
                location="Downtown Crossing, New York",
                stars=5,
                services=["wifi", "parking", "valet"],
            ),
        ]
        session.add_all(instances)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(_insert_mock_hotels())
