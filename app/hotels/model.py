from sqlalchemy import JSON, CheckConstraint, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.core import Base
from app.db.mixins import ReprMixin
from app.db.types import IntPrimaryKey


class HotelModel(ReprMixin, Base):
    __tablename__ = "hotels"

    id: Mapped[IntPrimaryKey]
    name: Mapped[str]
    location: Mapped[str]
    image_name: Mapped[str | None]
    stars: Mapped[int] = mapped_column(SmallInteger)
    services: Mapped[list[str]] = mapped_column(JSON)

    __table_args__ = (
        CheckConstraint("stars BETWEEN 1 AND 5", name="hotels_stars_range_check"),
    )
