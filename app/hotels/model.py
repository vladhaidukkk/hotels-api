from typing import TYPE_CHECKING

from sqlalchemy import JSON, CheckConstraint, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base
from app.db.mixins import ReprMixin
from app.db.types import IntPrimaryKey

if TYPE_CHECKING:
    from app.rooms.model import RoomModel


class HotelModel(ReprMixin, Base):
    __tablename__ = "hotels"

    id: Mapped[IntPrimaryKey]
    name: Mapped[str]
    location: Mapped[str]
    image_name: Mapped[str | None]
    stars: Mapped[int] = mapped_column(SmallInteger)
    services: Mapped[list[str]] = mapped_column(JSON)

    rooms: Mapped[list["RoomModel"]] = relationship(back_populates="hotel")

    __table_args__ = (
        CheckConstraint("stars BETWEEN 1 AND 5", name="hotels_stars_range_check"),
    )

    def __str__(self) -> str:
        return self.name
